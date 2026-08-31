#!/usr/bin/env python3
"""Memory-safe KuaiRand-1K development ranker.

This program uses only the ignored development cache produced by
``scripts/prepare_kuairand_1k_cache.py``.  The cache contains no rows after
2022-04-28, so this program cannot evaluate or train on the public test dates.
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import gc
import hashlib
import json
import math
import time
from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.nn import functional as F


SPLITS = {
    "stack_early": {
        "train": (20220408, 20220409),
        "valid": (20220410, 20220410),
        "forward": (20220411, 20220411),
    },
    "official": {
        "train": (20220408, 20220421),
        "valid": (20220422, 20220428),
    },
    "shadow_early": {
        "train": (20220408, 20220411),
        "valid": (20220412, 20220414),
        "forward": (20220415, 20220417),
    },
    "shadow_middle": {
        "train": (20220408, 20220414),
        "valid": (20220415, 20220417),
        "forward": (20220418, 20220421),
    },
    "shadow_late": {
        "train": (20220408, 20220417),
        "valid": (20220418, 20220421),
        "forward": (20220422, 20220428),
    },
}
AGE_EDGES_DAYS = np.asarray([1, 3, 7, 14, 30, 90, 365], dtype=np.int32)


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def seen_with_min_count(
    values: np.ndarray, dimension: int, minimum_count: int
) -> np.ndarray:
    if minimum_count <= 0:
        raise ValueError("identity minimum count must be positive")
    raw = np.asarray(values, dtype=np.int64)
    valid = raw if not np.any(raw < 0) else raw[raw >= 0]
    counts = np.bincount(valid, minlength=dimension)
    if len(counts) != dimension:
        raise ValueError("identity exceeds declared dimension")
    return counts >= minimum_count


def interaction_ordinals(raw_dates: np.ndarray) -> np.ndarray:
    values = np.asarray(raw_dates, dtype=np.int32)
    unique, inverse = np.unique(values, return_inverse=True)
    ordinals = np.asarray(
        [
            dt.date(int(value) // 10000, (int(value) // 100) % 100, int(value) % 100).toordinal()
            for value in unique
        ],
        dtype=np.int32,
    )
    return ordinals[inverse]


def item_age_buckets(dates: np.ndarray, upload_ordinals: np.ndarray) -> np.ndarray:
    upload = np.asarray(upload_ordinals, dtype=np.int32)
    age = interaction_ordinals(dates) - upload
    valid = (upload >= 0) & (age >= 0)
    return np.where(valid, np.searchsorted(AGE_EDGES_DAYS, age), -1).astype(np.int16)


def recurring_time_fields(
    time_ms: np.ndarray, dates: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Return Asia/Shanghai hour and recurring weekday without raw date IDs."""
    timestamps = np.asarray(time_ms, dtype=np.int64)
    hours = ((timestamps // 3_600_000 + 8) % 24).astype(np.int64)
    weekdays = ((interaction_ordinals(dates) - 1) % 7).astype(np.int64)
    return hours, weekdays


def fast_evaluate(user_ids, labels, scores, k: int = 5) -> dict[str, float | int]:
    """Vectorized-by-user implementation of the unchanged organizer metric."""
    users = np.asarray(user_ids)
    y = np.asarray(labels, dtype=np.uint8)
    prediction = np.asarray(scores, dtype=np.float64)
    if not (len(users) == len(y) == len(prediction)):
        raise ValueError("metric arrays have different lengths")
    grouped = np.argsort(users, kind="stable")
    users = users[grouped]
    y = y[grouped]
    prediction = prediction[grouped]
    starts = np.r_[0, np.flatnonzero(users[1:] != users[:-1]) + 1]
    ends = np.r_[starts[1:], len(users)]
    discounts = 1.0 / np.log2(np.arange(k) + 2.0)
    gnum = 0.0
    gden = 0.0
    ndcg_sum = 0.0
    for start, end in zip(starts, ends):
        group_y = y[start:end]
        group_scores = prediction[start:end]
        positives = int(group_y.sum())
        negatives = len(group_y) - positives
        if positives and negatives:
            ascending = np.argsort(group_scores, kind="stable")
            sorted_scores = group_scores[ascending]
            sorted_y = group_y[ascending]
            tie_starts = np.r_[0, np.flatnonzero(sorted_scores[1:] != sorted_scores[:-1]) + 1]
            tie_ends = np.r_[tie_starts[1:], len(sorted_scores)]
            positive_rank_sum = 0.0
            for tie_start, tie_end in zip(tie_starts, tie_ends):
                # Organizer ranks are one-based; tie_end is exclusive.
                average_rank = (tie_start + 1 + tie_end) / 2.0
                positive_rank_sum += average_rank * int(sorted_y[tie_start:tie_end].sum())
            group_auc = (
                positive_rank_sum - positives * (positives + 1) / 2.0
            ) / (positives * negatives)
            gnum += positives * group_auc
            gden += positives
        descending = np.argsort(-group_scores, kind="stable")[:k]
        gains = group_y[descending].astype(np.float64)
        dcg = float(np.sum(gains * discounts[: len(gains)]))
        ideal_count = min(positives, k)
        idcg = float(np.sum(discounts[:ideal_count]))
        ndcg_sum += 0.0 if idcg == 0.0 else dcg / idcg
    gauc = gnum / gden if gden else 0.5
    ndcg = ndcg_sum / len(starts) if len(starts) else 0.0
    return {
        "GAUC": gauc,
        f"nDCG@{k}": ndcg,
        "primary": (gauc + ndcg) / 2.0,
        "users": int(len(starts)),
        "rows": int(len(y)),
    }


class CachedRows:
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.manifest = json.loads((cache_dir / "manifest.json").read_text())
        if self.manifest["retained_date_range"] != [20220408, 20220428]:
            raise ValueError("cache is not the locked train/validation-only date range")
        self.user = np.load(cache_dir / "user.npy", mmap_mode="r")
        self.video = np.load(cache_dir / "video.npy", mmap_mode="r")
        self.author = np.load(cache_dir / "author.npy", mmap_mode="r")
        self.tag = np.load(cache_dir / "tag.npy", mmap_mode="r")
        self.tag2 = np.load(cache_dir / "tag2.npy", mmap_mode="r")
        self.tag3 = np.load(cache_dir / "tag3.npy", mmap_mode="r")
        self.upload_type = np.load(cache_dir / "upload_type.npy", mmap_mode="r")
        self.video_type = np.load(cache_dir / "video_type.npy", mmap_mode="r")
        self.music_type = np.load(cache_dir / "music_type.npy", mmap_mode="r")
        self.visible_status = np.load(cache_dir / "visible_status.npy", mmap_mode="r")
        self.aspect = np.load(cache_dir / "aspect.npy", mmap_mode="r")
        self.upload_ordinal = np.load(cache_dir / "upload_ordinal.npy", mmap_mode="r")
        self.tab = np.load(cache_dir / "tab.npy", mmap_mode="r")
        self.duration = np.load(cache_dir / "duration.npy", mmap_mode="r")
        self.time_ms = np.load(cache_dir / "time_ms.npy", mmap_mode="r")
        self.is_click = np.load(cache_dir / "is_click.npy", mmap_mode="r")
        self.is_like = np.load(cache_dir / "is_like.npy", mmap_mode="r")
        self.is_follow = np.load(cache_dir / "is_follow.npy", mmap_mode="r")
        self.is_comment = np.load(cache_dir / "is_comment.npy", mmap_mode="r")
        self.is_forward = np.load(cache_dir / "is_forward.npy", mmap_mode="r")
        self.is_hate = np.load(cache_dir / "is_hate.npy", mmap_mode="r")
        self.date = np.load(cache_dir / "date.npy", mmap_mode="r")
        self.label = np.load(cache_dir / "label.npy", mmap_mode="r")
        self.evaluation_remainder = None
        self.evaluation_residue = None
        evaluation_sampling = self.manifest.get("evaluation_sampling")
        if evaluation_sampling:
            self.evaluation_remainder = np.load(
                cache_dir / evaluation_sampling["path"], mmap_mode="r"
            )
            self.evaluation_residue = int(evaluation_sampling["residue"])
        sizes = {
            len(self.user), len(self.video), len(self.author), len(self.tag),
            len(self.tag2), len(self.tag3),
            len(self.upload_type), len(self.video_type), len(self.tab),
            len(self.music_type), len(self.visible_status), len(self.aspect),
            len(self.upload_ordinal),
            len(self.duration), len(self.time_ms), len(self.is_click),
            len(self.is_like), len(self.is_follow), len(self.is_comment),
            len(self.is_forward), len(self.is_hate), len(self.date), len(self.label)
        }
        if sizes != {self.manifest["rows"]}:
            raise ValueError(f"cache array length mismatch: {sizes}")
        if self.evaluation_remainder is not None and len(self.evaluation_remainder) != len(self.user):
            raise ValueError("evaluation-remainder array length mismatch")

    def indices(
        self, bounds: tuple[int, int], *, evaluation: bool = False
    ) -> np.ndarray:
        lo, hi = bounds
        mask = (self.date >= lo) & (self.date <= hi)
        if evaluation and self.evaluation_remainder is not None:
            mask &= self.evaluation_remainder == self.evaluation_residue
        return np.flatnonzero(mask).astype(np.int64)


class Encoder:
    def __init__(
        self,
        rows: CachedRows,
        train_indices: np.ndarray,
        feature_set: str,
        split_mode: str,
        min_video_count: int = 1,
        min_author_count: int = 1,
        time_features: bool = False,
    ):
        self.feature_set = feature_set
        self.time_features = time_features
        self.min_video_count = min_video_count
        self.min_author_count = min_author_count
        train_users = np.asarray(rows.user[train_indices], dtype=np.int64)
        train_videos = np.asarray(rows.video[train_indices], dtype=np.int64)
        train_authors = np.asarray(rows.author[train_indices], dtype=np.int64)
        self.seen_user = seen_with_min_count(
            train_users, rows.manifest["user_count"], 1
        )
        self.seen_video = seen_with_min_count(
            train_videos, rows.manifest["video_count"], min_video_count
        )
        self.seen_author = seen_with_min_count(
            train_authors, rows.manifest["author_count"], min_author_count
        )
        if feature_set in {"content", "cross", "history", "full_history", "item_history", "history_item", "history_item_behavior", "history_item_trend", "history_item_repeat", "history_item_repeat_author_behavior", "history_item_repeat_author_recency", "history_item_repeat_tag_affinity", "history_item_repeat_multitag_affinity", "history_item_repeat_sequence", "sequence", "multitag", "rich"}:
            self.seen_tag = np.zeros(rows.manifest["tag_count"], dtype=np.bool_)
            self.seen_upload_type = np.zeros(
                rows.manifest["upload_type_count"], dtype=np.bool_
            )
            self.seen_video_type = np.zeros(
                rows.manifest["video_type_count"], dtype=np.bool_
            )
            train_tags = np.asarray(rows.tag[train_indices], dtype=np.int64)
            train_uploads = np.asarray(rows.upload_type[train_indices], dtype=np.int64)
            train_types = np.asarray(rows.video_type[train_indices], dtype=np.int64)
            self.seen_tag[train_tags[train_tags >= 0]] = True
            self.seen_upload_type[train_uploads[train_uploads >= 0]] = True
            self.seen_video_type[train_types[train_types >= 0]] = True
            if feature_set == "multitag":
                self.seen_tag2 = np.zeros(rows.manifest["tag_count"], dtype=np.bool_)
                self.seen_tag3 = np.zeros(rows.manifest["tag_count"], dtype=np.bool_)
                train_tag2 = np.asarray(rows.tag2[train_indices], dtype=np.int64)
                train_tag3 = np.asarray(rows.tag3[train_indices], dtype=np.int64)
                self.seen_tag2[train_tag2[train_tag2 >= 0]] = True
                self.seen_tag3[train_tag3[train_tag3 >= 0]] = True
            if feature_set == "rich":
                self.seen_music_type = np.zeros(
                    rows.manifest["music_type_count"], dtype=np.bool_
                )
                self.seen_visible_status = np.zeros(
                    rows.manifest["visible_status_count"], dtype=np.bool_
                )
                self.seen_aspect = np.zeros(
                    rows.manifest["aspect_count"], dtype=np.bool_
                )
                train_music = np.asarray(rows.music_type[train_indices], dtype=np.int64)
                train_visible = np.asarray(
                    rows.visible_status[train_indices], dtype=np.int64
                )
                train_aspect = np.asarray(rows.aspect[train_indices], dtype=np.int64)
                self.seen_music_type[train_music[train_music >= 0]] = True
                self.seen_visible_status[train_visible[train_visible >= 0]] = True
                self.seen_aspect[train_aspect[train_aspect >= 0]] = True
                train_age = item_age_buckets(
                    rows.date[train_indices], rows.upload_ordinal[train_indices]
                )
                self.seen_age = np.zeros(len(AGE_EDGES_DAYS) + 1, dtype=np.bool_)
                self.seen_age[train_age[train_age >= 0]] = True
        self.duration_edges = np.quantile(
            np.asarray(rows.duration[train_indices], dtype=np.float32),
            np.linspace(0.0, 1.0, 11)[1:-1],
        )
        dimensions = [
            rows.manifest["user_count"] + 1,
            rows.manifest["video_count"] + 1,
            rows.manifest["author_count"] + 1,
            rows.manifest["tab_count"] + 1,
            11,
        ]
        if feature_set in {"content", "cross", "history", "full_history", "item_history", "history_item", "history_item_behavior", "history_item_trend", "history_item_repeat", "history_item_repeat_author_behavior", "history_item_repeat_author_recency", "history_item_repeat_tag_affinity", "history_item_repeat_multitag_affinity", "history_item_repeat_sequence", "sequence", "multitag", "rich"}:
            dimensions.extend(
                [
                    rows.manifest["tag_count"] + 1,
                    rows.manifest["upload_type_count"] + 1,
                    rows.manifest["video_type_count"] + 1,
                ]
            )
        if feature_set == "multitag":
            dimensions.extend(
                [rows.manifest["tag_count"] + 1, rows.manifest["tag_count"] + 1]
            )
        if feature_set == "rich":
            dimensions.extend(
                [
                    rows.manifest["music_type_count"] + 1,
                    rows.manifest["visible_status_count"] + 1,
                    rows.manifest["aspect_count"] + 1,
                    len(AGE_EDGES_DAYS) + 2,
                ]
            )
        if feature_set == "cross":
            dimensions.extend(
                [
                    rows.manifest["user_count"] * rows.manifest["tag_count"] + 1,
                    rows.manifest["user_count"] * rows.manifest["upload_type_count"] + 1,
                    rows.manifest["user_count"] * rows.manifest["video_type_count"] + 1,
                    rows.manifest["user_count"] * 10 + 1,
                ]
            )
        if feature_set in {"history", "full_history", "history_item", "history_item_behavior", "history_item_trend", "history_item_repeat", "history_item_repeat_author_behavior", "history_item_repeat_author_recency", "history_item_repeat_tag_affinity", "history_item_repeat_multitag_affinity", "history_item_repeat_sequence"}:
            manifest_name = (
                "full_history_manifest.json"
                if feature_set == "full_history"
                else "history_manifest.json"
            )
            history_manifest_path = rows.cache_dir / manifest_name
            if not history_manifest_path.is_file():
                raise FileNotFoundError(
                    "history features are not prepared; run "
                    "the matching causal history preparation script"
                )
            history_manifest = json.loads(history_manifest_path.read_text())
            if split_mode not in history_manifest.get("splits", {}):
                raise ValueError(f"history manifest has no split {split_mode}")
            self.history = np.load(
                rows.cache_dir / history_manifest["splits"][split_mode]["path"],
                mmap_mode="r",
            )
            if self.history.shape != (len(rows.user), 8):
                raise ValueError(f"history feature shape mismatch: {self.history.shape}")
            # Seven bounded categorical fields plus last-positive-tag identity.
            dimensions.extend([17, 22, 12, 12, 17, 22, 3, rows.manifest["tag_count"] + 1])
        if feature_set in {"item_history", "history_item", "history_item_behavior", "history_item_trend", "history_item_repeat", "history_item_repeat_author_behavior", "history_item_repeat_author_recency", "history_item_repeat_tag_affinity", "history_item_repeat_multitag_affinity", "history_item_repeat_sequence"}:
            behavior = feature_set == "history_item_behavior"
            trend = feature_set == "history_item_trend"
            item_manifest_path = rows.cache_dir / (
                "item_behavior_manifest.json"
                if behavior
                else "item_trend_manifest.json"
                if trend
                else "item_history_manifest.json"
            )
            if not item_manifest_path.is_file():
                raise FileNotFoundError(
                    "causal item history is not prepared; run "
                    "the matching causal item preparation script"
                )
            item_manifest = json.loads(item_manifest_path.read_text())
            if split_mode not in item_manifest.get("splits", {}):
                raise ValueError(f"item history manifest has no split {split_mode}")
            self.item_history = np.load(
                rows.cache_dir / item_manifest["splits"][split_mode]["path"],
                mmap_mode="r",
            )
            expected_item_fields = 8 if behavior or trend else 4
            if self.item_history.shape != (len(rows.user), expected_item_fields):
                raise ValueError(
                    f"item history feature shape mismatch: {self.item_history.shape}"
                )
            dimensions.extend(
                [17, 22, 17, 22]
                + ([22, 22, 22, 22] if behavior else [17, 22, 17, 22] if trend else [])
            )
        if feature_set in {"history_item_repeat", "history_item_repeat_author_behavior", "history_item_repeat_author_recency", "history_item_repeat_tag_affinity", "history_item_repeat_multitag_affinity", "history_item_repeat_sequence"}:
            repeat_manifest_path = rows.cache_dir / "user_entity_history_manifest.json"
            if not repeat_manifest_path.is_file():
                raise FileNotFoundError(
                    "causal user-entity history is not prepared; run "
                    "scripts/prepare_kuairand_27k_user_entity_history.py"
                )
            repeat_manifest = json.loads(repeat_manifest_path.read_text())
            if split_mode not in repeat_manifest.get("splits", {}):
                raise ValueError(f"user-entity history manifest has no split {split_mode}")
            self.user_entity_history = np.load(
                rows.cache_dir / repeat_manifest["splits"][split_mode]["path"],
                mmap_mode="r",
            )
            if self.user_entity_history.shape != (len(rows.user), 4):
                raise ValueError(
                    "user-entity history feature shape mismatch: "
                    f"{self.user_entity_history.shape}"
                )
            dimensions.extend([17, 22, 17, 22])
        if feature_set == "history_item_repeat_tag_affinity":
            tag_history_manifest_path = rows.cache_dir / "user_tag_history_manifest.json"
            if not tag_history_manifest_path.is_file():
                raise FileNotFoundError(
                    "causal user-tag history is not prepared; run "
                    "scripts/prepare_kuairand_27k_user_tag_history.py"
                )
            tag_history_manifest = json.loads(tag_history_manifest_path.read_text())
            if split_mode not in tag_history_manifest.get("splits", {}):
                raise ValueError(f"user-tag history manifest has no split {split_mode}")
            self.user_tag_history = np.load(
                rows.cache_dir / tag_history_manifest["splits"][split_mode]["path"],
                mmap_mode="r",
            )
            if self.user_tag_history.shape != (len(rows.user), 2):
                raise ValueError(
                    "user-tag history feature shape mismatch: "
                    f"{self.user_tag_history.shape}"
                )
            dimensions.extend([17, 22])
        if feature_set == "history_item_repeat_multitag_affinity":
            multitag_manifest_path = rows.cache_dir / "user_multitag_history_manifest.json"
            if not multitag_manifest_path.is_file():
                raise FileNotFoundError(
                    "causal user-multitag history is not prepared; run "
                    "scripts/prepare_kuairand_27k_user_multitag_history.py"
                )
            multitag_manifest = json.loads(multitag_manifest_path.read_text())
            if split_mode not in multitag_manifest.get("splits", {}):
                raise ValueError(f"user-multitag history manifest has no split {split_mode}")
            self.user_multitag_history = np.load(
                rows.cache_dir / multitag_manifest["splits"][split_mode]["path"],
                mmap_mode="r",
            )
            if self.user_multitag_history.shape != (len(rows.user), 2):
                raise ValueError(
                    "user-multitag history feature shape mismatch: "
                    f"{self.user_multitag_history.shape}"
                )
            dimensions.extend([17, 22])
        if feature_set == "history_item_repeat_author_behavior":
            behavior_manifest_path = rows.cache_dir / "user_author_behavior_manifest.json"
            if not behavior_manifest_path.is_file():
                raise FileNotFoundError(
                    "causal user-author behavior is not prepared; run "
                    "scripts/prepare_kuairand_27k_user_author_behavior.py"
                )
            behavior_manifest = json.loads(behavior_manifest_path.read_text())
            if split_mode not in behavior_manifest.get("splits", {}):
                raise ValueError(
                    f"user-author behavior manifest has no split {split_mode}"
                )
            self.user_author_behavior = np.load(
                rows.cache_dir / behavior_manifest["splits"][split_mode]["path"],
                mmap_mode="r",
            )
            if self.user_author_behavior.shape != (len(rows.user), 2):
                raise ValueError(
                    "user-author behavior feature shape mismatch: "
                    f"{self.user_author_behavior.shape}"
                )
            dimensions.extend([22, 22])
        if feature_set == "history_item_repeat_author_recency":
            recency_manifest_path = rows.cache_dir / "user_author_recency_manifest.json"
            if not recency_manifest_path.is_file():
                raise FileNotFoundError(
                    "causal user-author recency is not prepared; run "
                    "scripts/prepare_kuairand_27k_user_author_recency.py"
                )
            recency_manifest = json.loads(recency_manifest_path.read_text())
            if split_mode not in recency_manifest.get("splits", {}):
                raise ValueError(
                    f"user-author recency manifest has no split {split_mode}"
                )
            self.user_author_recency = np.load(
                rows.cache_dir / recency_manifest["splits"][split_mode]["path"],
                mmap_mode="r",
            )
            if self.user_author_recency.shape != (len(rows.user), 2):
                raise ValueError(
                    "user-author recency feature shape mismatch: "
                    f"{self.user_author_recency.shape}"
                )
            dimensions.extend([18, 18])
        if feature_set in {"sequence", "history_item_repeat_sequence"}:
            sequence_manifest_path = rows.cache_dir / "sequence_profile_manifest.json"
            if not sequence_manifest_path.is_file():
                raise FileNotFoundError(
                    "sequence profiles are not prepared; run "
                    "scripts/prepare_kuairand_1k_sequence_profile.py"
                )
            sequence_manifest = json.loads(sequence_manifest_path.read_text())
            if split_mode not in sequence_manifest.get("splits", {}):
                raise ValueError(f"sequence manifest has no split {split_mode}")
            self.sequence = np.load(
                rows.cache_dir / sequence_manifest["splits"][split_mode]["path"],
                mmap_mode="r",
            )
            if self.sequence.shape != (len(rows.user), 11):
                raise ValueError(f"sequence profile shape mismatch: {self.sequence.shape}")
            tag_dimension = rows.manifest["tag_count"] + 1
            dimensions.extend(
                [tag_dimension] * 5 + [7, tag_dimension, 3, tag_dimension, 3, 18]
            )
        if self.time_features:
            dimensions.extend([25, 8])
        self.field_dims = np.asarray(dimensions, dtype=np.int64)
        self.offsets = np.cumsum(np.r_[0, self.field_dims[:-1]]).astype(np.int64)

    def encode(self, rows: CachedRows, indices: np.ndarray) -> np.ndarray:
        users = np.asarray(rows.user[indices], dtype=np.int64)
        videos = np.asarray(rows.video[indices], dtype=np.int64)
        authors = np.asarray(rows.author[indices], dtype=np.int64)
        tabs = np.asarray(rows.tab[indices], dtype=np.int64)
        durations = np.asarray(rows.duration[indices], dtype=np.float32)
        encoded = np.empty((len(indices), len(self.field_dims)), dtype=np.int64)
        encoded[:, 0] = np.where(self.seen_user[users], users + 1, 0) + self.offsets[0]
        encoded[:, 1] = np.where(self.seen_video[videos], videos + 1, 0) + self.offsets[1]
        author_seen = authors >= 0
        author_seen[author_seen] &= self.seen_author[authors[author_seen]]
        encoded[:, 2] = np.where(author_seen, authors + 1, 0) + self.offsets[2]
        encoded[:, 3] = tabs + 1 + self.offsets[3]
        encoded[:, 4] = np.searchsorted(self.duration_edges, durations) + 1 + self.offsets[4]
        if self.feature_set in {"content", "cross", "history", "full_history", "item_history", "history_item", "history_item_behavior", "history_item_trend", "history_item_repeat", "history_item_repeat_author_behavior", "history_item_repeat_author_recency", "history_item_repeat_tag_affinity", "history_item_repeat_multitag_affinity", "history_item_repeat_sequence", "sequence", "multitag", "rich"}:
            for column, values, seen in (
                (5, np.asarray(rows.tag[indices], dtype=np.int64), self.seen_tag),
                (
                    6,
                    np.asarray(rows.upload_type[indices], dtype=np.int64),
                    self.seen_upload_type,
                ),
                (
                    7,
                    np.asarray(rows.video_type[indices], dtype=np.int64),
                    self.seen_video_type,
                ),
            ):
                value_seen = values >= 0
                value_seen[value_seen] &= seen[values[value_seen]]
                encoded[:, column] = (
                    np.where(value_seen, values + 1, 0) + self.offsets[column]
                )
        if self.feature_set == "cross":
            user_seen = self.seen_user[users]
            cross_values = (
                (
                    8,
                    np.asarray(rows.tag[indices], dtype=np.int64),
                    self.seen_tag,
                    rows.manifest["tag_count"],
                ),
                (
                    9,
                    np.asarray(rows.upload_type[indices], dtype=np.int64),
                    self.seen_upload_type,
                    rows.manifest["upload_type_count"],
                ),
                (
                    10,
                    np.asarray(rows.video_type[indices], dtype=np.int64),
                    self.seen_video_type,
                    rows.manifest["video_type_count"],
                ),
            )
            for column, values, seen, cardinality in cross_values:
                value_seen = values >= 0
                value_seen[value_seen] &= seen[values[value_seen]]
                valid = user_seen & value_seen
                identity = users * cardinality + np.maximum(values, 0) + 1
                encoded[:, column] = np.where(valid, identity, 0) + self.offsets[column]
            duration_bucket = np.searchsorted(self.duration_edges, durations)
            duration_identity = users * 10 + duration_bucket + 1
            encoded[:, 11] = (
                np.where(user_seen, duration_identity, 0) + self.offsets[11]
            )
        if self.feature_set == "multitag":
            for column, values, seen in (
                (8, np.asarray(rows.tag2[indices], dtype=np.int64), self.seen_tag2),
                (9, np.asarray(rows.tag3[indices], dtype=np.int64), self.seen_tag3),
            ):
                value_seen = values >= 0
                value_seen[value_seen] &= seen[values[value_seen]]
                encoded[:, column] = (
                    np.where(value_seen, values + 1, 0) + self.offsets[column]
                )
        if self.feature_set == "rich":
            rich_values = (
                (8, np.asarray(rows.music_type[indices], dtype=np.int64), self.seen_music_type),
                (
                    9,
                    np.asarray(rows.visible_status[indices], dtype=np.int64),
                    self.seen_visible_status,
                ),
                (10, np.asarray(rows.aspect[indices], dtype=np.int64), self.seen_aspect),
                (
                    11,
                    item_age_buckets(rows.date[indices], rows.upload_ordinal[indices]).astype(
                        np.int64
                    ),
                    self.seen_age,
                ),
            )
            for column, values, seen in rich_values:
                value_seen = values >= 0
                value_seen[value_seen] &= seen[values[value_seen]]
                encoded[:, column] = (
                    np.where(value_seen, values + 1, 0) + self.offsets[column]
                )
        if self.feature_set in {"history", "full_history", "history_item", "history_item_behavior", "history_item_trend", "history_item_repeat", "history_item_repeat_author_behavior", "history_item_repeat_author_recency", "history_item_repeat_tag_affinity", "history_item_repeat_multitag_affinity", "history_item_repeat_sequence"}:
            history = np.asarray(self.history[indices], dtype=np.int64)
            for history_column in range(7):
                column = 8 + history_column
                encoded[:, column] = history[:, history_column] + 1 + self.offsets[column]
            last_tag = history[:, 7]
            encoded[:, 15] = (
                np.where(last_tag >= 0, last_tag + 1, 0) + self.offsets[15]
            )
        if self.feature_set in {"item_history", "history_item", "history_item_behavior", "history_item_trend", "history_item_repeat", "history_item_repeat_author_behavior", "history_item_repeat_author_recency", "history_item_repeat_tag_affinity", "history_item_repeat_multitag_affinity", "history_item_repeat_sequence"}:
            history = np.asarray(self.item_history[indices], dtype=np.int64)
            for item_column in range(history.shape[1]):
                column = (
                    16
                    if self.feature_set in {"history_item", "history_item_behavior", "history_item_trend", "history_item_repeat", "history_item_repeat_author_behavior", "history_item_repeat_author_recency", "history_item_repeat_tag_affinity", "history_item_repeat_multitag_affinity", "history_item_repeat_sequence"}
                    else 8
                ) + item_column
                encoded[:, column] = history[:, item_column] + 1 + self.offsets[column]
        if self.feature_set in {"history_item_repeat", "history_item_repeat_author_behavior", "history_item_repeat_author_recency", "history_item_repeat_tag_affinity", "history_item_repeat_multitag_affinity", "history_item_repeat_sequence"}:
            repeat = np.asarray(self.user_entity_history[indices], dtype=np.int64)
            for repeat_column in range(repeat.shape[1]):
                column = 20 + repeat_column
                encoded[:, column] = repeat[:, repeat_column] + 1 + self.offsets[column]
        if self.feature_set == "history_item_repeat_tag_affinity":
            tag_history = np.asarray(self.user_tag_history[indices], dtype=np.int64)
            for tag_history_column in range(tag_history.shape[1]):
                column = 24 + tag_history_column
                encoded[:, column] = (
                    tag_history[:, tag_history_column] + 1 + self.offsets[column]
                )
        if self.feature_set == "history_item_repeat_multitag_affinity":
            multitag_history = np.asarray(
                self.user_multitag_history[indices], dtype=np.int64
            )
            for multitag_column in range(multitag_history.shape[1]):
                column = 24 + multitag_column
                encoded[:, column] = (
                    multitag_history[:, multitag_column] + 1 + self.offsets[column]
                )
        if self.feature_set == "history_item_repeat_author_behavior":
            behavior = np.asarray(self.user_author_behavior[indices], dtype=np.int64)
            for behavior_column in range(behavior.shape[1]):
                column = 24 + behavior_column
                encoded[:, column] = (
                    behavior[:, behavior_column] + 1 + self.offsets[column]
                )
        if self.feature_set == "history_item_repeat_author_recency":
            recency = np.asarray(self.user_author_recency[indices], dtype=np.int64)
            for recency_column in range(recency.shape[1]):
                column = 24 + recency_column
                encoded[:, column] = recency[:, recency_column] + 1 + self.offsets[column]
        if self.feature_set in {"sequence", "history_item_repeat_sequence"}:
            sequence = np.asarray(self.sequence[indices], dtype=np.int64)
            for sequence_column in range(11):
                column = len(self.field_dims) - 11 + sequence_column
                values = sequence[:, sequence_column]
                if sequence_column in {0, 1, 2, 3, 4, 6, 8}:
                    encoded[:, column] = (
                        np.where(values >= 0, values + 1, 0) + self.offsets[column]
                    )
                else:
                    encoded[:, column] = values + 1 + self.offsets[column]
        if self.time_features:
            hours, weekdays = recurring_time_fields(
                rows.time_ms[indices], rows.date[indices]
            )
            encoded[:, -2] = hours + 1 + self.offsets[-2]
            encoded[:, -1] = weekdays + 1 + self.offsets[-1]
        return encoded


class SparseFM(nn.Module):
    def __init__(
        self,
        dimension: int,
        rank: int,
        unknown_offsets: np.ndarray,
        seed: int,
        latent_init_std: float = 0.01,
        neutral_unknown_init: bool = True,
    ):
        super().__init__()
        torch.manual_seed(seed)
        self.latent = nn.Embedding(dimension, rank, sparse=True)
        self.linear = nn.Embedding(dimension, 1, sparse=True)
        nn.init.normal_(self.latent.weight, mean=0.0, std=latent_init_std)
        nn.init.zeros_(self.linear.weight)
        if neutral_unknown_init:
            with torch.no_grad():
                unknown_indices = torch.from_numpy(unknown_offsets)
                self.latent.weight.index_fill_(0, unknown_indices, 0.0)
                self.linear.weight.index_fill_(0, unknown_indices, 0.0)

    def forward(self, fields: torch.Tensor) -> torch.Tensor:
        embeddings = self.latent(fields)
        summed = embeddings.sum(dim=1)
        interactions = 0.5 * (
            (summed * summed).sum(dim=1) - (embeddings * embeddings).sum(dim=(1, 2))
        )
        return self.linear(fields).sum(dim=1).squeeze(1) + interactions


class FunnelFM(SparseFM):
    """Shared FM representation for impression->click->long-view modeling."""

    def __init__(
        self,
        dimension: int,
        rank: int,
        unknown_offsets: np.ndarray,
        seed: int,
        latent_init_std: float = 0.01,
    ):
        super().__init__(dimension, rank, unknown_offsets, seed, latent_init_std)
        self.click_linear = nn.Embedding(dimension, 1, sparse=True)
        nn.init.zeros_(self.click_linear.weight)
        with torch.no_grad():
            self.click_linear.weight.index_fill_(
                0, torch.from_numpy(unknown_offsets), 0.0
            )

    def funnel_logits(
        self, fields: torch.Tensor
    ) -> tuple[torch.Tensor, torch.Tensor]:
        embeddings = self.latent(fields)
        summed = embeddings.sum(dim=1)
        interactions = 0.5 * (
            (summed * summed).sum(dim=1)
            - (embeddings * embeddings).sum(dim=(1, 2))
        )
        conditional_long_view = (
            self.linear(fields).sum(dim=1).squeeze(1) + interactions
        )
        click = self.click_linear(fields).sum(dim=1).squeeze(1) + interactions
        return click, conditional_long_view

    def forward(self, fields: torch.Tensor) -> torch.Tensor:
        click, conditional_long_view = self.funnel_logits(fields)
        return F.logsigmoid(click) + F.logsigmoid(conditional_long_view)


class WideCrossFM(SparseFM):
    """Content FM plus explicit cross fields that contribute only linearly."""

    def __init__(
        self,
        dimension: int,
        rank: int,
        base_field_count: int,
        unknown_offsets: np.ndarray,
        seed: int,
        latent_init_std: float = 0.01,
    ):
        super().__init__(dimension, rank, unknown_offsets, seed, latent_init_std)
        self.base_field_count = base_field_count

    def forward(self, fields: torch.Tensor) -> torch.Tensor:
        base_embeddings = self.latent(fields[:, : self.base_field_count])
        summed = base_embeddings.sum(dim=1)
        interactions = 0.5 * (
            (summed * summed).sum(dim=1)
            - (base_embeddings * base_embeddings).sum(dim=(1, 2))
        )
        return self.linear(fields).sum(dim=1).squeeze(1) + interactions


class BipartiteFM(SparseFM):
    """Sparse FM restricted to cross-group field interactions."""

    def __init__(
        self,
        dimension: int,
        rank: int,
        left_field_indices: tuple[int, ...],
        right_field_indices: tuple[int, ...],
        unknown_offsets: np.ndarray,
        seed: int,
        latent_init_std: float = 0.01,
    ):
        if not left_field_indices or not right_field_indices:
            raise ValueError("bipartite FM requires two nonempty field groups")
        if set(left_field_indices) & set(right_field_indices):
            raise ValueError("bipartite FM field groups must be disjoint")
        super().__init__(dimension, rank, unknown_offsets, seed, latent_init_std)
        self.register_buffer(
            "left_field_indices", torch.tensor(left_field_indices, dtype=torch.long)
        )
        self.register_buffer(
            "right_field_indices", torch.tensor(right_field_indices, dtype=torch.long)
        )

    def forward(self, fields: torch.Tensor) -> torch.Tensor:
        left = self.latent(fields.index_select(1, self.left_field_indices)).sum(dim=1)
        right = self.latent(fields.index_select(1, self.right_field_indices)).sum(dim=1)
        interactions = (left * right).sum(dim=1)
        return self.linear(fields).sum(dim=1).squeeze(1) + interactions


class DeepFM(nn.Module):
    """Sparse FM with a compact nonlinear tower over field embeddings."""

    def __init__(
        self,
        dimension: int,
        field_count: int,
        rank: int,
        hidden_dims: tuple[int, int],
        dropout: float,
        unknown_offsets: np.ndarray,
        seed: int,
        latent_init_std: float = 0.01,
    ):
        super().__init__()
        torch.manual_seed(seed)
        self.latent = nn.Embedding(dimension, rank, sparse=True)
        self.linear = nn.Embedding(dimension, 1, sparse=True)
        nn.init.normal_(self.latent.weight, mean=0.0, std=latent_init_std)
        nn.init.zeros_(self.linear.weight)
        first, second = hidden_dims
        self.deep = nn.Sequential(
            nn.Linear(field_count * rank, first),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(first, second),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(second, 1),
        )
        with torch.no_grad():
            unknown_indices = torch.from_numpy(unknown_offsets)
            self.latent.weight.index_fill_(0, unknown_indices, 0.0)
            self.linear.weight.index_fill_(0, unknown_indices, 0.0)

    def forward(self, fields: torch.Tensor) -> torch.Tensor:
        embeddings = self.latent(fields)
        summed = embeddings.sum(dim=1)
        interactions = 0.5 * (
            (summed * summed).sum(dim=1) - (embeddings * embeddings).sum(dim=(1, 2))
        )
        fm = self.linear(fields).sum(dim=1).squeeze(1) + interactions
        deep = self.deep(embeddings.flatten(start_dim=1)).squeeze(1)
        return fm + deep


class FieldAwareFM(nn.Module):
    """Field-aware FM with a distinct sparse vector for each target field."""

    def __init__(
        self,
        dimension: int,
        field_count: int,
        rank: int,
        unknown_offsets: np.ndarray,
        seed: int,
        latent_init_std: float = 0.01,
    ):
        super().__init__()
        torch.manual_seed(seed)
        self.field_count = field_count
        self.rank = rank
        self.latent = nn.Embedding(
            dimension, field_count * rank, sparse=True
        )
        self.linear = nn.Embedding(dimension, 1, sparse=True)
        nn.init.normal_(self.latent.weight, mean=0.0, std=latent_init_std)
        nn.init.zeros_(self.linear.weight)
        self.register_buffer(
            "pair_mask", torch.triu(torch.ones(field_count, field_count), diagonal=1)
        )
        with torch.no_grad():
            unknown_indices = torch.from_numpy(unknown_offsets)
            self.latent.weight.index_fill_(0, unknown_indices, 0.0)
            self.linear.weight.index_fill_(0, unknown_indices, 0.0)

    def forward(self, fields: torch.Tensor) -> torch.Tensor:
        embeddings = self.latent(fields).reshape(
            len(fields), self.field_count, self.field_count, self.rank
        )
        pair_scores = (embeddings * embeddings.transpose(1, 2)).sum(dim=3)
        interactions = (pair_scores * self.pair_mask).sum(dim=(1, 2))
        return self.linear(fields).sum(dim=1).squeeze(1) + interactions


def predict(
    model: nn.Module,
    rows: CachedRows,
    encoder: Encoder,
    indices: np.ndarray,
    batch_size: int,
) -> np.ndarray:
    output = np.empty(len(indices), dtype=np.float32)
    model.eval()
    with torch.no_grad():
        for start in range(0, len(indices), batch_size):
            batch_indices = indices[start : start + batch_size]
            fields = torch.from_numpy(encoder.encode(rows, batch_indices))
            output[start : start + len(batch_indices)] = model(fields).numpy()
    return output


def same_impression_pairs(
    rows: CachedRows,
    train_indices: np.ndarray,
    max_positives: int,
    seed: int,
) -> tuple[np.ndarray, np.ndarray, dict[str, int]]:
    """Sample positive/negative pairs only within a user/timestamp batch."""
    if max_positives <= 0:
        raise ValueError("same-impression pair cap must be positive")
    users = np.asarray(rows.user[train_indices], dtype=np.int32)
    times = np.asarray(rows.time_ms[train_indices], dtype=np.int64)
    labels = np.asarray(rows.label[train_indices], dtype=np.uint8)
    if np.any(users[1:] < users[:-1]):
        raise ValueError("training cache is not grouped by user")
    if np.any((users[1:] == users[:-1]) & (times[1:] < times[:-1])):
        raise ValueError("training cache has a per-user timestamp inversion")
    starts = np.r_[
        0,
        np.flatnonzero((users[1:] != users[:-1]) | (times[1:] != times[:-1])) + 1,
    ]
    ends = np.r_[starts[1:], len(train_indices)]
    group_size = ends - starts
    positive_count = np.add.reduceat(labels.astype(np.int64), starts)
    negative_count = group_size - positive_count
    usable = (positive_count > 0) & (negative_count > 0)
    pair_count = int(np.minimum(positive_count[usable], max_positives).sum())
    positive_rows = np.empty(pair_count, dtype=np.int64)
    negative_rows = np.empty(pair_count, dtype=np.int64)
    rng = np.random.default_rng(seed)
    cursor = 0
    for start, end, positives, is_usable in zip(
        starts, ends, positive_count, usable
    ):
        if not is_usable:
            continue
        local = np.arange(start, end, dtype=np.int64)
        positive = local[labels[start:end] == 1]
        negative = local[labels[start:end] == 0]
        take = min(len(positive), max_positives)
        if len(positive) > take:
            positive = rng.choice(positive, size=take, replace=False)
        chosen_negative = rng.choice(negative, size=take, replace=True)
        positive_rows[cursor : cursor + take] = train_indices[positive]
        negative_rows[cursor : cursor + take] = train_indices[chosen_negative]
        cursor += take
    if cursor != pair_count:
        raise RuntimeError(f"pair construction mismatch: {cursor} != {pair_count}")
    return positive_rows, negative_rows, {
        "impression_batches": int(len(starts)),
        "usable_impression_batches": int(usable.sum()),
        "pairs": pair_count,
        "max_positives_per_impression": max_positives,
    }


def within_user_pairs(
    rows: CachedRows,
    train_indices: np.ndarray,
    max_positives: int,
    seed: int,
) -> tuple[np.ndarray, np.ndarray, dict[str, int]]:
    """Sample long-view/non-long-view pairs across each user's train history."""
    if max_positives <= 0:
        raise ValueError("within-user pair cap must be positive")
    users = np.asarray(rows.user[train_indices], dtype=np.int32)
    labels = np.asarray(rows.label[train_indices], dtype=np.uint8)
    # Cache layout is an implementation detail: the 1K cache happens to be
    # grouped by user while the deterministic 27K sample is not.  Group a
    # stable view locally so pair semantics remain identical across caches and
    # keep returning original row indices for the encoder.
    order = np.argsort(users, kind="stable")
    grouped_indices = train_indices[order]
    users = users[order]
    labels = labels[order]
    starts = np.r_[0, np.flatnonzero(users[1:] != users[:-1]) + 1]
    ends = np.r_[starts[1:], len(train_indices)]
    positive_count = np.add.reduceat(labels.astype(np.int64), starts)
    group_size = ends - starts
    negative_count = group_size - positive_count
    usable = (positive_count > 0) & (negative_count > 0)
    pair_count = int(np.minimum(positive_count[usable], max_positives).sum())
    positive_rows = np.empty(pair_count, dtype=np.int64)
    negative_rows = np.empty(pair_count, dtype=np.int64)
    rng = np.random.default_rng(seed)
    cursor = 0
    for start, end, is_usable in zip(starts, ends, usable):
        if not is_usable:
            continue
        local = np.arange(start, end, dtype=np.int64)
        positive = local[labels[start:end] == 1]
        negative = local[labels[start:end] == 0]
        take = min(len(positive), max_positives)
        if len(positive) > take:
            positive = rng.choice(positive, size=take, replace=False)
        chosen_negative = rng.choice(negative, size=take, replace=True)
        positive_rows[cursor : cursor + take] = grouped_indices[positive]
        negative_rows[cursor : cursor + take] = grouped_indices[chosen_negative]
        cursor += take
    if cursor != pair_count:
        raise RuntimeError(f"pair construction mismatch: {cursor} != {pair_count}")
    return positive_rows, negative_rows, {
        "users": int(len(starts)),
        "usable_users": int(usable.sum()),
        "pairs": pair_count,
        "max_positives_per_user": max_positives,
    }


def within_user_hard_pairs(
    rows: CachedRows,
    train_indices: np.ndarray,
    train_scores: np.ndarray,
    max_positives: int,
) -> tuple[np.ndarray, np.ndarray, dict[str, object]]:
    """Pair each user's lowest-scored positives with highest-scored negatives."""
    if max_positives <= 0:
        raise ValueError("within-user hard-pair cap must be positive")
    if len(train_scores) != len(train_indices):
        raise ValueError("hard-pair training score length mismatch")
    users = np.asarray(rows.user[train_indices], dtype=np.int32)
    labels = np.asarray(rows.label[train_indices], dtype=np.uint8)
    scores = np.asarray(train_scores, dtype=np.float32)
    if not np.isfinite(scores).all():
        raise ValueError("hard-pair training scores must be finite")
    order = np.argsort(users, kind="stable")
    grouped_indices = train_indices[order]
    users = users[order]
    labels = labels[order]
    scores = scores[order]
    starts = np.r_[0, np.flatnonzero(users[1:] != users[:-1]) + 1]
    ends = np.r_[starts[1:], len(train_indices)]
    positive_count = np.add.reduceat(labels.astype(np.int64), starts)
    group_size = ends - starts
    negative_count = group_size - positive_count
    usable = (positive_count > 0) & (negative_count > 0)
    take_count = np.minimum.reduce(
        [
            positive_count[usable],
            negative_count[usable],
            np.full(int(usable.sum()), max_positives, dtype=np.int64),
        ]
    )
    pair_count = int(take_count.sum())
    positive_rows = np.empty(pair_count, dtype=np.int64)
    negative_rows = np.empty(pair_count, dtype=np.int64)
    cursor = 0
    for start, end, is_usable in zip(starts, ends, usable):
        if not is_usable:
            continue
        local = np.arange(start, end, dtype=np.int64)
        positive = local[labels[start:end] == 1]
        negative = local[labels[start:end] == 0]
        take = min(len(positive), len(negative), max_positives)
        positive_order = np.argsort(scores[positive], kind="stable")[:take]
        negative_order = np.argsort(scores[negative], kind="stable")[-take:][::-1]
        positive_rows[cursor : cursor + take] = grouped_indices[
            positive[positive_order]
        ]
        negative_rows[cursor : cursor + take] = grouped_indices[
            negative[negative_order]
        ]
        cursor += take
    if cursor != pair_count:
        raise RuntimeError(f"hard-pair construction mismatch: {cursor} != {pair_count}")
    return positive_rows, negative_rows, {
        "users": int(len(starts)),
        "usable_users": int(usable.sum()),
        "pairs": pair_count,
        "max_positives_per_user": max_positives,
        "positive_rule": "lowest_parent_score",
        "negative_rule": "highest_parent_score",
    }


def validate_checkpoint_metadata(
    checkpoint: dict[str, object],
    encoder: Encoder,
    args: argparse.Namespace,
    bounds: dict[str, tuple[int, int]],
) -> None:
    expected_scalars = {
        "feature_set": args.feature_set,
        "model_type": args.model_type,
        "split_mode": args.split_mode,
        "seed": args.seed,
        "min_video_count": args.min_video_count,
        "min_author_count": args.min_author_count,
        "time_features": args.time_features,
        "legacy_random_unknown_init": args.legacy_random_unknown_init,
        "epoch_order": args.epoch_order,
    }
    for key, expected in expected_scalars.items():
        if key.startswith("min_"):
            actual = checkpoint.get(key, 1)
        elif key == "time_features":
            actual = checkpoint.get(key, False)
        elif key == "legacy_random_unknown_init":
            actual = checkpoint.get(key, False)
        elif key == "epoch_order":
            actual = checkpoint.get(key, "random")
        else:
            actual = checkpoint.get(key)
        if actual != expected:
            raise ValueError(
                f"checkpoint {key} mismatch: {actual!r} != {expected!r}"
            )
    if checkpoint.get("split_bounds") != bounds:
        raise ValueError("checkpoint split bounds mismatch")
    if not np.array_equal(checkpoint.get("field_dims"), encoder.field_dims):
        raise ValueError("checkpoint field dimensions mismatch")
    if not np.array_equal(checkpoint.get("offsets"), encoder.offsets):
        raise ValueError("checkpoint offsets mismatch")


def robustness_slices(
    rows: CachedRows,
    activity_reference_indices: np.ndarray,
    valid_indices: np.ndarray,
    scores: np.ndarray,
) -> dict[str, object]:
    """Score fixed slices using a declared activity-reference population."""
    activity = np.bincount(
        np.asarray(rows.user[activity_reference_indices], dtype=np.int64),
        minlength=rows.manifest["user_count"],
    )
    valid_users = np.asarray(rows.user[valid_indices], dtype=np.int64)
    counts = activity[valid_users]
    positive = counts[counts > 0]
    cut1, cut2 = np.quantile(positive, [1 / 3, 2 / 3]) if len(positive) else (0, 0)
    valid_dates = np.asarray(rows.date[valid_indices], dtype=np.int32)
    dates = np.unique(valid_dates)
    midpoint = len(dates) // 2
    masks = {
        "early_dates": np.isin(valid_dates, dates[:midpoint]),
        "late_dates": np.isin(valid_dates, dates[midpoint:]),
        "cold_or_low_activity": counts <= cut1,
        "medium_activity": (counts > cut1) & (counts <= cut2),
        "high_activity": counts > cut2,
    }
    result: dict[str, object] = {"activity_cutpoints": [float(cut1), float(cut2)]}
    labels = np.asarray(rows.label[valid_indices], dtype=np.uint8)
    for name, mask in masks.items():
        selected = np.flatnonzero(mask)
        result[name] = fast_evaluate(valid_users[selected], labels[selected], scores[selected])
    result["minimum_primary"] = min(
        metric["primary"] for metric in result.values() if isinstance(metric, dict)
    )
    return result


def within_user_percentile_rank(
    users: np.ndarray, scores: np.ndarray
) -> np.ndarray:
    """Scale each user's scores to deterministic [0, 1] ordinal ranks."""
    transformed = np.empty(len(scores), dtype=np.float64)
    grouped = np.argsort(users, kind="stable")
    grouped_users = users[grouped]
    starts = np.r_[0, np.flatnonzero(grouped_users[1:] != grouped_users[:-1]) + 1]
    ends = np.r_[starts[1:], len(grouped)]
    for start, end in zip(starts, ends):
        indices = grouped[start:end]
        order = np.argsort(scores[indices], kind="stable")
        ranks = np.empty(len(indices), dtype=np.float64)
        ranks[order] = np.arange(len(indices), dtype=np.float64)
        transformed[indices] = ranks / max(len(indices) - 1, 1)
    return transformed


def aggregate_prediction_members(
    users: np.ndarray, members: list[np.ndarray], method: str
) -> np.ndarray:
    """Combine fixed prediction members without searching weights or subsets."""
    if len(members) < 2:
        raise ValueError("at least two prediction members are required")
    arrays = [np.asarray(member) for member in members]
    if any(array.ndim != 1 or len(array) != len(users) for array in arrays):
        raise ValueError("ensemble prediction length mismatch")
    if any(not np.isfinite(array).all() for array in arrays):
        raise ValueError("ensemble predictions must be finite")
    if method == "user_rank_mean":
        transformed = [within_user_percentile_rank(users, array) for array in arrays]
    elif method == "raw_mean":
        transformed = arrays
    else:
        raise ValueError(f"unknown prediction aggregation: {method}")
    return np.mean(transformed, axis=0, dtype=np.float64)


def slot_preserving_profile_blend(
    users: np.ndarray,
    parent_scores: np.ndarray,
    profile_scores: np.ndarray,
    supported: np.ndarray,
) -> np.ndarray:
    """Give frozen profile similarity one vote without disturbing unsupported rows.

    For each user, supported candidates exchange only the parent percentile
    slots they already occupy. Unsupported candidates keep their exact parent
    slots. The returned score is one equal parent vote and one reordered vote.
    """
    users = np.asarray(users, dtype=np.int64)
    parent_scores = np.asarray(parent_scores, dtype=np.float64)
    profile_scores = np.asarray(profile_scores, dtype=np.float64)
    supported = np.asarray(supported, dtype=np.bool_)
    if not (
        users.ndim
        == parent_scores.ndim
        == profile_scores.ndim
        == supported.ndim
        == 1
        and len(users)
        == len(parent_scores)
        == len(profile_scores)
        == len(supported)
    ):
        raise ValueError("profile blend arrays must be aligned one-dimensional arrays")
    if not np.isfinite(parent_scores).all() or not np.isfinite(profile_scores).all():
        raise ValueError("profile blend scores must be finite")
    parent_rank = within_user_percentile_rank(users, parent_scores)
    profile_vote = parent_rank.copy()
    grouped = np.argsort(users, kind="stable")
    grouped_users = users[grouped]
    starts = np.r_[0, np.flatnonzero(grouped_users[1:] != grouped_users[:-1]) + 1]
    ends = np.r_[starts[1:], len(grouped)]
    for start, end in zip(starts, ends):
        indices = grouped[start:end]
        eligible = indices[supported[indices]]
        if len(eligible) < 2:
            continue
        slots = np.sort(parent_rank[eligible])
        order = np.argsort(profile_scores[eligible], kind="stable")
        profile_vote[eligible[order]] = slots
    return (parent_rank + profile_vote) / 2.0


def frozen_video_profile_scores(
    rows: CachedRows,
    train_indices: np.ndarray,
    score_indices: np.ndarray,
    checkpoint: dict[str, object],
    batch_size: int,
) -> tuple[np.ndarray, np.ndarray, dict[str, int]]:
    """Score candidates by cosine to a training-positive frozen video profile."""
    if batch_size <= 0:
        raise ValueError("video profile batch size must be positive")
    required = {"latent", "field_dims", "offsets", "seen_video"}
    missing = required.difference(checkpoint)
    if missing:
        raise ValueError(f"video profile checkpoint missing keys: {sorted(missing)}")
    latent = checkpoint["latent"]
    if not isinstance(latent, torch.Tensor) or latent.ndim != 2:
        raise ValueError("video profile checkpoint latent must be a rank-2 tensor")
    field_dims = np.asarray(checkpoint["field_dims"], dtype=np.int64)
    offsets = np.asarray(checkpoint["offsets"], dtype=np.int64)
    seen_video = np.asarray(checkpoint["seen_video"], dtype=np.bool_)
    if len(field_dims) < 2 or len(offsets) < 2:
        raise ValueError("video profile checkpoint has no video field")
    video_count = int(field_dims[1] - 1)
    if video_count != rows.manifest["video_count"] or len(seen_video) != video_count:
        raise ValueError("video profile checkpoint video dimension mismatch")
    video_start = int(offsets[1]) + 1
    video_end = video_start + video_count
    if video_end > latent.shape[0]:
        raise ValueError("video profile checkpoint latent is shorter than video field")
    video_vectors = latent[video_start:video_end]
    if video_vectors.device.type != "cpu" or video_vectors.dtype != torch.float32:
        video_vectors = video_vectors.detach().to(device="cpu", dtype=torch.float32)
    else:
        video_vectors = video_vectors.detach()
    with torch.no_grad():
        for start in range(0, video_count, batch_size):
            chunk = video_vectors[start : start + batch_size]
            norms = torch.linalg.vector_norm(chunk, dim=1, keepdim=True).clamp_min_(1e-12)
            chunk.div_(norms)
        user_count = int(rows.manifest["user_count"])
        profiles = torch.zeros((user_count, latent.shape[1]), dtype=torch.float32)
        positive_counts = torch.zeros(user_count, dtype=torch.int64)
        used_positive_exposures = 0
        for start in range(0, len(train_indices), batch_size):
            batch_indices = train_indices[start : start + batch_size]
            labels = np.asarray(rows.label[batch_indices], dtype=np.uint8)
            selected = labels == 1
            if not selected.any():
                continue
            users = np.asarray(rows.user[batch_indices[selected]], dtype=np.int64)
            videos = np.asarray(rows.video[batch_indices[selected]], dtype=np.int64)
            selected_seen = seen_video[videos]
            if not selected_seen.any():
                continue
            users_tensor = torch.from_numpy(users[selected_seen])
            videos_tensor = torch.from_numpy(videos[selected_seen])
            profiles.index_add_(0, users_tensor, video_vectors[videos_tensor])
            positive_counts.index_add_(
                0, users_tensor, torch.ones(len(users_tensor), dtype=torch.int64)
            )
            used_positive_exposures += len(users_tensor)
        profile_norms = torch.linalg.vector_norm(profiles, dim=1, keepdim=True)
        profile_users = profile_norms[:, 0] > 0
        profiles[profile_users] = profiles[profile_users] / profile_norms[profile_users]
        profile_users_numpy = profile_users.numpy()
        output = np.zeros(len(score_indices), dtype=np.float32)
        supported = np.zeros(len(score_indices), dtype=np.bool_)
        for start in range(0, len(score_indices), batch_size):
            batch_indices = score_indices[start : start + batch_size]
            users = np.asarray(rows.user[batch_indices], dtype=np.int64)
            videos = np.asarray(rows.video[batch_indices], dtype=np.int64)
            available = seen_video[videos] & profile_users_numpy[users]
            if not available.any():
                continue
            users_tensor = torch.from_numpy(users[available])
            videos_tensor = torch.from_numpy(videos[available])
            similarities = (profiles[users_tensor] * video_vectors[videos_tensor]).sum(dim=1)
            output[start : start + len(batch_indices)][available] = similarities.numpy()
            supported[start : start + len(batch_indices)][available] = True
    metadata = {
        "positive_exposures": int(used_positive_exposures),
        "profile_users": int((positive_counts > 0).sum().item()),
        "supported_rows": int(supported.sum()),
        "supported_users": int(np.unique(np.asarray(rows.user[score_indices])[supported]).size),
    }
    return output, supported, metadata


LAMBDAMART_FEATURE_NAMES = (
    "log1p_duration",
    "tab",
    "primary_tag",
    "upload_type",
    "video_type",
    "prior_user_count_log2",
    "prior_user_long_view_rate_21",
    "prior_user_strong_feedback_count_log2",
    "prior_user_hate_count_log2",
    "prior_user_tag_count_log2",
    "prior_user_tag_long_view_rate_21",
    "current_tag_matches_last_positive_tag",
    "last_positive_tag",
    "prior_day_video_count_log2",
    "prior_day_video_long_view_rate_21",
    "prior_day_author_count_log2",
    "prior_day_author_long_view_rate_21",
    "prior_user_author_count_log2",
    "prior_user_author_long_view_rate_21",
    "prior_user_video_count_log2",
    "prior_user_video_long_view_rate_21",
)
LAMBDAMART_CATEGORICAL_FEATURES = (1, 2, 3, 4, 12)


def load_declared_split_array(
    cache_dir: Path, manifest_name: str, split_mode: str, expected_columns: int
) -> np.ndarray:
    """Load one already-audited causal feature sidecar for a declared split."""
    manifest_path = cache_dir / manifest_name
    manifest = json.loads(manifest_path.read_text())
    if split_mode not in manifest.get("splits", {}):
        raise ValueError(f"{manifest_name} has no split {split_mode}")
    values = np.load(cache_dir / manifest["splits"][split_mode]["path"], mmap_mode="r")
    if values.ndim != 2 or values.shape[1] != expected_columns:
        raise ValueError(f"{manifest_name} feature shape mismatch: {values.shape}")
    return values


def lambdamart_dense_features(
    rows: CachedRows,
    indices: np.ndarray,
    history: np.ndarray,
    item_history: np.ndarray,
    entity_history: np.ndarray,
) -> np.ndarray:
    """Materialize the frozen bounded causal tree feature matrix."""
    indices = np.asarray(indices, dtype=np.int64)
    if not (
        len(history) == len(item_history) == len(entity_history) == len(rows.user)
    ):
        raise ValueError("LambdaMART sidecars do not align with cache rows")
    features = np.empty((len(indices), len(LAMBDAMART_FEATURE_NAMES)), dtype=np.float32)
    features[:, 0] = np.log1p(
        np.maximum(np.asarray(rows.duration[indices], dtype=np.float32), 0.0)
    )
    features[:, 1] = np.asarray(rows.tab[indices], dtype=np.float32)
    features[:, 2] = np.asarray(rows.tag[indices], dtype=np.float32) + 1.0
    features[:, 3] = np.asarray(rows.upload_type[indices], dtype=np.float32) + 1.0
    features[:, 4] = np.asarray(rows.video_type[indices], dtype=np.float32) + 1.0
    features[:, 5:13] = np.asarray(history[indices], dtype=np.float32)
    features[:, 12] += 1.0
    features[:, 13:17] = np.asarray(item_history[indices], dtype=np.float32)
    features[:, 17:21] = np.asarray(entity_history[indices], dtype=np.float32)
    if not np.isfinite(features).all():
        raise ValueError("LambdaMART features must be finite")
    return features


def lambdamart_grouped_matrix(
    rows: CachedRows,
    indices: np.ndarray,
    history: np.ndarray,
    item_history: np.ndarray,
    entity_history: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return stable user-grouped features, labels, group sizes, and order."""
    indices = np.asarray(indices, dtype=np.int64)
    users = np.asarray(rows.user[indices], dtype=np.int64)
    order = np.argsort(users, kind="stable")
    ordered_indices = indices[order]
    ordered_users = users[order]
    group_sizes = np.bincount(
        ordered_users, minlength=int(rows.manifest["user_count"])
    )
    group_sizes = bounded_query_groups(group_sizes[group_sizes > 0], 10_000)
    if int(group_sizes.sum()) != len(indices):
        raise ValueError("LambdaMART group sizes do not cover all rows")
    features = lambdamart_dense_features(
        rows, ordered_indices, history, item_history, entity_history
    )
    labels = np.asarray(rows.label[ordered_indices], dtype=np.int32)
    return features, labels, group_sizes, order


def bounded_query_groups(group_sizes: np.ndarray, maximum: int) -> np.ndarray:
    """Split an oversized user's stable rows without mixing or dropping users."""
    if maximum <= 0:
        raise ValueError("maximum query size must be positive")
    raw = np.asarray(group_sizes, dtype=np.int64)
    if raw.ndim != 1 or np.any(raw <= 0):
        raise ValueError("query group sizes must be positive")
    bounded: list[int] = []
    for size in raw:
        remaining = int(size)
        while remaining > maximum:
            bounded.append(maximum)
            remaining -= maximum
        if remaining:
            bounded.append(remaining)
    result = np.asarray(bounded, dtype=np.int32)
    if int(result.sum()) != int(raw.sum()) or np.any(result > maximum):
        raise AssertionError("bounded query split did not preserve rows")
    return result


def restore_grouped_predictions(order: np.ndarray, grouped_scores: np.ndarray) -> np.ndarray:
    """Restore predictions from stable user-grouped order to cache-index order."""
    order = np.asarray(order, dtype=np.int64)
    grouped_scores = np.asarray(grouped_scores, dtype=np.float64)
    if order.ndim != 1 or grouped_scores.ndim != 1 or len(order) != len(grouped_scores):
        raise ValueError("grouped prediction arrays must align")
    restored = np.empty(len(order), dtype=np.float64)
    restored[order] = grouped_scores
    return restored


def high_activity_specialist_scores(
    users: np.ndarray,
    activity: np.ndarray,
    members: list[np.ndarray],
    method: str,
    cutoff: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Route the last member only into the fixed upper-tertile activity cohort."""
    users = np.asarray(users, dtype=np.int64)
    activity = np.asarray(activity, dtype=np.int64)
    if activity.ndim != 1 or np.any(users < 0) or np.any(users >= len(activity)):
        raise ValueError("routing activity does not cover every user")
    if len(members) < 4:
        raise ValueError("high-activity specialist requires three base members and one specialist")
    route = activity[users] > cutoff
    base = aggregate_prediction_members(users, members[:-1], method)
    specialist = aggregate_prediction_members(users, members, method)
    return np.where(route, specialist, base), route


def high_activity_fallback_scores(
    users: np.ndarray,
    activity: np.ndarray,
    members: list[np.ndarray],
    method: str,
    cutoff: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Route the final member alone into the fixed upper-tertile cohort."""
    users = np.asarray(users, dtype=np.int64)
    activity = np.asarray(activity, dtype=np.int64)
    if activity.ndim != 1 or np.any(users < 0) or np.any(users >= len(activity)):
        raise ValueError("routing activity does not cover every user")
    if len(members) != 2:
        raise ValueError("high-activity fallback requires one base and one fallback")
    arrays = [np.asarray(member, dtype=np.float64) for member in members]
    if any(array.ndim != 1 or len(array) != len(users) for array in arrays):
        raise ValueError("ensemble prediction length mismatch")
    if any(not np.isfinite(array).all() for array in arrays):
        raise ValueError("ensemble predictions must be finite")
    route = activity[users] > cutoff
    if method == "user_rank_mean":
        base, fallback = (
            within_user_percentile_rank(users, array) for array in arrays
        )
    elif method == "raw_mean":
        base, fallback = arrays
    else:
        raise ValueError(f"unknown prediction aggregation: {method}")
    return np.where(route, fallback, base), route


def high_activity_equal_blend_scores(
    users: np.ndarray,
    activity: np.ndarray,
    members: list[np.ndarray],
    method: str,
    cutoff: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Blend base and fallback equally only in the upper-tertile cohort."""
    users = np.asarray(users, dtype=np.int64)
    activity = np.asarray(activity, dtype=np.int64)
    if activity.ndim != 1 or np.any(users < 0) or np.any(users >= len(activity)):
        raise ValueError("routing activity does not cover every user")
    if len(members) != 2:
        raise ValueError("high-activity blend requires one base and one fallback")
    arrays = [np.asarray(member, dtype=np.float64) for member in members]
    if any(array.ndim != 1 or len(array) != len(users) for array in arrays):
        raise ValueError("ensemble prediction length mismatch")
    if any(not np.isfinite(array).all() for array in arrays):
        raise ValueError("ensemble predictions must be finite")
    route = activity[users] > cutoff
    if method == "user_rank_mean":
        base, fallback = (
            within_user_percentile_rank(users, array) for array in arrays
        )
    elif method == "raw_mean":
        base, fallback = arrays
    else:
        raise ValueError(f"unknown prediction aggregation: {method}")
    blend = 0.5 * (base + fallback)
    return np.where(route, blend, base), route


def activity_upper_tertile(reference_users: np.ndarray, activity: np.ndarray) -> float:
    """Match the robustness slice's validation-row-weighted upper cutpoint."""
    reference_users = np.asarray(reference_users, dtype=np.int64)
    activity = np.asarray(activity, dtype=np.int64)
    if np.any(reference_users < 0) or np.any(reference_users >= len(activity)):
        raise ValueError("activity reference contains an uncovered user")
    positive = activity[reference_users]
    positive = positive[positive > 0]
    return float(np.quantile(positive, 2 / 3)) if len(positive) else 0.0


def user_balanced_weights(users: np.ndarray, alpha: float) -> np.ndarray:
    """Return mean-one row weights inverse to user frequency to `alpha`."""
    if not 0.0 <= alpha <= 1.0:
        raise ValueError("user balance alpha must be in [0, 1]")
    users = np.asarray(users, dtype=np.int64)
    if users.ndim != 1 or not len(users):
        raise ValueError("user balance requires a nonempty one-dimensional array")
    counts = np.bincount(users)
    weights = counts[users].astype(np.float64) ** (-alpha)
    weights /= weights.mean()
    return weights.astype(np.float32)


def balanced_positive_weight(labels: np.ndarray) -> float:
    """Return the negative-to-positive ratio for binary class-balanced BCE."""
    labels = np.asarray(labels, dtype=np.float64)
    if labels.ndim != 1 or not len(labels):
        raise ValueError("class balancing requires nonempty one-dimensional labels")
    if np.any((labels != 0) & (labels != 1)):
        raise ValueError("class balancing requires binary labels")
    positives = float(labels.sum())
    negatives = float(len(labels) - positives)
    if positives == 0 or negatives == 0:
        raise ValueError("class balancing requires both label classes")
    return negatives / positives


def fractional_epoch_order(order: np.ndarray, fraction: float) -> np.ndarray:
    """Return the deterministic prefix used for a fractional training epoch."""
    if not 0.0 < fraction <= 1.0:
        raise ValueError("--epoch-fraction must be in (0, 1]")
    if len(order) == 0:
        return order
    return order[: math.ceil(len(order) * fraction)]


def chronological_epoch_order(training_times: np.ndarray) -> np.ndarray:
    """Return row positions in stable global chronological order."""
    training_times = np.asarray(training_times, dtype=np.int64)
    if training_times.ndim != 1:
        raise ValueError("training timestamps must be one-dimensional")
    return np.argsort(training_times, kind="stable")


def remove_sparse_gradient_rows(
    parameter: torch.nn.Parameter, ranges: tuple[tuple[int, int], ...]
) -> int:
    """Remove selected embedding rows from a sparse optimizer update."""
    gradient = parameter.grad
    if gradient is None:
        return 0
    if not gradient.is_sparse:
        raise ValueError("identity freezing requires sparse embedding gradients")
    gradient = gradient.coalesce()
    rows = gradient.indices()[0]
    blocked = torch.zeros_like(rows, dtype=torch.bool)
    for start, end in ranges:
        if start < 0 or end < start or end > parameter.shape[0]:
            raise ValueError("invalid sparse-gradient freeze range")
        blocked |= (rows >= start) & (rows < end)
    keep = ~blocked
    parameter.grad = torch.sparse_coo_tensor(
        gradient.indices()[:, keep],
        gradient.values()[keep],
        gradient.shape,
        dtype=gradient.dtype,
        device=gradient.device,
    ).coalesce()
    return int(blocked.sum().item())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache-dir", type=Path, required=True)
    parser.add_argument("--split-mode", choices=tuple(SPLITS), default="official")
    parser.add_argument("--rank", type=int, default=16)
    parser.add_argument("--latent-init-std", type=float, default=0.01)
    parser.add_argument(
        "--model-type",
        choices=(
            "sparse_fm",
            "wide_cross_fm",
            "additive_tail_fm",
            "bipartite_fm",
            "funnel_fm",
            "deep_fm",
            "field_aware_fm",
        ),
        default="sparse_fm",
    )
    parser.add_argument(
        "--feature-set",
        choices=("base", "content", "cross", "history", "full_history", "item_history", "history_item", "history_item_behavior", "history_item_trend", "history_item_repeat", "history_item_repeat_author_behavior", "history_item_repeat_author_recency", "history_item_repeat_tag_affinity", "history_item_repeat_multitag_affinity", "history_item_repeat_sequence", "sequence", "multitag", "rich"),
        default="base",
    )
    parser.add_argument("--learning-rate", type=float, default=0.001)
    parser.add_argument("--min-video-count", type=int, default=1)
    parser.add_argument("--min-author-count", type=int, default=1)
    parser.add_argument("--dense-learning-rate", type=float, default=0.001)
    parser.add_argument("--deep-hidden-dims", nargs=2, type=int, default=(32, 16))
    parser.add_argument("--deep-dropout", type=float, default=0.1)
    parser.add_argument("--l2", type=float, default=0.0)
    parser.add_argument("--wide-cross-l2", type=float, default=0.0)
    parser.add_argument("--user-balance-alpha", type=float, default=0.0)
    parser.add_argument("--balance-positive-class", action="store_true")
    parser.add_argument("--time-features", action="store_true")
    parser.add_argument("--legacy-random-unknown-init", action="store_true")
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--epoch-fraction", type=float, default=1.0)
    parser.add_argument(
        "--epoch-order", choices=("random", "chronological"), default="random"
    )
    parser.add_argument("--freeze-identity-after-epoch", type=int, default=0)
    parser.add_argument("--patience", type=int, default=4)
    parser.add_argument("--batch-size", type=int, default=65536)
    parser.add_argument("--predict-batch-size", type=int, default=262144)
    parser.add_argument("--threads", type=int, default=16)
    parser.add_argument("--seed", type=int, default=2027)
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--model-out", type=Path)
    parser.add_argument("--predictions-out", type=Path)
    parser.add_argument("--prediction-files", nargs="+", type=Path, default=[])
    parser.add_argument("--embedding-profile-checkpoint", type=Path)
    parser.add_argument("--embedding-profile-parent-predictions", type=Path)
    parser.add_argument("--lambdamart", action="store_true")
    parser.add_argument("--lambdamart-parent-predictions", type=Path)
    parser.add_argument(
        "--prediction-aggregation",
        choices=("user_rank_mean", "raw_mean"),
        default="user_rank_mean",
    )
    parser.add_argument(
        "--prediction-routing",
        choices=(
            "none",
            "high_activity_last_member",
            "high_activity_last_member_only",
            "high_activity_equal_blend",
        ),
        default="none",
    )
    parser.add_argument("--checkpoint-in", type=Path)
    parser.add_argument("--pairwise-epochs", type=int, default=0)
    parser.add_argument("--pairwise-learning-rate", type=float, default=0.0002)
    parser.add_argument("--pairwise-batch-size", type=int, default=32768)
    parser.add_argument("--pairwise-max-positives", type=int, default=5)
    parser.add_argument(
        "--pairwise-scope",
        choices=("same_impression", "within_user"),
        default="same_impression",
    )
    parser.add_argument(
        "--pairwise-negative-sampling",
        choices=("random", "hard"),
        default="random",
    )
    parser.add_argument("--pairwise-select-best", action="store_true")
    parser.add_argument("--pairwise-patience", type=int, default=0)
    args = parser.parse_args()
    profile_mode = (
        args.embedding_profile_checkpoint is not None
        or args.embedding_profile_parent_predictions is not None
    )
    if profile_mode and (
        args.embedding_profile_checkpoint is None
        or args.embedding_profile_parent_predictions is None
    ):
        raise ValueError(
            "video profile mode requires both checkpoint and parent predictions"
        )
    if profile_mode and args.prediction_files:
        raise ValueError("video profile mode cannot also use prediction files")
    if profile_mode and args.epochs != 0:
        raise ValueError("video profile mode requires --epochs 0")
    if args.lambdamart != (args.lambdamart_parent_predictions is not None):
        raise ValueError("LambdaMART mode requires exactly one parent prediction archive")
    if args.lambdamart and args.epochs != 0:
        raise ValueError("LambdaMART mode requires --epochs 0")
    if args.lambdamart and (profile_mode or args.prediction_files or args.checkpoint_in):
        raise ValueError("LambdaMART mode cannot be combined with another scoring mode")
    if args.lambdamart and args.model_out is None:
        raise ValueError("LambdaMART mode requires --model-out")
    if args.checkpoint_in is not None and args.epochs != 0:
        raise ValueError("--checkpoint-in requires --epochs 0")
    if args.latent_init_std <= 0:
        raise ValueError("--latent-init-std must be positive")
    if not 0.0 < args.epoch_fraction <= 1.0:
        raise ValueError("--epoch-fraction must be in (0, 1]")
    if args.freeze_identity_after_epoch < 0:
        raise ValueError("--freeze-identity-after-epoch must be nonnegative")
    if args.freeze_identity_after_epoch and args.model_type not in {
        "sparse_fm",
        "wide_cross_fm",
        "additive_tail_fm",
        "bipartite_fm",
    }:
        raise ValueError("identity freezing requires a single-head sparse FM")
    if args.legacy_random_unknown_init and args.model_type != "sparse_fm":
        raise ValueError("legacy random unknown initialization requires sparse_fm")
    if (
        args.checkpoint_in is None
        and args.epochs <= 0
        and not profile_mode
        and not args.lambdamart
    ):
        raise ValueError("scratch training requires positive --epochs")
    if args.pairwise_negative_sampling == "hard" and args.pairwise_scope != "within_user":
        raise ValueError("hard pair sampling requires --pairwise-scope within_user")
    if args.pairwise_select_best and args.pairwise_epochs <= 0:
        raise ValueError("--pairwise-select-best requires positive pairwise epochs")
    if args.pairwise_select_best and args.pairwise_patience <= 0:
        raise ValueError("--pairwise-select-best requires positive pairwise patience")
    if args.model_type == "funnel_fm" and args.pairwise_epochs:
        raise ValueError("funnel_fm does not support pairwise fine-tuning")
    if args.model_type == "funnel_fm" and args.balance_positive_class:
        raise ValueError("funnel_fm does not support positive class balancing")
    started = time.time()
    torch.set_num_threads(args.threads)
    rows = CachedRows(args.cache_dir)
    bounds = SPLITS[args.split_mode]
    train_indices = rows.indices(bounds["train"])
    # Expanded caches may retain denser rows for model fitting while locking
    # evaluation to a deterministic subset. Define robustness activity on the
    # same locked subset so slice membership remains comparable to the parent
    # cache; ordinary caches have no remainder sidecar and are unchanged.
    activity_reference_indices = rows.indices(bounds["train"], evaluation=True)
    valid_indices = rows.indices(bounds["valid"], evaluation=True)
    forward_indices = (
        rows.indices(bounds["forward"], evaluation=True)
        if "forward" in bounds
        else None
    )
    if args.lambdamart:
        import lightgbm as lgb

        parent_path = args.lambdamart_parent_predictions
        assert parent_path is not None and args.model_out is not None
        parent = np.load(parent_path)
        if "valid" not in parent.files or len(parent["valid"]) != len(valid_indices):
            raise ValueError("LambdaMART parent has no aligned validation predictions")
        history = load_declared_split_array(
            args.cache_dir, "history_manifest.json", args.split_mode, 8
        )
        item_history = load_declared_split_array(
            args.cache_dir, "item_history_manifest.json", args.split_mode, 4
        )
        entity_history = load_declared_split_array(
            args.cache_dir, "user_entity_history_manifest.json", args.split_mode, 4
        )
        train_features, train_labels, train_groups, train_order = (
            lambdamart_grouped_matrix(
                rows, train_indices, history, item_history, entity_history
            )
        )
        valid_features, valid_labels_grouped, valid_groups, valid_order = (
            lambdamart_grouped_matrix(
                rows, valid_indices, history, item_history, entity_history
            )
        )
        train_dataset = lgb.Dataset(
            train_features,
            label=train_labels,
            group=train_groups,
            feature_name=list(LAMBDAMART_FEATURE_NAMES),
            categorical_feature=list(LAMBDAMART_CATEGORICAL_FEATURES),
            free_raw_data=True,
        )
        train_user_count = int(
            np.unique(np.asarray(rows.user[train_indices], dtype=np.int32)).size
        )
        train_query_count = int(len(train_groups))
        valid_dataset = lgb.Dataset(
            valid_features,
            label=valid_labels_grouped,
            group=valid_groups,
            feature_name=list(LAMBDAMART_FEATURE_NAMES),
            categorical_feature=list(LAMBDAMART_CATEGORICAL_FEATURES),
            reference=train_dataset,
            free_raw_data=True,
        )
        lambdamart_parameters = {
            "objective": "lambdarank",
            "metric": "ndcg",
            "ndcg_eval_at": [5],
            "lambdarank_truncation_level": 5,
            "learning_rate": 0.05,
            "num_leaves": 31,
            "min_data_in_leaf": 1000,
            "max_bin": 63,
            "feature_fraction": 1.0,
            "bagging_fraction": 1.0,
            "bagging_freq": 0,
            "verbosity": 1,
            "num_threads": args.threads,
            "seed": args.seed,
            "data_random_seed": args.seed,
            "feature_fraction_seed": args.seed,
            "bagging_seed": args.seed,
            "deterministic": True,
            "force_col_wise": True,
        }
        booster = lgb.train(
            lambdamart_parameters,
            train_dataset,
            num_boost_round=200,
            valid_sets=[valid_dataset],
            valid_names=["valid"],
            callbacks=[lgb.early_stopping(20), lgb.log_evaluation(10)],
        )
        best_iteration = int(booster.best_iteration or 200)
        valid_tree_grouped = booster.predict(
            valid_features, num_iteration=best_iteration
        )
        valid_tree_scores = restore_grouped_predictions(
            valid_order, valid_tree_grouped
        )
        valid_users = np.asarray(rows.user[valid_indices], dtype=np.int32)
        valid_labels = np.asarray(rows.label[valid_indices], dtype=np.uint8)
        valid_scores = aggregate_prediction_members(
            valid_users,
            [np.asarray(parent["valid"]), valid_tree_scores],
            "user_rank_mean",
        )
        raw_tree_valid = fast_evaluate(valid_users, valid_labels, valid_tree_scores)
        booster.free_dataset()
        del train_dataset, valid_dataset, train_features, train_labels, train_groups
        del train_order, valid_features, valid_labels_grouped, valid_groups
        gc.collect()
        forward_scores = None
        raw_tree_forward = None
        if forward_indices is not None:
            if "forward" not in parent.files or len(parent["forward"]) != len(
                forward_indices
            ):
                raise ValueError("LambdaMART parent has no aligned forward predictions")
            (
                forward_features,
                forward_labels_grouped,
                forward_groups,
                forward_order,
            ) = lambdamart_grouped_matrix(
                rows, forward_indices, history, item_history, entity_history
            )
            forward_tree_grouped = booster.predict(
                forward_features, num_iteration=best_iteration
            )
            forward_tree_scores = restore_grouped_predictions(
                forward_order, forward_tree_grouped
            )
            forward_users = np.asarray(rows.user[forward_indices], dtype=np.int32)
            forward_labels = np.asarray(rows.label[forward_indices], dtype=np.uint8)
            forward_scores = aggregate_prediction_members(
                forward_users,
                [np.asarray(parent["forward"]), forward_tree_scores],
                "user_rank_mean",
            )
            raw_tree_forward = fast_evaluate(
                forward_users, forward_labels, forward_tree_scores
            )
            del forward_features, forward_labels_grouped, forward_groups
            gc.collect()
        args.model_out.parent.mkdir(parents=True, exist_ok=True)
        booster.save_model(str(args.model_out), num_iteration=best_iteration)
        importance = booster.feature_importance(
            importance_type="gain", iteration=best_iteration
        )
        result = {
            "benchmark": rows.manifest["benchmark"],
            "variant": "causal_dense_lambdamart_parent_rank_consensus",
            "split_mode": args.split_mode,
            "split_bounds": bounds,
            "parameters": lambdamart_parameters,
            "maximum_boost_rounds": 200,
            "early_stopping_rounds": 20,
            "best_iteration": best_iteration,
            "feature_names": list(LAMBDAMART_FEATURE_NAMES),
            "categorical_feature_indices": list(LAMBDAMART_CATEGORICAL_FEATURES),
            "feature_importance_gain": {
                name: float(value)
                for name, value in zip(LAMBDAMART_FEATURE_NAMES, importance)
            },
            "train_rows": int(len(train_indices)),
            "train_users": train_user_count,
            "train_queries": train_query_count,
            "maximum_query_rows": 10_000,
            "parent_predictions": str(parent_path),
            "parent_predictions_sha256": sha256_path(parent_path),
            "model_out": str(args.model_out),
            "model_out_sha256": sha256_path(args.model_out),
            "lightgbm_version": lgb.__version__,
            "raw_tree_valid": raw_tree_valid,
            "valid": fast_evaluate(valid_users, valid_labels, valid_scores),
            "robustness": robustness_slices(
                rows, activity_reference_indices, valid_indices, valid_scores
            ),
            "robustness_activity_reference_rows": int(len(activity_reference_indices)),
            "elapsed_seconds": time.time() - started,
            "public_test_evaluated": False,
        }
        if forward_scores is not None:
            result["raw_tree_forward"] = raw_tree_forward
            result["forward_valid"] = fast_evaluate(
                forward_users, forward_labels, forward_scores
            )
        if args.predictions_out:
            args.predictions_out.parent.mkdir(parents=True, exist_ok=True)
            predictions = {"valid": valid_scores.astype(np.float32)}
            if forward_scores is not None:
                predictions["forward"] = forward_scores.astype(np.float32)
            np.savez_compressed(args.predictions_out, **predictions)
        serializable = json.loads(json.dumps(result, default=str))
        if args.json_out:
            args.json_out.parent.mkdir(parents=True, exist_ok=True)
            args.json_out.write_text(
                json.dumps(serializable, indent=2, sort_keys=True) + "\n"
            )
        print("RESULT_JSON=" + json.dumps(serializable, sort_keys=True))
        return
    if profile_mode:
        checkpoint_path = args.embedding_profile_checkpoint
        parent_path = args.embedding_profile_parent_predictions
        assert checkpoint_path is not None and parent_path is not None
        checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
        if not isinstance(checkpoint, dict):
            raise ValueError("video profile checkpoint must contain a dictionary")
        if checkpoint.get("feature_set") != "history_item_repeat":
            raise ValueError("video profile checkpoint must be a history_item_repeat model")
        if checkpoint.get("model_type") != "sparse_fm":
            raise ValueError("video profile checkpoint must be a sparse_fm model")
        if checkpoint.get("split_mode") != args.split_mode:
            raise ValueError("video profile checkpoint split does not match requested split")
        if checkpoint.get("split_bounds") != bounds:
            raise ValueError("video profile checkpoint bounds do not match requested split")
        if int(checkpoint.get("seed", -1)) != args.seed:
            raise ValueError("video profile checkpoint seed does not match requested seed")
        parent = np.load(parent_path)
        if "valid" not in parent.files or len(parent["valid"]) != len(valid_indices):
            raise ValueError("video profile parent has no aligned validation predictions")
        all_score_indices = (
            np.concatenate([valid_indices, forward_indices])
            if forward_indices is not None
            else valid_indices
        )
        all_profile, all_supported, profile_metadata = frozen_video_profile_scores(
            rows, train_indices, all_score_indices, checkpoint, args.predict_batch_size
        )
        valid_profile = all_profile[: len(valid_indices)]
        valid_supported = all_supported[: len(valid_indices)]
        valid_users = np.asarray(rows.user[valid_indices], dtype=np.int32)
        valid_labels = np.asarray(rows.label[valid_indices], dtype=np.uint8)
        valid_profile_metadata = dict(profile_metadata)
        valid_profile_metadata.update(
            {
                "supported_rows": int(valid_supported.sum()),
                "supported_users": int(np.unique(valid_users[valid_supported]).size),
            }
        )
        valid_scores = slot_preserving_profile_blend(
            valid_users, parent["valid"], valid_profile, valid_supported
        )
        result = {
            "benchmark": rows.manifest["benchmark"],
            "variant": "frozen_video_profile_slot_consensus",
            "split_mode": args.split_mode,
            "split_bounds": bounds,
            "checkpoint": str(checkpoint_path),
            "checkpoint_sha256": sha256_path(checkpoint_path),
            "parent_predictions": str(parent_path),
            "parent_predictions_sha256": sha256_path(parent_path),
            "profile_definition": (
                "mean unit video latent over every training long-view-positive "
                "exposure; cosine candidate score; supported candidates reorder "
                "only their parent percentile slots; equal parent/profile votes"
            ),
            "valid_profile": valid_profile_metadata,
            "valid": fast_evaluate(valid_users, valid_labels, valid_scores),
            "robustness": robustness_slices(
                rows, activity_reference_indices, valid_indices, valid_scores
            ),
            "robustness_activity_reference_rows": int(len(activity_reference_indices)),
            "elapsed_seconds": time.time() - started,
            "public_test_evaluated": False,
        }
        forward_scores = None
        if forward_indices is not None:
            if "forward" not in parent.files or len(parent["forward"]) != len(
                forward_indices
            ):
                raise ValueError("video profile parent has no aligned forward predictions")
            forward_users = np.asarray(rows.user[forward_indices], dtype=np.int32)
            forward_labels = np.asarray(rows.label[forward_indices], dtype=np.uint8)
            forward_profile = all_profile[len(valid_indices) :]
            forward_supported = all_supported[len(valid_indices) :]
            forward_profile_metadata = dict(profile_metadata)
            forward_profile_metadata.update(
                {
                    "supported_rows": int(forward_supported.sum()),
                    "supported_users": int(
                        np.unique(forward_users[forward_supported]).size
                    ),
                }
            )
            forward_scores = slot_preserving_profile_blend(
                forward_users,
                parent["forward"],
                forward_profile,
                forward_supported,
            )
            result["forward_profile"] = forward_profile_metadata
            result["forward_valid"] = fast_evaluate(
                forward_users, forward_labels, forward_scores
            )
        if args.predictions_out:
            args.predictions_out.parent.mkdir(parents=True, exist_ok=True)
            predictions = {"valid": valid_scores.astype(np.float32)}
            if forward_scores is not None:
                predictions["forward"] = forward_scores.astype(np.float32)
            np.savez_compressed(args.predictions_out, **predictions)
        serializable = json.loads(json.dumps(result, default=str))
        if args.json_out:
            args.json_out.parent.mkdir(parents=True, exist_ok=True)
            args.json_out.write_text(
                json.dumps(serializable, indent=2, sort_keys=True) + "\n"
            )
        print("RESULT_JSON=" + json.dumps(serializable, sort_keys=True))
        return
    if args.prediction_files:
        if len(args.prediction_files) < 2:
            raise ValueError("at least two prediction files are required")
        archives = [np.load(path) for path in args.prediction_files]
        members = [archive["valid"] for archive in archives]
        if any(len(member) != len(valid_indices) for member in members):
            raise ValueError("ensemble prediction length mismatch")
        valid_users = np.asarray(rows.user[valid_indices], dtype=np.int32)
        valid_labels = np.asarray(rows.label[valid_indices], dtype=np.uint8)
        routing_metadata = None
        activity = np.bincount(
            np.asarray(rows.user[activity_reference_indices], dtype=np.int64),
            minlength=rows.manifest["user_count"],
        )
        if args.prediction_routing in {
            "high_activity_last_member",
            "high_activity_last_member_only",
            "high_activity_equal_blend",
        }:
            activity_cutoff = activity_upper_tertile(valid_users, activity)
            route_function = {
                "high_activity_last_member": high_activity_specialist_scores,
                "high_activity_last_member_only": high_activity_fallback_scores,
                "high_activity_equal_blend": high_activity_equal_blend_scores,
            }[args.prediction_routing]
            valid_scores, valid_route = route_function(
                valid_users,
                activity,
                members,
                args.prediction_aggregation,
                activity_cutoff,
            )
            routing_metadata = {
                "method": args.prediction_routing,
                "activity_cutoff": activity_cutoff,
                "valid_routed_rows": int(valid_route.sum()),
                "valid_routed_users": int(np.unique(valid_users[valid_route]).size),
            }
        else:
            valid_scores = aggregate_prediction_members(
                valid_users, members, args.prediction_aggregation
            )
        result = {
            "benchmark": rows.manifest["benchmark"],
            "variant": (
                "mean_user_rank_ensemble"
                if args.prediction_aggregation == "user_rank_mean"
                else "mean_raw_logit_ensemble"
            ),
            "prediction_aggregation": args.prediction_aggregation,
            "prediction_routing": routing_metadata,
            "split_mode": args.split_mode,
            "split_bounds": bounds,
            "members": [str(path) for path in args.prediction_files],
            "valid": fast_evaluate(valid_users, valid_labels, valid_scores),
            "robustness": robustness_slices(
                rows, activity_reference_indices, valid_indices, valid_scores
            ),
            "robustness_activity_reference_rows": int(len(activity_reference_indices)),
            "elapsed_seconds": time.time() - started,
            "public_test_evaluated": False,
        }
        forward_scores = None
        if forward_indices is not None:
            if any("forward" not in archive.files for archive in archives):
                raise ValueError("shadow ensemble member has no forward predictions")
            forward_members = [archive["forward"] for archive in archives]
            if any(len(member) != len(forward_indices) for member in forward_members):
                raise ValueError("ensemble forward prediction length mismatch")
            forward_users = np.asarray(rows.user[forward_indices], dtype=np.int32)
            forward_labels = np.asarray(rows.label[forward_indices], dtype=np.uint8)
            if args.prediction_routing in {
                "high_activity_last_member",
                "high_activity_last_member_only",
                "high_activity_equal_blend",
            }:
                route_function = {
                    "high_activity_last_member": high_activity_specialist_scores,
                    "high_activity_last_member_only": high_activity_fallback_scores,
                    "high_activity_equal_blend": high_activity_equal_blend_scores,
                }[args.prediction_routing]
                forward_scores, forward_route = route_function(
                    forward_users,
                    activity,
                    forward_members,
                    args.prediction_aggregation,
                    routing_metadata["activity_cutoff"],
                )
                routing_metadata.update(
                    {
                        "forward_routed_rows": int(forward_route.sum()),
                        "forward_routed_users": int(
                            np.unique(forward_users[forward_route]).size
                        ),
                    }
                )
            else:
                forward_scores = aggregate_prediction_members(
                    forward_users, forward_members, args.prediction_aggregation
                )
            result["forward_valid"] = fast_evaluate(
                forward_users, forward_labels, forward_scores
            )
        if args.predictions_out:
            args.predictions_out.parent.mkdir(parents=True, exist_ok=True)
            predictions = {"valid": valid_scores.astype(np.float32)}
            if forward_scores is not None:
                predictions["forward"] = forward_scores.astype(np.float32)
            np.savez_compressed(args.predictions_out, **predictions)
        serializable = json.loads(json.dumps(result, default=str))
        if args.json_out:
            args.json_out.parent.mkdir(parents=True, exist_ok=True)
            args.json_out.write_text(
                json.dumps(serializable, indent=2, sort_keys=True) + "\n"
            )
        print("RESULT_JSON=" + json.dumps(serializable, sort_keys=True))
        return
    encoder = Encoder(
        rows,
        train_indices,
        args.feature_set,
        args.split_mode,
        args.min_video_count,
        args.min_author_count,
        args.time_features,
    )
    dimension = int(encoder.field_dims.sum())
    if args.model_type == "deep_fm":
        model = DeepFM(
            dimension,
            len(encoder.field_dims),
            args.rank,
            tuple(args.deep_hidden_dims),
            args.deep_dropout,
            encoder.offsets,
            args.seed,
            args.latent_init_std,
        )
    elif args.model_type == "field_aware_fm":
        model = FieldAwareFM(
            dimension,
            len(encoder.field_dims),
            args.rank,
            encoder.offsets,
            args.seed,
            args.latent_init_std,
        )
    elif args.model_type == "wide_cross_fm":
        if args.feature_set != "cross":
            raise ValueError("wide_cross_fm requires --feature-set cross")
        model = WideCrossFM(
            dimension,
            args.rank,
            8,
            encoder.offsets,
            args.seed,
            args.latent_init_std,
        )
    elif args.model_type == "additive_tail_fm":
        if args.feature_set != "history_item_repeat_sequence":
            raise ValueError(
                "additive_tail_fm requires --feature-set "
                "history_item_repeat_sequence"
            )
        model = WideCrossFM(
            dimension,
            args.rank,
            24,
            encoder.offsets,
            args.seed,
            args.latent_init_std,
        )
    elif args.model_type == "bipartite_fm":
        if args.feature_set != "history_item_repeat":
            raise ValueError("bipartite_fm requires --feature-set history_item_repeat")
        model = BipartiteFM(
            dimension,
            args.rank,
            (0, 3, *range(8, 16), *range(20, 24)),
            (1, 2, *range(4, 8), *range(16, 20)),
            encoder.offsets,
            args.seed,
            args.latent_init_std,
        )
    elif args.model_type == "funnel_fm":
        model = FunnelFM(
            dimension,
            args.rank,
            encoder.offsets,
            args.seed,
            args.latent_init_std,
        )
    else:
        model = SparseFM(
            dimension,
            args.rank,
            encoder.offsets,
            args.seed,
            args.latent_init_std,
            neutral_unknown_init=not args.legacy_random_unknown_init,
        )
    loaded_checkpoint = None
    checkpoint_in_sha256 = None
    if args.checkpoint_in is not None:
        checkpoint_in_sha256 = sha256_path(args.checkpoint_in)
        # This is an ignored checkpoint produced locally by this program. Its
        # metadata and tensor shapes are checked immediately after unpickling.
        loaded_checkpoint = torch.load(
            args.checkpoint_in, map_location="cpu", weights_only=False
        )
        if not isinstance(loaded_checkpoint, dict):
            raise ValueError("checkpoint must contain a dictionary")
        validate_checkpoint_metadata(loaded_checkpoint, encoder, args, bounds)
        if loaded_checkpoint["latent"].shape != model.latent.weight.shape:
            raise ValueError("checkpoint latent tensor shape mismatch")
        if loaded_checkpoint["linear"].shape != model.linear.weight.shape:
            raise ValueError("checkpoint linear tensor shape mismatch")
        if args.model_type == "funnel_fm":
            if (
                loaded_checkpoint["click_linear"].shape
                != model.click_linear.weight.shape
            ):
                raise ValueError("checkpoint click-linear tensor shape mismatch")
        with torch.no_grad():
            model.latent.weight.copy_(loaded_checkpoint["latent"])
            model.linear.weight.copy_(loaded_checkpoint["linear"])
            if args.model_type == "funnel_fm":
                model.click_linear.weight.copy_(loaded_checkpoint["click_linear"])
        if args.model_type == "deep_fm":
            model.deep.load_state_dict(loaded_checkpoint["deep"])
    sparse_parameters = [model.latent.weight, model.linear.weight]
    if args.model_type == "funnel_fm":
        sparse_parameters.append(model.click_linear.weight)
    optimizer = torch.optim.SparseAdam(sparse_parameters, lr=args.learning_rate)
    dense_optimizer = (
        torch.optim.Adam(model.deep.parameters(), lr=args.dense_learning_rate)
        if args.model_type == "deep_fm"
        else None
    )
    rng = np.random.default_rng(args.seed)
    best_primary = -math.inf
    best_weights = None
    if loaded_checkpoint is not None:
        best_weights = {
            "latent": model.latent.weight.detach().clone(),
            "linear": model.linear.weight.detach().clone(),
            "epoch": 0,
        }
        if args.model_type == "deep_fm":
            best_weights["deep"] = {
                key: value.detach().clone()
                for key, value in model.deep.state_dict().items()
            }
        if args.model_type == "funnel_fm":
            best_weights["click_linear"] = (
                model.click_linear.weight.detach().clone()
            )
    bad = 0
    trace = []
    train_labels = (
        np.asarray(rows.label[train_indices], dtype=np.float32)
        if args.epochs
        else None
    )
    train_clicks = (
        np.asarray(rows.is_click[train_indices], dtype=np.float32)
        if args.epochs and args.model_type == "funnel_fm"
        else None
    )
    positive_class_weight = (
        balanced_positive_weight(train_labels)
        if args.balance_positive_class and train_labels is not None
        else 1.0
    )
    loss_fn = nn.BCEWithLogitsLoss(
        reduction="none",
        pos_weight=(
            torch.tensor(positive_class_weight)
            if args.balance_positive_class
            else None
        ),
    )
    train_weights = (
        user_balanced_weights(
            np.asarray(rows.user[train_indices], dtype=np.int64),
            args.user_balance_alpha,
        )
        if args.epochs
        else None
    )
    valid_users = np.asarray(rows.user[valid_indices], dtype=np.int32)
    valid_labels = np.asarray(rows.label[valid_indices], dtype=np.uint8)
    chronological_order = (
        chronological_epoch_order(
            np.asarray(rows.time_ms[train_indices], dtype=np.int64)
        )
        if args.epoch_order == "chronological"
        else None
    )
    identity_ranges = tuple(
        (
            int(encoder.offsets[field]),
            int(encoder.offsets[field] + encoder.field_dims[field]),
        )
        for field in range(3)
    )

    for epoch in range(1, args.epochs + 1):
        epoch_started = time.time()
        model.train()
        epoch_order = (
            chronological_order
            if chronological_order is not None
            else rng.permutation(len(train_indices))
        )
        order = fractional_epoch_order(epoch_order, args.epoch_fraction)
        losses = []
        for start in range(0, len(order), args.batch_size):
            positions = order[start : start + args.batch_size]
            batch_indices = train_indices[positions]
            fields = torch.from_numpy(encoder.encode(rows, batch_indices))
            assert train_labels is not None and train_weights is not None
            labels = torch.from_numpy(train_labels[positions])
            optimizer.zero_grad(set_to_none=True)
            if dense_optimizer is not None:
                dense_optimizer.zero_grad(set_to_none=True)
            weights = torch.from_numpy(train_weights[positions])
            if args.model_type == "funnel_fm":
                assert train_clicks is not None
                click_labels = torch.from_numpy(train_clicks[positions])
                click_logits, conditional_logits = model.funnel_logits(fields)
                joint_probability = (
                    torch.sigmoid(click_logits) * torch.sigmoid(conditional_logits)
                ).clamp(1e-7, 1.0 - 1e-7)
                row_loss = F.binary_cross_entropy(
                    joint_probability, labels, reduction="none"
                ) + F.binary_cross_entropy_with_logits(
                    click_logits, click_labels, reduction="none"
                )
            else:
                logits = model(fields)
                row_loss = loss_fn(logits, labels)
            loss = (row_loss * weights).mean()
            if args.l2:
                active = model.latent(fields)
                loss = loss + args.l2 * (active * active).mean()
            if args.wide_cross_l2:
                if args.model_type != "wide_cross_fm":
                    raise ValueError("--wide-cross-l2 requires wide_cross_fm")
                active_cross_weights = model.linear(fields[:, 8:])
                loss = loss + args.wide_cross_l2 * (
                    active_cross_weights * active_cross_weights
                ).mean()
            loss.backward()
            if (
                args.freeze_identity_after_epoch
                and epoch > args.freeze_identity_after_epoch
            ):
                remove_sparse_gradient_rows(model.latent.weight, identity_ranges)
                remove_sparse_gradient_rows(model.linear.weight, identity_ranges)
            optimizer.step()
            if dense_optimizer is not None:
                dense_optimizer.step()
            losses.append(float(loss.detach()))
        valid_scores = predict(model, rows, encoder, valid_indices, args.predict_batch_size)
        metric = fast_evaluate(valid_users, valid_labels, valid_scores)
        epoch_record = {
            "epoch": epoch,
            "loss": float(np.mean(losses)),
            "valid": metric,
            "elapsed_seconds": time.time() - epoch_started,
        }
        trace.append(epoch_record)
        print(
            f"epoch {epoch:2d} loss {epoch_record['loss']:.5f} "
            f"GAUC {metric['GAUC']:.6f} nDCG@5 {metric['nDCG@5']:.6f} "
            f"primary {metric['primary']:.6f} {epoch_record['elapsed_seconds']:.1f}s",
            flush=True,
        )
        if metric["primary"] > best_primary + 1e-5:
            best_primary = float(metric["primary"])
            best_weights = {
                "latent": model.latent.weight.detach().clone(),
                "linear": model.linear.weight.detach().clone(),
                "epoch": epoch,
            }
            if args.model_type == "deep_fm":
                best_weights["deep"] = {
                    key: value.detach().clone()
                    for key, value in model.deep.state_dict().items()
                }
            if args.model_type == "funnel_fm":
                best_weights["click_linear"] = (
                    model.click_linear.weight.detach().clone()
                )
            bad = 0
        else:
            bad += 1
            if bad >= args.patience:
                break
    if best_weights is None:
        raise RuntimeError("training produced no checkpoint")
    with torch.no_grad():
        model.latent.weight.copy_(best_weights["latent"])
        model.linear.weight.copy_(best_weights["linear"])
        if args.model_type == "funnel_fm":
            model.click_linear.weight.copy_(best_weights["click_linear"])
    if args.model_type == "deep_fm":
        model.deep.load_state_dict(best_weights["deep"])
    valid_scores = predict(model, rows, encoder, valid_indices, args.predict_batch_size)
    pointwise_valid = fast_evaluate(valid_users, valid_labels, valid_scores)
    pairwise_trace = []
    pair_metadata = None
    pairwise_best_epoch = None
    if args.pairwise_epochs:
        if args.pairwise_negative_sampling == "hard":
            train_scores = predict(
                model, rows, encoder, train_indices, args.predict_batch_size
            )
            positive_rows, negative_rows, pair_metadata = within_user_hard_pairs(
                rows,
                train_indices,
                train_scores,
                args.pairwise_max_positives,
            )
            del train_scores
        else:
            pair_builder = (
                within_user_pairs
                if args.pairwise_scope == "within_user"
                else same_impression_pairs
            )
            positive_rows, negative_rows, pair_metadata = pair_builder(
                rows,
                train_indices,
                args.pairwise_max_positives,
                args.seed + 104729,
            )
        if not len(positive_rows):
            raise ValueError("pairwise training produced no usable pairs")
        pair_optimizer = torch.optim.SparseAdam(
            [model.latent.weight, model.linear.weight],
            lr=args.pairwise_learning_rate,
        )
        pair_dense_optimizer = (
            torch.optim.Adam(model.deep.parameters(), lr=args.pairwise_learning_rate)
            if args.model_type == "deep_fm"
            else None
        )
        pair_rng = np.random.default_rng(args.seed + 130363)
        pair_best_primary = float(pointwise_valid["primary"])
        pair_best_scores = valid_scores.copy()
        pair_best_weights = {
            "latent": model.latent.weight.detach().clone(),
            "linear": model.linear.weight.detach().clone(),
        }
        if args.model_type == "deep_fm":
            pair_best_weights["deep"] = {
                key: value.detach().clone()
                for key, value in model.deep.state_dict().items()
            }
        pair_bad = 0
        for pair_epoch in range(1, args.pairwise_epochs + 1):
            pair_started = time.time()
            model.train()
            pair_order = pair_rng.permutation(len(positive_rows))
            pair_losses = []
            for start in range(0, len(pair_order), args.pairwise_batch_size):
                positions = pair_order[start : start + args.pairwise_batch_size]
                positive_fields = torch.from_numpy(
                    encoder.encode(rows, positive_rows[positions])
                )
                negative_fields = torch.from_numpy(
                    encoder.encode(rows, negative_rows[positions])
                )
                pair_optimizer.zero_grad(set_to_none=True)
                if pair_dense_optimizer is not None:
                    pair_dense_optimizer.zero_grad(set_to_none=True)
                difference = model(positive_fields) - model(negative_fields)
                pair_loss = torch.nn.functional.softplus(-difference).mean()
                pair_loss.backward()
                pair_optimizer.step()
                if pair_dense_optimizer is not None:
                    pair_dense_optimizer.step()
                pair_losses.append(float(pair_loss.detach()))
            pair_scores = predict(
                model, rows, encoder, valid_indices, args.predict_batch_size
            )
            pair_metric = fast_evaluate(valid_users, valid_labels, pair_scores)
            pair_record = {
                "epoch": pair_epoch,
                "loss": float(np.mean(pair_losses)),
                "valid": pair_metric,
                "elapsed_seconds": time.time() - pair_started,
            }
            improved = bool(pair_metric["primary"] > pair_best_primary + 1e-5)
            pair_record["selected"] = improved
            pairwise_trace.append(pair_record)
            print(
                f"pairwise {pair_epoch:2d} loss {pair_record['loss']:.5f} "
                f"GAUC {pair_metric['GAUC']:.6f} nDCG@5 {pair_metric['nDCG@5']:.6f} "
                f"primary {pair_metric['primary']:.6f} "
                f"{pair_record['elapsed_seconds']:.1f}s",
                flush=True,
            )
            if improved:
                pair_best_primary = float(pair_metric["primary"])
                pair_best_scores = pair_scores.copy()
                pairwise_best_epoch = pair_epoch
                pair_best_weights = {
                    "latent": model.latent.weight.detach().clone(),
                    "linear": model.linear.weight.detach().clone(),
                }
                if args.model_type == "deep_fm":
                    pair_best_weights["deep"] = {
                        key: value.detach().clone()
                        for key, value in model.deep.state_dict().items()
                    }
                pair_bad = 0
            else:
                pair_bad += 1
                if args.pairwise_select_best and pair_bad >= args.pairwise_patience:
                    break
        if args.pairwise_select_best:
            with torch.no_grad():
                model.latent.weight.copy_(pair_best_weights["latent"])
                model.linear.weight.copy_(pair_best_weights["linear"])
            if args.model_type == "deep_fm":
                model.deep.load_state_dict(pair_best_weights["deep"])
            best_weights["latent"] = pair_best_weights["latent"]
            best_weights["linear"] = pair_best_weights["linear"]
            if args.model_type == "deep_fm":
                best_weights["deep"] = pair_best_weights["deep"]
            valid_scores = pair_best_scores
        else:
            pairwise_best_epoch = pairwise_trace[-1]["epoch"]
            best_weights["latent"] = model.latent.weight.detach().clone()
            best_weights["linear"] = model.linear.weight.detach().clone()
            if args.model_type == "deep_fm":
                best_weights["deep"] = {
                    key: value.detach().clone()
                    for key, value in model.deep.state_dict().items()
                }
            valid_scores = pair_scores
    result: dict[str, object] = {
        "benchmark": "KuaiRand-1K",
        "variant": (
            "content_deep_fm"
            if args.model_type == "deep_fm" and args.feature_set == "content"
            else "deep_fm"
            if args.model_type == "deep_fm"
            else "content_field_aware_fm"
            if args.model_type == "field_aware_fm" and args.feature_set == "content"
            else "field_aware_fm"
            if args.model_type == "field_aware_fm"
            else "history_item_repeat_funnel_fm"
            if args.model_type == "funnel_fm"
            and args.feature_set == "history_item_repeat"
            else "full_history_sparse_fm"
            if args.feature_set == "full_history"
            else "history_sparse_fm"
            if args.feature_set == "history"
            else "item_history_sparse_fm"
            if args.feature_set == "item_history"
            else "history_item_sparse_fm"
            if args.feature_set == "history_item"
            else "history_item_behavior_sparse_fm"
            if args.feature_set == "history_item_behavior"
            else "history_item_trend_sparse_fm"
            if args.feature_set == "history_item_trend"
            else "history_item_repeat_bipartite_fm"
            if args.feature_set == "history_item_repeat"
            and args.model_type == "bipartite_fm"
            else "history_item_repeat_time_sparse_fm"
            if args.feature_set == "history_item_repeat"
            and args.model_type == "sparse_fm"
            and args.time_features
            else "history_item_repeat_sparse_fm"
            if args.feature_set == "history_item_repeat"
            else "history_item_repeat_author_behavior_sparse_fm"
            if args.feature_set == "history_item_repeat_author_behavior"
            else "history_item_repeat_author_recency_sparse_fm"
            if args.feature_set == "history_item_repeat_author_recency"
            else "history_item_repeat_tag_affinity_sparse_fm"
            if args.feature_set == "history_item_repeat_tag_affinity"
            else "history_item_repeat_multitag_affinity_sparse_fm"
            if args.feature_set == "history_item_repeat_multitag_affinity"
            else "history_item_repeat_sequence_sparse_fm"
            if args.feature_set == "history_item_repeat_sequence"
            and args.model_type == "sparse_fm"
            else "history_item_repeat_sequence_additive_tail_fm"
            if args.feature_set == "history_item_repeat_sequence"
            and args.model_type == "additive_tail_fm"
            else "sequence_profile_sparse_fm"
            if args.feature_set == "sequence"
            else "explicit_user_cross_sparse_fm"
            if args.feature_set == "cross"
            and args.model_type == "sparse_fm"
            else "wide_user_cross_fm"
            if args.model_type == "wide_cross_fm"
            else "multitag_sparse_fm"
            if args.feature_set == "multitag"
            else "rich_metadata_sparse_fm"
            if args.feature_set == "rich"
            else "content_sparse_fm"
            if args.feature_set == "content"
            else "sparse_fm"
        ),
        "split_mode": args.split_mode,
        "split_bounds": bounds,
        "train_rows": int(len(train_indices)),
        "robustness_activity_reference_rows": int(len(activity_reference_indices)),
        "valid_rows": int(len(valid_indices)),
        "field_dims": encoder.field_dims.tolist(),
        "embedding_rows": dimension,
        "identity_frequency": {
            "min_video_count": args.min_video_count,
            "min_author_count": args.min_author_count,
            "time_features": args.time_features,
            "legacy_random_unknown_init": args.legacy_random_unknown_init,
            "seen_videos": int(encoder.seen_video.sum()),
            "seen_authors": int(encoder.seen_author.sum()),
        },
        "positive_class_weight": positive_class_weight,
        "best_epoch": best_weights["epoch"],
        "valid": fast_evaluate(valid_users, valid_labels, valid_scores),
        "pointwise_valid": pointwise_valid,
        "pairwise_trace": pairwise_trace,
        "pair_metadata": pair_metadata,
        "pairwise_best_epoch": pairwise_best_epoch,
        "checkpoint_in_sha256": checkpoint_in_sha256,
        "robustness": robustness_slices(
            rows, activity_reference_indices, valid_indices, valid_scores
        ),
        "trace": trace,
        "parameters": vars(args) | {"cache_dir": str(args.cache_dir)},
        "elapsed_seconds": time.time() - started,
        "public_test_evaluated": False,
    }
    if forward_indices is not None:
        forward_scores = predict(
            model, rows, encoder, forward_indices, args.predict_batch_size
        )
        result["forward_valid"] = fast_evaluate(
            np.asarray(rows.user[forward_indices], dtype=np.int32),
            np.asarray(rows.label[forward_indices], dtype=np.uint8),
            forward_scores,
        )
    if args.model_out:
        args.model_out.parent.mkdir(parents=True, exist_ok=True)
        checkpoint = {
            "latent": best_weights["latent"],
            "linear": best_weights["linear"],
            "field_dims": encoder.field_dims,
            "offsets": encoder.offsets,
            "duration_edges": encoder.duration_edges,
            "seen_user": encoder.seen_user,
            "seen_video": encoder.seen_video,
            "seen_author": encoder.seen_author,
            "feature_set": args.feature_set,
            "split_bounds": bounds,
            "split_mode": args.split_mode,
            "seed": args.seed,
            "model_type": args.model_type,
            "min_video_count": args.min_video_count,
            "min_author_count": args.min_author_count,
            "legacy_random_unknown_init": args.legacy_random_unknown_init,
            "epoch_order": args.epoch_order,
            "checkpoint_in_sha256": checkpoint_in_sha256,
            "pairwise_best_epoch": pairwise_best_epoch,
            "pairwise_scope": args.pairwise_scope,
            "pairwise_negative_sampling": args.pairwise_negative_sampling,
        }
        if args.model_type == "funnel_fm":
            checkpoint["click_linear"] = best_weights["click_linear"]
        if args.model_type == "deep_fm":
            checkpoint.update(
                {
                    "deep": best_weights["deep"],
                    "deep_hidden_dims": tuple(args.deep_hidden_dims),
                    "deep_dropout": args.deep_dropout,
                }
            )
        if args.feature_set in {"content", "cross", "history", "full_history", "item_history", "history_item", "history_item_behavior", "history_item_trend", "history_item_repeat", "history_item_repeat_author_behavior", "history_item_repeat_author_recency", "history_item_repeat_tag_affinity", "history_item_repeat_multitag_affinity", "history_item_repeat_sequence", "sequence", "multitag", "rich"}:
            checkpoint.update(
                {
                    "seen_tag": encoder.seen_tag,
                    "seen_upload_type": encoder.seen_upload_type,
                    "seen_video_type": encoder.seen_video_type,
                }
            )
        if args.feature_set == "multitag":
            checkpoint.update(
                {
                    "seen_tag2": encoder.seen_tag2,
                    "seen_tag3": encoder.seen_tag3,
                }
            )
        if args.feature_set == "rich":
            checkpoint.update(
                {
                    "seen_music_type": encoder.seen_music_type,
                    "seen_visible_status": encoder.seen_visible_status,
                    "seen_aspect": encoder.seen_aspect,
                    "seen_age": encoder.seen_age,
                    "age_edges_days": AGE_EDGES_DAYS,
                }
            )
        if args.feature_set in {"history", "full_history", "history_item", "history_item_behavior", "history_item_trend", "history_item_repeat", "history_item_repeat_author_behavior", "history_item_repeat_author_recency", "history_item_repeat_tag_affinity", "history_item_repeat_multitag_affinity", "history_item_repeat_sequence"}:
            checkpoint["history_feature_names"] = [
                "prior_user_count_log2",
                "prior_user_long_view_rate_21",
                "prior_user_strong_feedback_count_log2",
                "prior_user_hate_count_log2",
                "prior_user_tag_count_log2",
                "prior_user_tag_long_view_rate_21",
                "current_tag_matches_last_positive_tag",
                "last_positive_tag",
            ]
        if args.feature_set in {"item_history", "history_item", "history_item_behavior", "history_item_trend", "history_item_repeat", "history_item_repeat_author_behavior", "history_item_repeat_author_recency", "history_item_repeat_tag_affinity", "history_item_repeat_multitag_affinity", "history_item_repeat_sequence"}:
            checkpoint["item_history_feature_names"] = [
                "prior_day_video_count_log2",
                "prior_day_video_long_view_rate_21",
                "prior_day_author_count_log2",
                "prior_day_author_long_view_rate_21",
            ]
            if args.feature_set == "history_item_behavior":
                checkpoint["item_history_feature_names"].extend(
                    [
                        "prior_day_video_strong_feedback_rate_21",
                        "prior_day_video_hate_rate_21",
                        "prior_day_author_strong_feedback_rate_21",
                        "prior_day_author_hate_rate_21",
                    ]
                )
            if args.feature_set == "history_item_trend":
                checkpoint["item_history_feature_names"].extend(
                    [
                        "prior_3d_video_count_log2",
                        "prior_3d_video_long_view_rate_21",
                        "prior_3d_author_count_log2",
                        "prior_3d_author_long_view_rate_21",
                    ]
                )
        if args.feature_set in {"history_item_repeat", "history_item_repeat_author_behavior", "history_item_repeat_author_recency", "history_item_repeat_tag_affinity", "history_item_repeat_multitag_affinity", "history_item_repeat_sequence"}:
            checkpoint["user_entity_history_feature_names"] = [
                "prior_user_author_count_log2",
                "prior_user_author_long_view_rate_21",
                "prior_user_video_count_log2",
                "prior_user_video_long_view_rate_21",
            ]
        if args.feature_set == "history_item_repeat_tag_affinity":
            checkpoint["user_tag_history_feature_names"] = [
                "prior_user_primary_tag_count_log2",
                "prior_user_primary_tag_long_view_rate_21",
            ]
        if args.feature_set == "history_item_repeat_multitag_affinity":
            checkpoint["user_multitag_history_feature_names"] = [
                "prior_user_primary_tag_any_position_count_log2",
                "prior_user_primary_tag_any_position_long_view_rate_21",
            ]
        if args.feature_set == "history_item_repeat_author_behavior":
            checkpoint["user_author_behavior_feature_names"] = [
                "prior_user_author_strong_feedback_rate_21",
                "prior_user_author_hate_rate_21",
            ]
        if args.feature_set == "history_item_repeat_author_recency":
            checkpoint["user_author_recency_feature_names"] = [
                "prior_user_author_exposure_gap_hours_log2",
                "prior_user_author_long_view_gap_hours_log2",
            ]
        if args.feature_set in {"sequence", "history_item_repeat_sequence"}:
            checkpoint["sequence_profile_feature_names"] = [
                "last_positive_tag_1",
                "last_positive_tag_2",
                "last_positive_tag_3",
                "last_positive_tag_4",
                "last_positive_tag_5",
                "current_tag_count_in_last_5_positive",
                "last_strong_positive_tag",
                "current_tag_matches_last_strong_positive",
                "last_hate_tag",
                "current_tag_matches_last_hate",
                "hours_since_last_positive_log2",
            ]
        if args.feature_set == "cross":
            checkpoint["explicit_cross_feature_names"] = [
                "user_x_primary_tag",
                "user_x_upload_type",
                "user_x_video_type",
                "user_x_duration_bucket",
            ]
        if args.time_features:
            checkpoint["recurring_time_feature_names"] = [
                "asia_shanghai_hour_of_day",
                "weekday",
            ]
        torch.save(checkpoint, args.model_out)
    if args.predictions_out:
        args.predictions_out.parent.mkdir(parents=True, exist_ok=True)
        payload = {"valid": valid_scores.astype(np.float32)}
        if forward_indices is not None:
            payload["forward"] = forward_scores.astype(np.float32)
        np.savez_compressed(args.predictions_out, **payload)
    serializable = json.loads(json.dumps(result, default=str))
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(serializable, indent=2, sort_keys=True) + "\n")
    print("RESULT_JSON=" + json.dumps(serializable, sort_keys=True))


if __name__ == "__main__":
    main()
