#!/usr/bin/env python3
"""Track 2 ranking experiments.

The organizer evaluator is imported unchanged. Official test outcomes are
redacted at the loader boundary and cannot be evaluated by this CLI.
"""
from __future__ import annotations

import argparse
import collections
import csv
import datetime as dt
import hashlib
import json
import math
import sys
import time
from pathlib import Path

import lightgbm as lgb
import numpy as np
from scipy import sparse
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer

ROOT = Path(__file__).resolve().parents[1]
STARTER = ROOT / "organizer" / "kuairand-starter-kit"
sys.path.insert(0, str(STARTER))
from evaluate import evaluate  # noqa: E402
from data import encode as organizer_encode, load as organizer_load  # noqa: E402
from baseline import FM as OrganizerFM  # noqa: E402


SPLITS = {
    "train": (20220408, 20220421),
    "valid": (20220422, 20220428),
    "test": (20220429, 20220508),
}

SHADOW_SPLITS = {
    "shadow_early": {
        "train": (20220408, 20220411),
        "valid": (20220412, 20220414),
        "test": (20220415, 20220417),
    },
    "shadow_middle": {
        "train": (20220408, 20220414),
        "valid": (20220415, 20220417),
        "test": (20220418, 20220421),
    },
    "shadow_late": {
        "train": (20220408, 20220417),
        "valid": (20220418, 20220421),
        "test": (20220422, 20220428),
    },
}


def split_bounds_for_mode(mode):
    if mode == "official":
        return SPLITS
    if mode == "shadow":
        return SHADOW_SPLITS["shadow_late"]
    return SHADOW_SPLITS[mode]


def sequence_history_indices(rows, mode="causal"):
    """Return the deterministic row traversal used to construct histories."""
    if mode == "source":
        return list(range(len(rows)))
    if mode != "causal":
        raise ValueError(f"unknown sequence history order: {mode}")
    by_user = collections.defaultdict(list)
    for index, row in enumerate(rows):
        by_user[row["user"]].append(index)
    return [
        index
        for indices in by_user.values()
        for index in sorted(indices, key=lambda item: (rows[item]["time_ms"], item))
    ]


STRICT_SKIP_WATCH_RATIO = 0.05
DUAL_RECENT_HISTORY_LENGTH = 5


def is_strict_skip_history_event(row):
    """Return whether a labeled training row is a high-confidence skip.

    The rule is intentionally fixed and conservative: the impression was not
    a long view, was not clicked, and consumed no more than five percent of the
    video. It is called only for labeled training rows; validation and official
    test histories are frozen from training state.
    """
    return bool(
        row["label"] == 0
        and row["click"] == 0
        and min(row["play_time"] / max(row["duration"], 1.0), 1.0)
        <= STRICT_SKIP_WATCH_RATIO
    )


def is_secondary_history_event(row, event):
    """Select a distinct causal feedback channel without using target labels."""
    if event == "none":
        return False
    if event == "click":
        return bool(row["click"])
    if event == "engagement":
        return any(bool(row[name]) for name in ("like", "follow", "comment", "forward"))
    raise ValueError(f"unknown secondary history event: {event}")


def masked_attention_profile(historical, attention_logits, mask):
    """Return a finite masked attention profile, including for empty rows."""
    import torch

    if historical.ndim != 3 or attention_logits.shape != mask.shape:
        raise ValueError("attention values, logits, and mask are not aligned")
    if historical.shape[:2] != mask.shape:
        raise ValueError("attention history and mask are not aligned")
    masked_logits = attention_logits.masked_fill(~mask, -1e4)
    attention = torch.softmax(masked_logits, dim=1) * mask
    attention = attention / attention.sum(1, keepdim=True).clamp_min(1e-6)
    return (historical * attention[:, :, None]).sum(1)


def hard_attention_profile(historical, attention_logits, mask):
    """Select the highest-scoring valid history vector and zero empty rows."""
    import torch

    if historical.ndim != 3 or attention_logits.shape != mask.shape:
        raise ValueError("attention values, logits, and mask are not aligned")
    if historical.shape[:2] != mask.shape:
        raise ValueError("attention history and mask are not aligned")
    masked_logits = attention_logits.masked_fill(~mask, -torch.inf)
    rows = torch.arange(len(historical), device=historical.device)
    selected = historical[rows, masked_logits.argmax(1)]
    return selected * mask.any(1, keepdim=True)


def build_task_protected_extraction(input_dim, hidden_dim, dropout):
    """Build one task-protected shared/specific expert extraction layer.

    Long-view and click each mix two shared experts with one private expert.
    The task-specific gates start uniform and learn the appropriate sharing.
    """
    import torch
    from torch import nn

    if input_dim <= 0 or hidden_dim < 2:
        raise ValueError("task-protected extraction needs positive dimensions")
    expert_dim = hidden_dim // 2

    def expert():
        return nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, expert_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
        )

    class TaskProtectedExtraction(nn.Module):
        def __init__(self):
            super().__init__()
            self.shared_experts = nn.ModuleList([expert(), expert()])
            self.long_view_expert = expert()
            self.click_expert = expert()
            self.long_view_gate = nn.Linear(input_dim, 3)
            self.click_gate = nn.Linear(input_dim, 3)
            self.long_view_head = nn.Linear(expert_dim, 1)
            self.click_head = nn.Linear(expert_dim, 1)
            for gate in (self.long_view_gate, self.click_gate):
                nn.init.zeros_(gate.weight)
                nn.init.zeros_(gate.bias)

        @staticmethod
        def mix(experts, gate):
            stacked = torch.stack(experts, dim=1)
            return (stacked * torch.softmax(gate, dim=1)[:, :, None]).sum(1)

        def forward(self, values):
            shared = [expert_layer(values) for expert_layer in self.shared_experts]
            long_view = self.mix(
                shared + [self.long_view_expert(values)],
                self.long_view_gate(values),
            )
            click = self.mix(
                shared + [self.click_expert(values)],
                self.click_gate(values),
            )
            return (
                self.long_view_head(long_view).squeeze(1),
                self.click_head(click).squeeze(1),
            )

    return TaskProtectedExtraction()


def build_causal_history_transformer(embedding_dim, history_length, dropout):
    """Build the single frozen causal self-attention history encoder."""
    from torch import nn

    if embedding_dim <= 0 or embedding_dim % 4:
        raise ValueError("history transformer width must be positive and divisible by 4")
    if history_length <= 0:
        raise ValueError("history transformer length must be positive")
    position_embedding = nn.Embedding(history_length, embedding_dim)
    layer = nn.TransformerEncoderLayer(
        d_model=embedding_dim,
        nhead=4,
        dim_feedforward=4 * embedding_dim,
        dropout=dropout,
        activation="gelu",
        batch_first=True,
        norm_first=False,
    )
    encoder = nn.TransformerEncoder(
        layer,
        num_layers=1,
        enable_nested_tensor=False,
    )
    return position_embedding, encoder


def encode_causal_history(encoder, position_embedding, historical, mask):
    """Encode left-padded histories without producing NaNs for empty rows."""
    import torch

    if historical.ndim != 3 or mask.shape != historical.shape[:2]:
        raise ValueError("history values and padding mask are not aligned")
    positions = torch.arange(historical.shape[1], device=historical.device)
    positioned = historical + position_embedding(positions)[None, :, :]
    encoded = torch.zeros_like(positioned)
    nonempty = mask.any(dim=1)
    if bool(nonempty.any()):
        causal_mask = torch.triu(
            torch.ones(
                historical.shape[1],
                historical.shape[1],
                dtype=torch.bool,
                device=historical.device,
            ),
            diagonal=1,
        )
        encoded[nonempty] = encoder(
            positioned[nonempty],
            mask=causal_mask,
            src_key_padding_mask=~mask[nonempty],
        )
    return encoded * mask[:, :, None]


def _read_metadata(data_dir: Path):
    videos = {}
    with (data_dir / "video_features_basic_pure.csv").open() as fh:
        for r in csv.DictReader(fh):
            videos[r["video_id"]] = {
                "author": r["author_id"],
                "video_type": r["video_type"],
                "upload_type": r["upload_type"],
                "music": r["music_id"],
                "tag": r["tag"],
            }
    users = {}
    with (data_dir / "user_features_pure.csv").open() as fh:
        for r in csv.DictReader(fh):
            users[r["user_id"]] = {
                "user_active_degree": r["user_active_degree"],
                "follow_range": r["follow_user_num_range"],
                "fans_range": r["fans_user_num_range"],
                "friend_range": r["friend_user_num_range"],
                "register_range": r["register_days_range"],
            }
    return videos, users


OUTCOME_FIELDS = (
    "label",
    "click",
    "like",
    "follow",
    "comment",
    "forward",
    "hate",
    "play_time",
)


def _materialize_row(raw, videos, users, *, include_outcomes=True):
    video = videos.get(raw["video_id"], {})
    user = users.get(raw["user_id"], {})
    tags = [value for value in video.get("tag", "").split(",") if value]
    row = {
        "date": int(raw["date"]),
        "time_ms": int(raw["time_ms"]),
        "user": raw["user_id"],
        "video": raw["video_id"],
        "author": video.get("author", "UNK"),
        "video_type": video.get("video_type", "UNK"),
        "upload_type": video.get("upload_type", "UNK"),
        "music": video.get("music", "UNK"),
        "tag1": tags[0] if tags else "UNK",
        "tag2": tags[1] if len(tags) > 1 else "NONE",
        "tag_combo": video.get("tag", "UNK") or "UNK",
        "tab": raw["tab"],
        "hour": int(raw["hourmin"]) // 100,
        "weekday": str(dt.datetime.strptime(raw["date"], "%Y%m%d").weekday()),
        "duration": float(raw["duration_ms"]),
        "user_active_degree": user.get("user_active_degree", "UNK"),
        "follow_range": user.get("follow_range", "UNK"),
        "fans_range": user.get("fans_range", "UNK"),
        "friend_range": user.get("friend_range", "UNK"),
        "register_range": user.get("register_range", "UNK"),
    }
    if include_outcomes:
        row.update(
            {
                "play_time": float(raw["play_time_ms"]),
                "label": 0 if raw["long_view"] == "0" else 1,
                "click": 0 if raw["is_click"] == "0" else 1,
                "like": 0 if raw["is_like"] == "0" else 1,
                "follow": 0 if raw["is_follow"] == "0" else 1,
                "comment": 0 if raw["is_comment"] == "0" else 1,
                "forward": 0 if raw["is_forward"] == "0" else 1,
                "hate": 0 if raw["is_hate"] == "0" else 1,
            }
        )
    return row


def load_rows(data_dir: Path, split_bounds=None):
    """Load requested dates and redact every official-test outcome.

    Rows dated after the official validation boundary are projected to
    feature-only dictionaries before any outcome field is accessed. Shadow
    forward windows end no later than 2022-04-28 and retain development labels.
    """
    videos, users = _read_metadata(data_dir)
    rows = []
    bounds = split_bounds or SPLITS
    wanted_ranges = tuple(bounds.values())
    wanted = (
        "log_standard_4_08_to_4_21_pure.csv",
        "log_standard_4_22_to_5_08_pure.csv",
    )
    for filename in wanted:
        with (data_dir / filename).open() as fh:
            for r in csv.DictReader(fh):
                date = int(r["date"])
                if not any(lo <= date <= hi for lo, hi in wanted_ranges):
                    continue
                rows.append(
                    _materialize_row(
                        r,
                        videos,
                        users,
                        include_outcomes=date <= SPLITS["valid"][1],
                    )
                )
    splits = {
        name: [r for r in rows if lo <= r["date"] <= hi]
        for name, (lo, hi) in bounds.items()
    }
    if bounds == SPLITS:
        leaked = [
            field
            for row in splits["test"]
            for field in OUTCOME_FIELDS
            if field in row
        ]
        if leaked:
            raise RuntimeError(f"official test outcome escaped loader boundary: {leaked[0]}")
    return splits


def load_random_rows(data_dir: Path):
    """Load the organizer-identified unbiased validation log."""
    videos, users = _read_metadata(data_dir)
    path = data_dir / "log_random_4_22_to_5_08_pure.csv"
    with path.open() as handle:
        return [_materialize_row(row, videos, users) for row in csv.DictReader(handle)]


def label_boundary_attestation(official_test_rows_feature_only: bool):
    """Describe the fitted-state boundary carried by every modern result."""
    return {
        "official_test_outcomes_loaded": False,
        "official_test_rows_feature_only": bool(official_test_rows_feature_only),
        "fitted_preprocessing_splits": ["train"],
        "behavior_history_splits": ["train"],
        "official_test_outcome_statistics_used": False,
    }


def robustness_slices(train_rows, valid_rows, scores):
    """Report temporal and activity slices without changing the official metric."""
    activity = collections.Counter(row["user"] for row in train_rows)
    counts = np.asarray([activity[row["user"]] for row in valid_rows])
    positive_counts = counts[counts > 0]
    cut1, cut2 = np.quantile(positive_counts, [1 / 3, 2 / 3]) if len(positive_counts) else (0, 0)
    dates = sorted({row["date"] for row in valid_rows})
    midpoint = len(dates) // 2
    groups = {
        "early_dates": {date for date in dates[:midpoint]},
        "late_dates": {date for date in dates[midpoint:]},
    }
    output = {}
    for name, selected_dates in groups.items():
        indices = [i for i, row in enumerate(valid_rows) if row["date"] in selected_dates]
        output[name] = evaluate(
            [valid_rows[i]["user"] for i in indices],
            [valid_rows[i]["label"] for i in indices],
            np.asarray(scores)[indices],
        )
    activity_groups = {
        "cold_or_low_activity": counts <= cut1,
        "medium_activity": (counts > cut1) & (counts <= cut2),
        "high_activity": counts > cut2,
    }
    for name, mask in activity_groups.items():
        indices = np.flatnonzero(mask)
        output[name] = evaluate(
            [valid_rows[i]["user"] for i in indices],
            [valid_rows[i]["label"] for i in indices],
            np.asarray(scores)[indices],
        )
    output["activity_cutpoints"] = [float(cut1), float(cut2)]
    output["minimum_primary"] = min(
        metric["primary"] for metric in output.values() if isinstance(metric, dict)
    )
    return output


class FeatureBuilder:
    CAT_NAMES = (
        "video",
        "author",
        "tab",
        "video_type",
        "upload_type",
        "music",
        "duration_bucket",
        "hour",
    )
    RATE_KEYS = (
        ("video",),
        ("author",),
        ("user", "video"),
        ("user", "author"),
        ("user", "duration_bucket"),
        ("tab", "video"),
    )

    def __init__(self, train_rows, include_history: bool):
        self.include_history = include_history
        durations = np.asarray([r["duration"] for r in train_rows])
        self.duration_edges = np.quantile(durations, np.linspace(0, 1, 11)[1:-1])
        for r in train_rows:
            r["duration_bucket"] = str(int(np.searchsorted(self.duration_edges, r["duration"])))
        self.vocabs = {}
        for name in self.CAT_NAMES:
            vals = sorted({str(r[name]) for r in train_rows})
            self.vocabs[name] = {v: i + 1 for i, v in enumerate(vals)}
        self.global_rates = {
            target: sum(r[target] for r in train_rows) / len(train_rows)
            for target in ("label", "click", "like")
        }
        self.stats = {}
        if include_history:
            for fields in self.RATE_KEYS:
                by_key = collections.defaultdict(lambda: [0, 0, 0, 0])
                for r in train_rows:
                    k = tuple(r[f] for f in fields)
                    s = by_key[k]
                    s[0] += 1
                    s[1] += r["label"]
                    s[2] += r["click"]
                    s[3] += r["like"]
                self.stats[fields] = by_key

    def _prepare(self, rows):
        for r in rows:
            if "duration_bucket" not in r:
                r["duration_bucket"] = str(int(np.searchsorted(self.duration_edges, r["duration"])))

    def transform(self, rows, training=False):
        self._prepare(rows)
        columns = []
        names = []
        categorical = []
        for name in self.CAT_NAMES:
            vocab = self.vocabs[name]
            columns.append(np.asarray([vocab.get(str(r[name]), 0) for r in rows], dtype=np.float32))
            categorical.append(len(columns) - 1)
            names.append(name)
        day0 = SPLITS["train"][0]
        columns.extend(
            [
                np.log1p(np.asarray([r["duration"] for r in rows], dtype=np.float32)),
                np.asarray([r["date"] - day0 for r in rows], dtype=np.float32),
                np.sin(np.asarray([r["hour"] for r in rows]) * (2 * math.pi / 24)).astype(np.float32),
                np.cos(np.asarray([r["hour"] for r in rows]) * (2 * math.pi / 24)).astype(np.float32),
            ]
        )
        names.extend(("log_duration", "day_index", "hour_sin", "hour_cos"))
        if self.include_history:
            for fields in self.RATE_KEYS:
                stats = self.stats[fields]
                for target, pos_idx, prior in (("label", 1, 20.0), ("click", 2, 20.0), ("like", 3, 100.0)):
                    vals = np.empty(len(rows), dtype=np.float32)
                    mean = self.global_rates[target]
                    for i, r in enumerate(rows):
                        k = tuple(r[f] for f in fields)
                        n, lv, click, like = stats.get(k, (0, 0, 0, 0))
                        pos = (lv, click, like)[pos_idx - 1]
                        if training:
                            n -= 1
                            pos -= r[target]
                        vals[i] = (pos + prior * mean) / (n + prior)
                    columns.append(vals)
                    names.append("_".join(fields) + "_" + target + "_rate")
        return np.column_stack(columns).astype(np.float32), names, categorical


class CausalAggregateBuilder:
    """Build past-only numeric behavior aggregates plus raw categorical context."""

    CAT_NAMES = (
        "user",
        "video",
        "author",
        "tag1",
        "tag_combo",
        "tab",
        "duration_bucket",
        "hour",
        "video_type",
        "upload_type",
        "user_active_degree",
    )
    KEYS = (
        ("user",),
        ("video",),
        ("author",),
        ("tag1",),
        ("tag_combo",),
        ("user", "author"),
        ("user", "tag1"),
        ("user", "tag_combo"),
        ("user", "duration_bucket"),
        ("tab", "video"),
    )
    TARGETS = (
        ("label", 20.0),
        ("click", 20.0),
        ("like", 100.0),
        ("follow", 200.0),
        ("comment", 200.0),
    )

    def __init__(self, train_rows):
        durations = np.asarray([row["duration"] for row in train_rows])
        self.duration_edges = np.quantile(durations, np.linspace(0, 1, 11)[1:-1])
        for row in train_rows:
            row["duration_bucket"] = str(
                int(np.searchsorted(self.duration_edges, row["duration"]))
            )
        self.vocabs = {}
        for name in self.CAT_NAMES:
            values = sorted({str(row[name]) for row in train_rows})
            self.vocabs[name] = {value: index + 1 for index, value in enumerate(values)}
        self.global_means = {
            target: sum(row[target] for row in train_rows) / len(train_rows)
            for target, _ in self.TARGETS
        }
        self.global_watch_ratio = float(
            np.mean(
                [
                    min(row["play_time"] / max(row["duration"], 1.0), 1.0)
                    for row in train_rows
                ]
            )
        )
        self.statistics = {
            fields: collections.defaultdict(lambda: np.zeros(7, dtype=np.float64))
            for fields in self.KEYS
        }

    def _prepare(self, rows):
        for row in rows:
            if "duration_bucket" not in row:
                row["duration_bucket"] = str(
                    int(np.searchsorted(self.duration_edges, row["duration"]))
                )

    def _empty(self, size):
        names = list(self.CAT_NAMES)
        names += ["log_duration", "hour_sin", "hour_cos"]
        for fields in self.KEYS:
            prefix = "_".join(fields)
            names.append(f"{prefix}_log_count")
            names.extend(f"{prefix}_{target}_rate" for target, _ in self.TARGETS)
            names.append(f"{prefix}_watch_ratio")
        matrix = np.empty((size, len(names)), dtype=np.float32)
        return matrix, names, list(range(len(self.CAT_NAMES)))

    def _base_features(self, rows, matrix):
        for column, name in enumerate(self.CAT_NAMES):
            vocab = self.vocabs[name]
            matrix[:, column] = [vocab.get(str(row[name]), 0) for row in rows]
        offset = len(self.CAT_NAMES)
        matrix[:, offset] = np.log1p(
            np.asarray([row["duration"] for row in rows], dtype=np.float32)
        )
        hours = np.asarray([row["hour"] for row in rows], dtype=np.float32)
        matrix[:, offset + 1] = np.sin(hours * (2 * math.pi / 24))
        matrix[:, offset + 2] = np.cos(hours * (2 * math.pi / 24))

    def _aggregate_features(self, row, matrix, index):
        column = len(self.CAT_NAMES) + 3
        for fields in self.KEYS:
            key = tuple(row[field] for field in fields)
            stats = self.statistics[fields][key]
            count = stats[0]
            matrix[index, column] = math.log1p(count)
            column += 1
            for target_index, (target, prior) in enumerate(self.TARGETS, start=1):
                matrix[index, column] = (
                    stats[target_index] + prior * self.global_means[target]
                ) / (count + prior)
                column += 1
            matrix[index, column] = (
                stats[6] + 20.0 * self.global_watch_ratio
            ) / (count + 20.0)
            column += 1

    def _update(self, row):
        watch_ratio = min(row["play_time"] / max(row["duration"], 1.0), 1.0)
        increments = np.asarray(
            [
                1.0,
                row["label"],
                row["click"],
                row["like"],
                row["follow"],
                row["comment"],
                watch_ratio,
            ],
            dtype=np.float64,
        )
        for fields in self.KEYS:
            key = tuple(row[field] for field in fields)
            self.statistics[fields][key] += increments

    def fit_transform(self, rows):
        self._prepare(rows)
        matrix, names, categorical = self._empty(len(rows))
        self._base_features(rows, matrix)
        order = sorted(range(len(rows)), key=lambda index: (rows[index]["time_ms"], index))
        for index in order:
            self._aggregate_features(rows[index], matrix, index)
            self._update(rows[index])
        return matrix, names, categorical

    def transform(self, rows):
        self._prepare(rows)
        matrix, names, categorical = self._empty(len(rows))
        self._base_features(rows, matrix)
        for index, row in enumerate(rows):
            self._aggregate_features(row, matrix, index)
        return matrix, names, categorical


class CausalRepeatBuilder:
    """Build strictly past-only memory features for repeated user-video pairs."""

    NAMES = (
        "pair_seen",
        "pair_log_count",
        "pair_label_rate",
        "pair_click_rate",
        "pair_like_rate",
        "pair_watch_ratio",
        "pair_last_label",
        "pair_last_click",
        "pair_last_like",
        "pair_log_time_gap_hours",
    )

    def __init__(self, train_rows):
        self.global_means = {
            target: float(np.mean([row[target] for row in train_rows]))
            for target in ("label", "click", "like")
        }
        self.global_watch_ratio = float(
            np.mean(
                [
                    min(row["play_time"] / max(row["duration"], 1.0), 1.0)
                    for row in train_rows
                ]
            )
        )
        # count, sums(label/click/like/watch), last(label/click/like/time_ms)
        self.statistics = collections.defaultdict(lambda: np.zeros(9, dtype=np.float64))

    def _features(self, row):
        state = self.statistics[(row["user"], row["video"])]
        count = state[0]
        seen = float(count > 0)
        if count:
            gap_hours = max(float(row["time_ms"]) - state[8], 0.0) / 3_600_000.0
        else:
            gap_hours = 0.0
        return (
            seen,
            math.log1p(count),
            (state[1] + 5.0 * self.global_means["label"]) / (count + 5.0),
            (state[2] + 5.0 * self.global_means["click"]) / (count + 5.0),
            (state[3] + 20.0 * self.global_means["like"]) / (count + 20.0),
            (state[4] + 5.0 * self.global_watch_ratio) / (count + 5.0),
            state[5] if count else 0.0,
            state[6] if count else 0.0,
            state[7] if count else 0.0,
            math.log1p(gap_hours),
        )

    def _update(self, row):
        state = self.statistics[(row["user"], row["video"])]
        state[0] += 1.0
        state[1] += row["label"]
        state[2] += row["click"]
        state[3] += row["like"]
        state[4] += min(row["play_time"] / max(row["duration"], 1.0), 1.0)
        state[5] = row["label"]
        state[6] = row["click"]
        state[7] = row["like"]
        state[8] = row["time_ms"]

    def fit_transform(self, rows):
        matrix = np.empty((len(rows), len(self.NAMES)), dtype=np.float32)
        order = sorted(range(len(rows)), key=lambda index: (rows[index]["time_ms"], index))
        for index in order:
            matrix[index] = self._features(rows[index])
            self._update(rows[index])
        return matrix, list(self.NAMES)

    def transform(self, rows):
        matrix = np.empty((len(rows), len(self.NAMES)), dtype=np.float32)
        for index, row in enumerate(rows):
            matrix[index] = self._features(row)
        return matrix, list(self.NAMES)


def train_aggregate_binary(args):
    """Train a binary LightGBM on strictly past-only behavior aggregates."""
    t0 = time.time()
    split_bounds = split_bounds_for_mode(args.split_mode)
    splits = load_rows(Path(args.data_dir), split_bounds=split_bounds)
    builder = CausalAggregateBuilder(splits["train"])
    Xtr, names, categorical = builder.fit_transform(splits["train"])
    Xva, _, _ = builder.transform(splits["valid"])
    Xte, _, _ = builder.transform(splits["test"])
    ytr = np.asarray([row["label"] for row in splits["train"]], dtype=np.float32)
    yva = np.asarray([row["label"] for row in splits["valid"]], dtype=np.float32)
    valid_users = [row["user"] for row in splits["valid"]]

    train_set = lgb.Dataset(
        Xtr,
        label=ytr,
        feature_name=names,
        categorical_feature=categorical,
        free_raw_data=True,
    )
    valid_set = lgb.Dataset(
        Xva,
        label=yva,
        feature_name=names,
        categorical_feature=categorical,
        reference=train_set,
        free_raw_data=True,
    )
    params = {
        "objective": "binary",
        "metric": "binary_logloss",
        "learning_rate": args.learning_rate,
        "num_leaves": args.num_leaves,
        "min_data_in_leaf": args.min_data_in_leaf,
        "feature_fraction": args.feature_fraction,
        "bagging_fraction": args.bagging_fraction,
        "bagging_freq": 1 if args.bagging_fraction < 1 else 0,
        "lambda_l2": args.lambda_l2,
        "max_cat_to_onehot": 8,
        "cat_smooth": 20.0,
        "verbosity": -1,
        "seed": args.seed,
        "num_threads": args.threads,
        "deterministic": True,
        "force_col_wise": True,
    }
    model = lgb.train(
        params,
        train_set,
        num_boost_round=args.num_boost_round,
        valid_sets=[valid_set],
        callbacks=[
            lgb.early_stopping(args.early_stopping_rounds),
            lgb.log_evaluation(25),
        ],
    )
    validation_scores = model.predict(Xva, num_iteration=model.best_iteration)
    result = {
        "variant": args.variant,
        "valid": evaluate(valid_users, yva, validation_scores),
        "robustness": robustness_slices(splits["train"], splits["valid"], validation_scores),
        "best_iteration": model.best_iteration,
        "parameters": {
            **params,
            "split_mode": args.split_mode,
            "split_bounds": split_bounds,
        },
        "feature_count": len(names),
        "top_features": sorted(
            zip(names, model.feature_importance(importance_type="gain")),
            key=lambda item: item[1],
            reverse=True,
        )[:20],
        "elapsed_seconds": time.time() - t0,
    }
    test_scores = None
    if args.evaluate_forward or args.predict_test:
        test_scores = model.predict(Xte, num_iteration=model.best_iteration)
    if args.evaluate_forward:
        if args.split_mode == "official":
            raise ValueError("--evaluate-forward is only allowed with a shadow split")
        result["forward_valid"] = evaluate(
            [row["user"] for row in splits["test"]],
            [row["label"] for row in splits["test"]],
            test_scores,
        )
    if args.model_out:
        Path(args.model_out).parent.mkdir(parents=True, exist_ok=True)
        model.save_model(args.model_out, num_iteration=model.best_iteration)
    if args.predictions_out:
        Path(args.predictions_out).parent.mkdir(parents=True, exist_ok=True)
        payload = {"valid": np.asarray(validation_scores, dtype=np.float32)}
        if test_scores is not None:
            payload["test"] = np.asarray(test_scores, dtype=np.float32)
        np.savez_compressed(args.predictions_out, **payload)
    return result


def group_sort(rows, X):
    order = np.asarray(sorted(range(len(rows)), key=lambda i: (rows[i]["user"], i)), dtype=np.int64)
    users = [rows[i]["user"] for i in order]
    groups = []
    previous = None
    for u in users:
        if u != previous:
            groups.append(1)
            previous = u
        else:
            groups[-1] += 1
    y = np.asarray([rows[i]["label"] for i in order], dtype=np.float32)
    return X[order], y, groups, order


def pairwise_step(model, Xp, Xn, l2):
    """One BPR update for an organizer FM; the shared user terms cancel."""
    zp, Ep, Sp = model.logits(Xp)
    zn, En, Sn = model.logits(Xn)
    diff = np.clip(zp - zn, -30, 30)
    gp = (1.0 / (1.0 + np.exp(-diff)) - 1.0).astype(np.float32) / len(diff)
    gn = -gp
    gV = np.zeros_like(model.V)
    gW = np.zeros_like(model.W)
    np.add.at(gW, Xp, gp[:, None])
    np.add.at(gW, Xn, gn[:, None])
    np.add.at(gV, Xp, gp[:, None, None] * (Sp[:, None, :] - Ep))
    np.add.at(gV, Xn, gn[:, None, None] * (Sn[:, None, :] - En))
    gV += l2 * model.V
    gW += l2 * model.W
    model.t += 1
    b1, b2, eps = 0.9, 0.999, 1e-8
    for param, grad, mom, var in (
        (model.V, gV, model.mV, model.vV),
        (model.W, gW, model.mW, model.vW),
    ):
        mom *= b1
        mom += (1 - b1) * grad
        var *= b2
        var += (1 - b2) * (grad * grad)
        param -= model.lr * (mom / (1 - b1**model.t)) / (np.sqrt(var / (1 - b2**model.t)) + eps)
    return float(np.mean(np.logaddexp(0.0, -diff)))


def train_pairwise_fm(args):
    t0 = time.time()
    splits = organizer_load(args.data_dir)
    enc, dim = organizer_encode(splits)
    Xtr, ytr, utr = enc["train"]
    Xva, yva, uva = enc["valid"]
    Xte, yte, ute = enc["test"]
    model = OrganizerFM(dim, k=args.fm_k, lr=args.fm_lr, l2=args.fm_l2, seed=args.seed)
    rng = np.random.default_rng(args.seed)
    best = -1.0
    best_state = None
    trace = []

    if args.variant == "fm_then_bpr":
        bad = 0
        for epoch in range(1, args.fm_epochs + 1):
            order = rng.permutation(len(ytr))
            losses = []
            for start in range(0, len(order), args.fm_batch_size):
                ix = order[start : start + args.fm_batch_size]
                losses.append(model.step(Xtr[ix], ytr[ix]))
            metric = evaluate(uva, yva, model.predict(Xva))
            trace.append({"stage": "pointwise", "epoch": epoch, "loss": float(np.mean(losses)), "valid": metric})
            if metric["primary"] > best + 1e-5:
                best = metric["primary"]
                best_state = (model.V.copy(), model.W.copy(), np.float32(model.b))
                bad = 0
            else:
                bad += 1
                if bad >= args.fm_patience:
                    break
        model.V, model.W, model.b = (x.copy() if hasattr(x, "copy") else x for x in best_state)
        model.mV.fill(0)
        model.vV.fill(0)
        model.mW.fill(0)
        model.vW.fill(0)
        model.t = 0

    by_user = collections.defaultdict(lambda: [[], []])
    for i, (u, y) in enumerate(zip(utr, ytr)):
        by_user[u][int(y)].append(i)
    usable = [(np.asarray(v[1], dtype=np.int64), np.asarray(v[0], dtype=np.int64)) for v in by_user.values() if v[0] and v[1]]
    model.lr = args.bpr_lr
    bad = 0
    for epoch in range(1, args.bpr_epochs + 1):
        positives = np.concatenate([p for p, _ in usable])
        if args.bpr_sampling == "hard":
            training_scores = model.predict(Xtr)
            selected = []
            for p, n in usable:
                hard_count = min(args.hard_negative_pool, len(n))
                hard = n[np.argpartition(training_scores[n], -hard_count)[-hard_count:]]
                selected.append(rng.choice(hard, size=len(p), replace=True))
            negatives = np.concatenate(selected)
        else:
            negatives = np.concatenate([rng.choice(n, size=len(p), replace=True) for p, n in usable])
        order = rng.permutation(len(positives))
        positives, negatives = positives[order], negatives[order]
        losses = []
        for start in range(0, len(order), args.bpr_batch_size):
            p = positives[start : start + args.bpr_batch_size]
            n = negatives[start : start + args.bpr_batch_size]
            losses.append(pairwise_step(model, Xtr[p], Xtr[n], args.fm_l2))
        metric = evaluate(uva, yva, model.predict(Xva))
        trace.append({"stage": "bpr", "epoch": epoch, "loss": float(np.mean(losses)), "valid": metric})
        print(
            f"BPR epoch {epoch:2d} loss {np.mean(losses):.5f} "
            f"GAUC {metric['GAUC']:.5f} nDCG@5 {metric['nDCG@5']:.5f} primary {metric['primary']:.5f}",
            flush=True,
        )
        if metric["primary"] > best + 1e-5:
            best = metric["primary"]
            best_state = (model.V.copy(), model.W.copy(), np.float32(model.b))
            bad = 0
        else:
            bad += 1
            if bad >= args.bpr_patience:
                break
    model.V, model.W, model.b = (x.copy() if hasattr(x, "copy") else x for x in best_state)
    result = {
        "variant": args.variant,
        "valid": evaluate(uva, yva, model.predict(Xva)),
        "trace": trace,
        "parameters": {
            "fm_k": args.fm_k,
            "fm_lr": args.fm_lr,
            "fm_l2": args.fm_l2,
            "fm_epochs": args.fm_epochs if args.variant == "fm_then_bpr" else 0,
            "bpr_epochs": args.bpr_epochs,
            "bpr_batch_size": args.bpr_batch_size,
            "bpr_lr": args.bpr_lr,
            "bpr_sampling": args.bpr_sampling,
            "hard_negative_pool": args.hard_negative_pool,
            "seed": args.seed,
        },
        "elapsed_seconds": time.time() - t0,
    }
    if args.evaluate_test:
        result["test"] = evaluate(ute, yte, model.predict(Xte))
    if args.model_out:
        Path(args.model_out).parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(args.model_out, V=model.V, W=model.W, b=model.b)
    return result


def load_auxiliary_targets(data_dir):
    targets = {name: collections.defaultdict(list) for name in SPLITS}
    for filename in ("log_standard_4_08_to_4_21_pure.csv", "log_standard_4_22_to_5_08_pure.csv"):
        with (Path(data_dir) / filename).open() as fh:
            for r in csv.DictReader(fh):
                date = int(r["date"])
                split = next((name for name, (lo, hi) in SPLITS.items() if lo <= date <= hi), None)
                if split is None:
                    continue
                duration = max(float(r["duration_ms"]), 1.0)
                play_ratio = min(float(r["play_time_ms"]) / duration, 1.0)
                targets[split]["click"].append(float(r["is_click"] != "0"))
                targets[split]["watch_ratio"].append(play_ratio)
                engagement = max(
                    float(r["is_click"] != "0"),
                    float(r["is_like"] != "0"),
                    float(r["is_follow"] != "0"),
                    float(r["is_comment"] != "0"),
                    float(r["is_forward"] != "0"),
                )
                targets[split]["engagement"].append(engagement)
    return targets


def train_softlabel_fm(args):
    t0 = time.time()
    splits = organizer_load(args.data_dir)
    enc, dim = organizer_encode(splits)
    Xtr, ytr, _ = enc["train"]
    Xva, yva, uva = enc["valid"]
    Xte, yte, ute = enc["test"]
    auxiliary = load_auxiliary_targets(args.data_dir)
    aux_train = np.asarray(auxiliary["train"][args.aux_target], dtype=np.float32)
    if len(aux_train) != len(ytr):
        raise RuntimeError(f"auxiliary alignment failed: {len(aux_train)} != {len(ytr)}")
    train_target = (ytr + args.aux_weight * aux_train) / (1.0 + args.aux_weight)
    model = OrganizerFM(dim, k=args.fm_k, lr=args.fm_lr, l2=args.fm_l2, seed=args.seed)
    rng = np.random.default_rng(args.seed)
    best, best_state, bad = -1.0, None, 0
    trace = []
    for epoch in range(1, args.fm_epochs + 1):
        order = rng.permutation(len(train_target))
        losses = []
        for start in range(0, len(order), args.fm_batch_size):
            ix = order[start : start + args.fm_batch_size]
            losses.append(model.step(Xtr[ix], train_target[ix]))
        metric = evaluate(uva, yva, model.predict(Xva))
        trace.append({"epoch": epoch, "loss": float(np.mean(losses)), "valid": metric})
        print(
            f"epoch {epoch:2d} loss {np.mean(losses):.5f} GAUC {metric['GAUC']:.5f} "
            f"nDCG@5 {metric['nDCG@5']:.5f} primary {metric['primary']:.5f}",
            flush=True,
        )
        if metric["primary"] > best + 1e-5:
            best = metric["primary"]
            best_state = (model.V.copy(), model.W.copy(), np.float32(model.b))
            bad = 0
        else:
            bad += 1
            if bad >= args.fm_patience:
                break
    model.V, model.W, model.b = (x.copy() if hasattr(x, "copy") else x for x in best_state)
    result = {
        "variant": args.variant,
        "valid": evaluate(uva, yva, model.predict(Xva)),
        "trace": trace,
        "parameters": {
            "aux_target": args.aux_target,
            "aux_weight": args.aux_weight,
            "fm_k": args.fm_k,
            "fm_lr": args.fm_lr,
            "fm_l2": args.fm_l2,
            "seed": args.seed,
        },
        "elapsed_seconds": time.time() - t0,
    }
    if args.evaluate_test:
        result["test"] = evaluate(ute, yte, model.predict(Xte))
    if args.model_out:
        Path(args.model_out).parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(args.model_out, V=model.V, W=model.W, b=model.b)
    return result


def encode_extended_rows(splits, feature_set):
    train = splits["train"]
    edges = np.quantile(
        np.asarray([r["duration"] for r in train]),
        np.linspace(0, 1, 11)[1:-1],
    )
    for rows in splits.values():
        for r in rows:
            r["duration_bucket"] = str(int(np.searchsorted(edges, r["duration"])))
            r["day"] = str(r["date"])
    fields = ["user", "video", "author", "tab", "duration_bucket"]
    if feature_set in ("tags", "extended"):
        fields += ["tag1", "tag2", "tag_combo"]
    if feature_set == "extended":
        fields += ["video_type", "upload_type", "music", "hour", "day"]
    vocabs = []
    for field in fields:
        values = sorted({str(r[field]) for r in train})
        vocabs.append({value: i for i, value in enumerate(values)})
    dimensions = [len(vocab) + 1 for vocab in vocabs]
    offsets = np.cumsum([0] + dimensions[:-1]).astype(np.int32)
    encoded = {}
    for split, rows in splits.items():
        X = np.empty((len(rows), len(fields)), dtype=np.int32)
        y = np.asarray([r["label"] for r in rows], dtype=np.float32)
        users = [r["user"] for r in rows]
        for column, (field, vocab, offset) in enumerate(zip(fields, vocabs, offsets)):
            unknown = len(vocab)
            X[:, column] = [vocab.get(str(r[field]), unknown) + offset for r in rows]
        encoded[split] = (X, y, users)
    return encoded, int(sum(dimensions)), fields


def train_extended_fm(args):
    t0 = time.time()
    splits = load_rows(Path(args.data_dir))
    enc, dim, fields = encode_extended_rows(splits, args.feature_set)
    Xtr, ytr, _ = enc["train"]
    Xva, yva, uva = enc["valid"]
    Xte, yte, ute = enc["test"]
    model = OrganizerFM(dim, k=args.fm_k, lr=args.fm_lr, l2=args.fm_l2, seed=args.seed)
    rng = np.random.default_rng(args.seed)
    best, best_state, bad = -1.0, None, 0
    trace = []
    for epoch in range(1, args.fm_epochs + 1):
        order = rng.permutation(len(ytr))
        losses = []
        for start in range(0, len(order), args.fm_batch_size):
            ix = order[start : start + args.fm_batch_size]
            losses.append(model.step(Xtr[ix], ytr[ix]))
        metric = evaluate(uva, yva, model.predict(Xva))
        trace.append({"epoch": epoch, "loss": float(np.mean(losses)), "valid": metric})
        print(
            f"epoch {epoch:2d} loss {np.mean(losses):.5f} GAUC {metric['GAUC']:.5f} "
            f"nDCG@5 {metric['nDCG@5']:.5f} primary {metric['primary']:.5f}",
            flush=True,
        )
        if metric["primary"] > best + 1e-5:
            best = metric["primary"]
            best_state = (model.V.copy(), model.W.copy(), np.float32(model.b))
            bad = 0
        else:
            bad += 1
            if bad >= args.fm_patience:
                break
    model.V, model.W, model.b = (x.copy() if hasattr(x, "copy") else x for x in best_state)
    result = {
        "variant": args.variant,
        "feature_set": args.feature_set,
        "fields": fields,
        "valid": evaluate(uva, yva, model.predict(Xva)),
        "trace": trace,
        "parameters": {
            "fm_k": args.fm_k,
            "fm_lr": args.fm_lr,
            "fm_l2": args.fm_l2,
            "seed": args.seed,
        },
        "elapsed_seconds": time.time() - t0,
    }
    if args.evaluate_test:
        result["test"] = evaluate(ute, yte, model.predict(Xte))
    if args.model_out:
        Path(args.model_out).parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(args.model_out, V=model.V, W=model.W, b=model.b)
    return result


def train_svd_cf(args):
    t0 = time.time()
    splits = load_rows(Path(args.data_dir))
    train = splits["train"]
    user_vocab = {value: i for i, value in enumerate(sorted({r["user"] for r in train}))}
    video_vocab = {value: i for i, value in enumerate(sorted({r["video"] for r in train}))}
    global_rate = sum(r["label"] for r in train) / len(train)
    row = np.asarray([user_vocab[r["user"]] for r in train], dtype=np.int32)
    col = np.asarray([video_vocab[r["video"]] for r in train], dtype=np.int32)
    if args.svd_weighting == "positive":
        value = np.asarray([r["label"] for r in train], dtype=np.float32)
    else:
        value = np.asarray([r["label"] - global_rate for r in train], dtype=np.float32)
    matrix = sparse.coo_matrix(
        (value, (row, col)),
        shape=(len(user_vocab), len(video_vocab)),
        dtype=np.float32,
    ).tocsr()
    if args.svd_weighting == "positive":
        matrix.data = np.log1p(matrix.data)
        user_norm = np.sqrt(np.asarray(matrix.power(2).sum(axis=1)).ravel())
        user_norm[user_norm == 0] = 1.0
        matrix = sparse.diags(1.0 / user_norm) @ matrix
    svd = TruncatedSVD(
        n_components=args.svd_components,
        n_iter=args.svd_iterations,
        random_state=args.seed,
    )
    user_factors = svd.fit_transform(matrix)
    item_factors = svd.components_.T

    def predict(rows):
        scores = np.zeros(len(rows), dtype=np.float32)
        for i, r in enumerate(rows):
            u = user_vocab.get(r["user"])
            v = video_vocab.get(r["video"])
            if u is not None and v is not None:
                scores[i] = np.dot(user_factors[u], item_factors[v])
        return scores

    valid_rows = splits["valid"]
    valid = evaluate(
        [r["user"] for r in valid_rows],
        [r["label"] for r in valid_rows],
        predict(valid_rows),
    )
    result = {
        "variant": args.variant,
        "valid": valid,
        "parameters": {
            "svd_components": args.svd_components,
            "svd_iterations": args.svd_iterations,
            "svd_weighting": args.svd_weighting,
            "seed": args.seed,
        },
        "explained_variance_ratio_sum": float(svd.explained_variance_ratio_.sum()),
        "elapsed_seconds": time.time() - t0,
    }
    if args.evaluate_test:
        test_rows = splits["test"]
        result["test"] = evaluate(
            [r["user"] for r in test_rows],
            [r["label"] for r in test_rows],
            predict(test_rows),
        )
    return result


def train_sequence_nn(args):
    import torch
    from torch import nn

    t0 = time.time()
    behavior_names = ("label", "click", "like", "follow", "comment", "forward", "hate")

    def behavior_code(row):
        # Zero is reserved for sequence padding. Each real event stores a
        # one-offset bit mask so the model can recover every observed action.
        return 1 + sum(int(row[name]) << bit for bit, name in enumerate(behavior_names))

    if not 0.0 <= args.id_embedding_dropout < 1.0:
        raise ValueError("--id-embedding-dropout must be in [0, 1)")
    if not 0.0 < args.nn_bpr_hard_fraction <= 1.0:
        raise ValueError("--nn-bpr-hard-fraction must be in (0, 1]")
    if args.cross_layers < 0:
        raise ValueError("--cross-layers must be nonnegative")
    if args.cross_layers and args.auxiliary_task != "none":
        raise ValueError("cross layers are not implemented with an auxiliary task")
    if args.auxiliary_architecture != "shared" and args.auxiliary_task == "none":
        raise ValueError("task-protected extraction requires an auxiliary task")
    if args.cwm_c_inverse <= 0:
        raise ValueError("--cwm-c-inverse must be positive")
    if args.cwm_sigma <= 0:
        raise ValueError("--cwm-sigma must be positive")
    if args.dual_timescale_history and args.history_length < DUAL_RECENT_HISTORY_LENGTH:
        raise ValueError("dual-timescale history requires history length at least five")
    if args.secondary_history_event != "none" and args.negative_history_event != "none":
        raise ValueError("secondary and negative histories are mutually exclusive")
    has_secondary_history = (
        args.secondary_history_event != "none" or args.negative_history_event != "none"
    )
    if args.history_categories and args.history_primary_tag:
        raise ValueError(
            "--history-categories and --history-primary-tag share one history slot"
        )
    split_bounds = split_bounds_for_mode(args.split_mode)
    splits = load_rows(Path(args.data_dir), split_bounds=split_bounds)
    if args.evaluate_random:
        splits["random"] = load_random_rows(Path(args.data_dir))
    evaluation_split_names = ["valid", "test"] + (["random"] if args.evaluate_random else [])
    if args.history_categories:
        category_path = Path(args.category_file)
        if not category_path.exists():
            raise FileNotFoundError(
                f"category file not found: {category_path}; run scripts/acquire_kuairand_categories.sh"
            )
        categories = {}
        with category_path.open(newline="") as handle:
            for row in csv.DictReader(handle):
                categories[row["final_video_id"]] = "|".join(
                    [
                        row["first_level_category_id"] or "-124.0",
                        row["second_level_category_id"] or "-124.0",
                        row["third_level_category_id"] or "-124.0",
                    ]
                )
        for rows in splits.values():
            for row in rows:
                row["category_path"] = categories.get(row["video"], "UNK")
    caption_vectors = None
    caption_explained_variance = None
    caption_source_sha256 = None
    if args.caption_content:
        caption_path = Path(args.caption_file)
        if not caption_path.exists():
            raise FileNotFoundError(
                f"caption file not found: {caption_path}; "
                "run scripts/acquire_kuairand_captions.py"
            )
        caption_source_sha256 = hashlib.sha256(caption_path.read_bytes()).hexdigest()
        expected_caption_sha256 = (
            "7593a7e1497951a16ca29126605b751869cf66df5a2f845f7690b2f6c1f4ba2c"
        )
        if caption_source_sha256 != expected_caption_sha256:
            raise ValueError(
                f"caption subset SHA-256 mismatch: {caption_source_sha256}"
            )
        caption_text = {}
        with caption_path.open(newline="") as handle:
            for row in csv.DictReader(handle):
                caption_text[row["final_video_id"]] = " ".join(
                    value.strip()
                    for value in (row["caption"], row["show_cover_text"])
                    if value and value.strip()
                )
        expected_ids = {str(video_id) for video_id in range(7583)}
        if set(caption_text) != expected_ids:
            raise ValueError("caption subset does not cover exact Pure video IDs 0..7582")
        ordered_ids = [str(video_id) for video_id in range(7583)]
        vectorizer = TfidfVectorizer(
            analyzer="char",
            ngram_range=(2, 4),
            min_df=2,
            max_features=50_000,
            sublinear_tf=True,
            dtype=np.float32,
        )
        caption_tfidf = vectorizer.fit_transform([caption_text[video_id] for video_id in ordered_ids])
        caption_svd = TruncatedSVD(n_components=16, n_iter=7, random_state=2026)
        caption_dense = caption_svd.fit_transform(caption_tfidf).astype(np.float32)
        caption_norm = np.linalg.norm(caption_dense, axis=1, keepdims=True)
        caption_dense /= np.maximum(caption_norm, 1e-8)
        caption_vectors = dict(zip(ordered_ids, caption_dense))
        caption_explained_variance = float(caption_svd.explained_variance_ratio_.sum())
    train = splits["train"]
    if (args.causal_aggregate_features or args.causal_repeat_features) and (
        args.nn_bpr_epochs > 0
        or args.nn_listwise_epochs > 0
        or args.nn_lambda_epochs > 0
    ):
        raise ValueError(
            "causal aggregate features are not implemented for ranking fine-tuning"
        )
    if args.multi_behavior_context:
        context_fields = (
            "last_click_video",
            "last_click_tag",
            "last_engagement_video",
            "last_engagement_tag",
        )
        state = collections.defaultdict(
            lambda: {
                "last_click_video": "NONE",
                "last_click_tag": "NONE",
                "last_engagement_video": "NONE",
                "last_engagement_tag": "NONE",
            }
        )
        by_user = collections.defaultdict(list)
        for index, row in enumerate(train):
            by_user[row["user"]].append(index)
        for user, indices in by_user.items():
            user_state = state[user]
            for index in sorted(indices, key=lambda item: (train[item]["time_ms"], item)):
                row = train[index]
                for field in context_fields:
                    row[field] = user_state[field]
                if row["click"]:
                    user_state["last_click_video"] = row["video"]
                    user_state["last_click_tag"] = row["tag_combo"]
                if row["like"] or row["follow"] or row["comment"] or row["forward"]:
                    user_state["last_engagement_video"] = row["video"]
                    user_state["last_engagement_tag"] = row["tag_combo"]
        for split_name in evaluation_split_names:
            for row in splits[split_name]:
                user_state = state[row["user"]]
                for field in context_fields:
                    row[field] = user_state[field]
    if args.target_rate_features:
        global_mean = sum(row["label"] for row in train) / len(train)
        for source in ("video", "author", "tag_combo"):
            statistics = collections.defaultdict(lambda: [0, 0])
            for row in train:
                statistics[row[source]][0] += 1
                statistics[row[source]][1] += row["label"]
            train_values = []
            for row in train:
                count, positive = statistics[row[source]]
                value = (positive - row["label"] + 20.0 * global_mean) / (count - 1 + 20.0)
                train_values.append(value)
            edges = np.unique(np.quantile(np.asarray(train_values), np.linspace(0, 1, 21)[1:-1]))
            feature = f"{source}_rate_bucket"
            for row, value in zip(train, train_values):
                row[feature] = str(int(np.searchsorted(edges, value)))
            for split_name in evaluation_split_names:
                for row in splits[split_name]:
                    count, positive = statistics.get(row[source], (0, 0))
                    value = (positive + 20.0 * global_mean) / (count + 20.0)
                    row[feature] = str(int(np.searchsorted(edges, value)))
    fields = ["user", "video", "author", "tag_combo", "tab", "duration_bucket"]
    if args.multi_behavior_context:
        fields.extend(context_fields)
    if args.history_primary_tag:
        fields.append("tag1")
    if args.history_categories:
        fields.append("category_path")
    if args.user_profile_features:
        fields.extend(
            [
                "user_active_degree",
                "follow_range",
                "fans_range",
                "friend_range",
                "register_range",
            ]
        )
    if args.target_rate_features:
        fields.extend(["video_rate_bucket", "author_rate_bucket", "tag_combo_rate_bucket"])
    if args.time_features:
        fields.extend(["hour", "weekday"])
    durations = np.asarray([r["duration"] for r in train])
    duration_edges = np.quantile(durations, np.linspace(0, 1, 11)[1:-1])
    for rows in splits.values():
        for r in rows:
            r["duration_bucket"] = str(int(np.searchsorted(duration_edges, r["duration"])))
    aggregate_feature_names = []
    aggregate_train = np.zeros((len(train), 0), dtype=np.float32)
    aggregate_valid = np.zeros((len(splits["valid"]), 0), dtype=np.float32)
    aggregate_test = np.zeros((len(splits["test"]), 0), dtype=np.float32)
    aggregate_random = np.zeros((len(splits.get("random", [])), 0), dtype=np.float32)
    if args.causal_aggregate_features and args.causal_repeat_features:
        raise ValueError(
            "--causal-aggregate-features and --causal-repeat-features are separate fixed families"
        )
    if args.causal_aggregate_features:
        aggregate_builder = CausalAggregateBuilder(train)
        aggregate_train_full, aggregate_names, _ = aggregate_builder.fit_transform(train)
        aggregate_valid_full, _, _ = aggregate_builder.transform(splits["valid"])
        aggregate_test_full, _, _ = aggregate_builder.transform(splits["test"])
        aggregate_random_full = None
        if args.evaluate_random:
            aggregate_random_full, _, _ = aggregate_builder.transform(splits["random"])
        wanted = (
            "user_log_count",
            "user_label_rate",
            "user_click_rate",
            "user_watch_ratio",
            "video_log_count",
            "video_label_rate",
            "author_log_count",
            "author_label_rate",
            "tag_combo_label_rate",
            "user_author_label_rate",
            "user_tag_combo_label_rate",
            "tab_video_label_rate",
        )
        indices = [aggregate_names.index(name) for name in wanted]
        aggregate_feature_names = list(wanted)
        aggregate_train = aggregate_train_full[:, indices]
        aggregate_valid = aggregate_valid_full[:, indices]
        aggregate_test = aggregate_test_full[:, indices]
        if aggregate_random_full is not None:
            aggregate_random = aggregate_random_full[:, indices]
        aggregate_mean = aggregate_train.mean(axis=0)
        aggregate_scale = aggregate_train.std(axis=0)
        aggregate_scale[aggregate_scale < 1e-6] = 1.0
        aggregate_train = (aggregate_train - aggregate_mean) / aggregate_scale
        aggregate_valid = (aggregate_valid - aggregate_mean) / aggregate_scale
        aggregate_test = (aggregate_test - aggregate_mean) / aggregate_scale
        if args.evaluate_random:
            aggregate_random = (aggregate_random - aggregate_mean) / aggregate_scale
    elif args.causal_repeat_features:
        repeat_builder = CausalRepeatBuilder(train)
        aggregate_train, aggregate_feature_names = repeat_builder.fit_transform(train)
        aggregate_valid, _ = repeat_builder.transform(splits["valid"])
        aggregate_test, _ = repeat_builder.transform(splits["test"])
        if args.evaluate_random:
            aggregate_random, _ = repeat_builder.transform(splits["random"])
        aggregate_mean = aggregate_train.mean(axis=0)
        aggregate_scale = aggregate_train.std(axis=0)
        aggregate_scale[aggregate_scale < 1e-6] = 1.0
        aggregate_train = (aggregate_train - aggregate_mean) / aggregate_scale
        aggregate_valid = (aggregate_valid - aggregate_mean) / aggregate_scale
        aggregate_test = (aggregate_test - aggregate_mean) / aggregate_scale
        if args.evaluate_random:
            aggregate_random = (aggregate_random - aggregate_mean) / aggregate_scale
    vocabs = {}
    for field in fields:
        values = sorted({str(r[field]) for r in train})
        vocabs[field] = {value: i + 2 for i, value in enumerate(values)}
    dimensions = [len(vocabs[field]) + 2 for field in fields]
    caption_matrix = None
    if caption_vectors is not None:
        caption_matrix = np.zeros((dimensions[1], 16), dtype=np.float32)
        for video_id, vector in caption_vectors.items():
            encoded_video = vocabs["video"].get(video_id)
            if encoded_video is not None:
                caption_matrix[encoded_video] = vector

    def encode_rows(rows, *, require_labels=True):
        X = np.empty((len(rows), len(fields)), dtype=np.int32)
        for j, field in enumerate(fields):
            vocab = vocabs[field]
            X[:, j] = [vocab.get(str(r[field]), 1) for r in rows]
        y = (
            np.asarray([r["label"] for r in rows], dtype=np.float32)
            if require_labels
            else None
        )
        return X, y

    Xtr, ytr = encode_rows(train)
    Xva, yva = encode_rows(splits["valid"])
    Xte, yte = encode_rows(
        splits["test"], require_labels=args.split_mode != "official"
    )
    Xrandom = yrandom = None
    if args.evaluate_random:
        Xrandom, yrandom = encode_rows(splits["random"])
    valid_users = [r["user"] for r in splits["valid"]]
    history_length = args.history_length
    def empty_history(size):
        return (
            np.zeros((size, history_length), dtype=np.int32),
            np.zeros((size, history_length), dtype=np.int32),
            np.zeros((size, history_length), dtype=np.int32),
            np.zeros((size, history_length), dtype=np.int32),
            np.zeros((size, history_length), dtype=np.int32),
        )

    (
        train_history,
        train_history_tags,
        train_history_authors,
        train_history_outcomes,
        train_history_primary_tags,
    ) = empty_history(len(train))
    histories = collections.defaultdict(lambda: collections.deque(maxlen=history_length))
    train_negative_history = np.zeros((len(train), history_length), dtype=np.int32)
    train_negative_history_tags = np.zeros((len(train), history_length), dtype=np.int32)
    negative_histories = collections.defaultdict(
        lambda: collections.deque(maxlen=history_length)
    )
    for i in sequence_history_indices(train, args.history_order):
        row = train[i]
        history = histories[row["user"]]
        negative_history = negative_histories[row["user"]]
        if history:
            train_history[i, -len(history) :] = [value[0] for value in history]
            train_history_tags[i, -len(history) :] = [value[1] for value in history]
            train_history_authors[i, -len(history) :] = [value[2] for value in history]
            train_history_outcomes[i, -len(history) :] = [value[3] for value in history]
            train_history_primary_tags[i, -len(history) :] = [value[4] for value in history]
        if negative_history:
            train_negative_history[i, -len(negative_history) :] = [
                value[0] for value in negative_history
            ]
            train_negative_history_tags[i, -len(negative_history) :] = [
                value[1] for value in negative_history
            ]
        history_positive = (
            True
            if args.history_event == "all"
            else any(row[name] for name in behavior_names)
            if args.history_event == "behavior"
            else row["label"] if args.history_event == "long_view" else row[args.history_event]
        )
        if history_positive:
            history_side_value = (
                Xtr[i, fields.index("tag1")]
                if args.history_primary_tag
                else Xtr[i, fields.index("category_path")]
                if args.history_categories
                else 0
            )
            history.append(
                (
                    Xtr[i, 1],
                    Xtr[i, 3],
                    Xtr[i, 2],
                    behavior_code(row) if args.history_behavior_signals else row["label"] + 1,
                    history_side_value,
                )
            )
        if args.secondary_history_event != "none" and is_secondary_history_event(
            row, args.secondary_history_event
        ):
            negative_history.append((Xtr[i, 1], Xtr[i, 3]))
        elif (
            args.negative_history_event == "strict_skip_005"
            and is_strict_skip_history_event(row)
        ):
            negative_history.append((Xtr[i, 1], Xtr[i, 3]))

    def frozen_history(rows):
        video, tags, authors, outcomes, primary_tags = empty_history(len(rows))
        for i, row in enumerate(rows):
            history = histories[row["user"]]
            if history:
                video[i, -len(history) :] = [value[0] for value in history]
                tags[i, -len(history) :] = [value[1] for value in history]
                authors[i, -len(history) :] = [value[2] for value in history]
                outcomes[i, -len(history) :] = [value[3] for value in history]
                primary_tags[i, -len(history) :] = [value[4] for value in history]
        return video, tags, authors, outcomes, primary_tags

    def frozen_negative_history(rows):
        video = np.zeros((len(rows), history_length), dtype=np.int32)
        tags = np.zeros((len(rows), history_length), dtype=np.int32)
        for i, row in enumerate(rows):
            history = negative_histories[row["user"]]
            if history:
                video[i, -len(history) :] = [value[0] for value in history]
                tags[i, -len(history) :] = [value[1] for value in history]
        return video, tags

    (
        valid_history,
        valid_history_tags,
        valid_history_authors,
        valid_history_outcomes,
        valid_history_primary_tags,
    ) = frozen_history(splits["valid"])
    (
        test_history,
        test_history_tags,
        test_history_authors,
        test_history_outcomes,
        test_history_primary_tags,
    ) = frozen_history(splits["test"])
    valid_negative_history, valid_negative_history_tags = frozen_negative_history(
        splits["valid"]
    )
    test_negative_history, test_negative_history_tags = frozen_negative_history(
        splits["test"]
    )
    random_histories = None
    random_negative_histories = None
    if args.evaluate_random:
        random_histories = frozen_history(splits["random"])
        random_negative_histories = frozen_negative_history(splits["random"])

    class HistoryRanker(nn.Module):
        def __init__(self):
            super().__init__()
            self.embeddings = nn.ModuleList(
                [nn.Embedding(dimension, args.embedding_dim, padding_idx=0) for dimension in dimensions]
            )
            self.linear_embeddings = nn.ModuleList(
                [nn.Embedding(dimension, 1, padding_idx=0) for dimension in dimensions]
            )
            for embedding in self.embeddings:
                nn.init.normal_(embedding.weight, mean=0.0, std=0.01)
                with torch.no_grad():
                    embedding.weight[0].zero_()
            for embedding in self.linear_embeddings:
                nn.init.zeros_(embedding.weight)
            self.bias = nn.Parameter(torch.zeros(()))
            self.caption_embedding = None
            self.caption_projection = None
            if caption_matrix is not None:
                self.caption_embedding = nn.Embedding.from_pretrained(
                    torch.from_numpy(caption_matrix),
                    freeze=True,
                    padding_idx=0,
                )
                self.caption_projection = nn.Linear(16, args.embedding_dim, bias=False)
                nn.init.normal_(self.caption_projection.weight, mean=0.0, std=0.01)
            self.din_attention = None
            self.negative_din_attention = None
            if args.attention_mode == "din":
                self.din_attention = nn.Sequential(
                    nn.Linear(4 * args.embedding_dim, 64),
                    nn.PReLU(),
                    nn.Linear(64, 1),
                )
                if has_secondary_history:
                    self.negative_din_attention = nn.Sequential(
                        nn.Linear(4 * args.embedding_dim, 64),
                        nn.PReLU(),
                        nn.Linear(64, 1),
                    )
            self.outcome_embedding = None
            self.behavior_embeddings = None
            if args.history_behavior_signals:
                self.behavior_embeddings = nn.ModuleList(
                    [nn.Embedding(2, args.embedding_dim) for _ in behavior_names]
                )
                for embedding in self.behavior_embeddings:
                    nn.init.zeros_(embedding.weight)
                    nn.init.normal_(embedding.weight[1], mean=0.0, std=0.01)
            elif args.history_event == "all":
                self.outcome_embedding = nn.Embedding(3, args.embedding_dim, padding_idx=0)
                nn.init.normal_(self.outcome_embedding.weight, mean=0.0, std=0.01)
                with torch.no_grad():
                    self.outcome_embedding.weight[0].zero_()
            self.history_gru = None
            self.history_transformer = None
            self.history_position_embedding = None
            if args.sequence_encoder == "gru":
                self.history_gru = nn.GRU(
                    args.embedding_dim,
                    args.embedding_dim,
                    batch_first=True,
                )
            elif args.sequence_encoder == "transformer":
                (
                    self.history_position_embedding,
                    self.history_transformer,
                ) = build_causal_history_transformer(
                    args.embedding_dim,
                    history_length,
                    args.dropout,
                )
            width = (
                len(fields) * args.embedding_dim
                + 3 * args.embedding_dim
                + len(aggregate_feature_names)
            )
            if has_secondary_history:
                width += 3 * args.embedding_dim
            if args.dual_timescale_history:
                width += 3 * args.embedding_dim
            if args.hard_history_expert:
                width += 3 * args.embedding_dim
            if args.history_match_features:
                width += 4
            self.cross_network = None
            self.deep_network = None
            self.cross_head = None
            self.task_protected_extraction = None
            if args.cross_layers:
                self.network = None
                self.shared_network = self.main_head = self.auxiliary_head = None
                self.cross_network = nn.ModuleList(
                    [nn.Linear(width, width) for _ in range(args.cross_layers)]
                )
                self.deep_network = nn.Sequential(
                    nn.Linear(width, args.hidden_dim),
                    nn.ReLU(),
                    nn.Dropout(args.dropout),
                    nn.Linear(args.hidden_dim, args.hidden_dim // 2),
                    nn.ReLU(),
                    nn.Dropout(args.dropout),
                )
                self.cross_head = nn.Linear(width + args.hidden_dim // 2, 1)
            elif args.auxiliary_task == "none":
                self.network = nn.Sequential(
                    nn.Linear(width, args.hidden_dim),
                    nn.ReLU(),
                    nn.Dropout(args.dropout),
                    nn.Linear(args.hidden_dim, args.hidden_dim // 2),
                    nn.ReLU(),
                    nn.Dropout(args.dropout),
                    nn.Linear(args.hidden_dim // 2, 1),
                )
                self.shared_network = self.main_head = self.auxiliary_head = None
            elif args.auxiliary_architecture == "shared":
                self.network = None
                self.shared_network = nn.Sequential(
                    nn.Linear(width, args.hidden_dim),
                    nn.ReLU(),
                    nn.Dropout(args.dropout),
                    nn.Linear(args.hidden_dim, args.hidden_dim // 2),
                    nn.ReLU(),
                    nn.Dropout(args.dropout),
                )
                self.main_head = nn.Linear(args.hidden_dim // 2, 1)
                self.auxiliary_head = nn.Linear(args.hidden_dim // 2, 1)
            else:
                assert args.auxiliary_architecture == "task_protected"
                self.network = None
                self.shared_network = self.main_head = self.auxiliary_head = None
                self.task_protected_extraction = build_task_protected_extraction(
                    width,
                    args.hidden_dim,
                    args.dropout,
                )

        def forward(
            self,
            x,
            history,
            history_tags,
            history_authors,
            history_outcomes,
            history_primary_tags,
            negative_history,
            negative_history_tags,
            aggregate_features,
            return_auxiliary=False,
        ):
            embedded = [embedding(x[:, j]) for j, embedding in enumerate(self.embeddings)]
            if self.training and args.id_embedding_dropout > 0:
                keep = 1.0 - args.id_embedding_dropout
                for index in (0, 1):
                    mask = torch.empty(
                        (embedded[index].shape[0], 1),
                        device=embedded[index].device,
                    ).bernoulli_(keep)
                    embedded[index] = embedded[index] * mask / keep
            candidate = embedded[1] + (embedded[3] if args.history_tags else 0.0)
            if args.history_authors:
                candidate = candidate + embedded[2]
            if args.history_primary_tag:
                candidate = candidate + embedded[fields.index("tag1")]
            if args.history_categories:
                candidate = candidate + embedded[fields.index("category_path")]
            historical = self.embeddings[1](history)
            if self.caption_embedding is not None:
                assert self.caption_projection is not None
                candidate = candidate + self.caption_projection(self.caption_embedding(x[:, 1]))
                historical = historical + self.caption_projection(
                    self.caption_embedding(history)
                )
            if args.history_tags:
                historical = historical + self.embeddings[3](history_tags)
            if args.history_authors:
                historical = historical + self.embeddings[2](history_authors)
            if self.outcome_embedding is not None:
                historical = historical + self.outcome_embedding(history_outcomes)
            if self.behavior_embeddings is not None:
                packed = (history_outcomes - 1).clamp_min(0)
                for bit, embedding in enumerate(self.behavior_embeddings):
                    historical = historical + embedding((packed >> bit) & 1)
            if args.history_primary_tag:
                historical = historical + self.embeddings[fields.index("tag1")](history_primary_tags)
            if args.history_categories:
                historical = historical + self.embeddings[fields.index("category_path")](
                    history_primary_tags
                )
            mask = history.ne(0)
            if self.history_gru is not None:
                length = mask.sum(1)
                position = torch.arange(history.shape[1], device=history.device)[None, :]
                source = (history.shape[1] - length[:, None] + position).clamp_max(history.shape[1] - 1)
                historical = historical.gather(
                    1, source[:, :, None].expand(-1, -1, historical.shape[-1])
                )
                mask = position < length[:, None]
                historical = historical * mask[:, :, None]
                historical, _ = self.history_gru(historical)
            elif self.history_transformer is not None:
                assert self.history_position_embedding is not None
                historical = encode_causal_history(
                    self.history_transformer,
                    self.history_position_embedding,
                    historical,
                    mask,
                )
            if args.attention_mode == "din":
                assert self.din_attention is not None
                target = candidate[:, None, :].expand_as(historical)
                attention_features = torch.cat(
                    [historical, target, historical - target, historical * target],
                    dim=-1,
                )
                attention_logits = self.din_attention(attention_features).squeeze(-1)
            else:
                attention_logits = (historical * candidate[:, None, :]).sum(-1) / math.sqrt(args.embedding_dim)
            if args.recency_half_life_events > 0:
                recency_rank = torch.arange(
                    history.shape[1] - 1,
                    -1,
                    -1,
                    device=history.device,
                    dtype=attention_logits.dtype,
                )
                attention_logits = attention_logits - (
                    math.log(2.0) * recency_rank[None, :] / args.recency_half_life_events
                )
            attention_logits = attention_logits.masked_fill(~mask, -1e4)
            attention = torch.softmax(attention_logits, dim=1) * mask
            attention = attention / attention.sum(1, keepdim=True).clamp_min(1e-6)
            profile = (historical * attention[:, :, None]).sum(1)
            combined_parts = embedded + [profile, candidate * profile, torch.abs(candidate - profile)]
            if args.dual_timescale_history:
                recent_positions = torch.arange(
                    history.shape[1],
                    device=history.device,
                ) >= history.shape[1] - DUAL_RECENT_HISTORY_LENGTH
                recent_mask = mask & recent_positions[None, :]
                recent_profile = masked_attention_profile(
                    historical,
                    attention_logits,
                    recent_mask,
                )
                combined_parts.extend(
                    [
                        recent_profile,
                        candidate * recent_profile,
                        torch.abs(candidate - recent_profile),
                    ]
                )
            if args.hard_history_expert:
                hard_profile = hard_attention_profile(
                    historical,
                    attention_logits,
                    mask,
                )
                combined_parts.extend(
                    [
                        hard_profile,
                        candidate * hard_profile,
                        torch.abs(candidate - hard_profile),
                    ]
                )
            negative_profile = None
            if has_secondary_history:
                negative_historical = self.embeddings[1](negative_history)
                if self.caption_embedding is not None:
                    assert self.caption_projection is not None
                    negative_historical = negative_historical + self.caption_projection(
                        self.caption_embedding(negative_history)
                    )
                if args.history_tags:
                    negative_historical = negative_historical + self.embeddings[3](
                        negative_history_tags
                    )
                negative_mask = negative_history.ne(0)
                if args.attention_mode == "din":
                    assert self.negative_din_attention is not None
                    negative_target = candidate[:, None, :].expand_as(
                        negative_historical
                    )
                    negative_attention_features = torch.cat(
                        [
                            negative_historical,
                            negative_target,
                            negative_historical - negative_target,
                            negative_historical * negative_target,
                        ],
                        dim=-1,
                    )
                    negative_attention_logits = self.negative_din_attention(
                        negative_attention_features
                    ).squeeze(-1)
                else:
                    negative_attention_logits = (
                        negative_historical * candidate[:, None, :]
                    ).sum(-1) / math.sqrt(args.embedding_dim)
                negative_attention_logits = negative_attention_logits.masked_fill(
                    ~negative_mask, -1e4
                )
                negative_attention = torch.softmax(
                    negative_attention_logits, dim=1
                ) * negative_mask
                negative_attention = negative_attention / negative_attention.sum(
                    1, keepdim=True
                ).clamp_min(1e-6)
                negative_profile = (
                    negative_historical * negative_attention[:, :, None]
                ).sum(1)
                combined_parts.extend(
                    [
                        negative_profile,
                        candidate * negative_profile,
                        torch.abs(candidate - negative_profile),
                    ]
                )
            if aggregate_features.shape[1]:
                combined_parts.append(aggregate_features)
            if args.history_match_features:
                count = mask.sum(1).clamp_min(1).to(candidate.dtype)
                video_match = ((history == x[:, 1:2]) & mask).sum(1).to(candidate.dtype) / count
                tag_match = ((history_tags == x[:, 3:4]) & mask).sum(1).to(candidate.dtype) / count
                recent_mask = mask[:, -5:]
                recent_count = recent_mask.sum(1).clamp_min(1).to(candidate.dtype)
                recent_tag_match = (
                    ((history_tags[:, -5:] == x[:, 3:4]) & recent_mask).sum(1).to(candidate.dtype)
                    / recent_count
                )
                normalized_count = torch.log1p(count) / math.log1p(history.shape[1])
                combined_parts.append(
                    torch.stack(
                        [normalized_count, video_match, tag_match, recent_tag_match],
                        dim=1,
                    )
                )
            combined = torch.cat(combined_parts, dim=1)
            auxiliary = None
            if self.cross_network is not None:
                assert self.deep_network is not None and self.cross_head is not None
                crossed = combined
                for layer in self.cross_network:
                    crossed = combined * layer(crossed) + crossed
                deep = self.deep_network(combined)
                output = self.cross_head(torch.cat([crossed, deep], dim=1)).squeeze(1)
            elif self.task_protected_extraction is not None:
                output, auxiliary = self.task_protected_extraction(combined)
            elif self.shared_network is None:
                assert self.network is not None
                output = self.network(combined).squeeze(1)
            else:
                assert self.main_head is not None and self.auxiliary_head is not None
                shared = self.shared_network(combined)
                output = self.main_head(shared).squeeze(1)
                auxiliary = self.auxiliary_head(shared).squeeze(1)
            if args.nn_fm_term:
                fm_fields = torch.stack(embedded + [profile], dim=1)
                summed = fm_fields.sum(1)
                fm = 0.5 * ((summed * summed).sum(1) - (fm_fields * fm_fields).sum((1, 2)))
                linear = torch.stack(
                    [embedding(x[:, j]).squeeze(1) for j, embedding in enumerate(self.linear_embeddings)],
                    dim=1,
                ).sum(1)
                output = output + self.bias + linear + fm
            return (output, auxiliary) if return_auxiliary else output

    torch.manual_seed(args.seed)
    device = torch.device("mps" if args.device == "auto" and torch.backends.mps.is_available() else args.device)
    model = HistoryRanker().to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.nn_lr, weight_decay=args.nn_weight_decay)
    loss_fn = nn.BCEWithLogitsLoss()
    training_weights = np.ones(len(train), dtype=np.float32)
    if args.user_balance_alpha > 0:
        user_counts = collections.Counter(row["user"] for row in train)
        training_weights = np.asarray(
            [user_counts[row["user"]] ** (-args.user_balance_alpha) for row in train],
            dtype=np.float32,
        )
        training_weights /= training_weights.mean()
    if args.date_decay_half_life_days > 0:
        newest_train_day = max(
            dt.datetime.strptime(str(row["date"]), "%Y%m%d").date() for row in train
        )
        date_weights = np.asarray(
            [
                0.5
                ** (
                    (newest_train_day - dt.datetime.strptime(str(row["date"]), "%Y%m%d").date()).days
                    / args.date_decay_half_life_days
                )
                for row in train
            ],
            dtype=np.float32,
        )
        training_weights *= date_weights
        training_weights /= training_weights.mean()
    auxiliary_targets = None
    auxiliary_durations = None
    if args.auxiliary_task == "watch_ratio":
        auxiliary_targets = np.asarray(
            [min(row["play_time"] / max(row["duration"], 1.0), 1.0) for row in train],
            dtype=np.float32,
        )
    elif args.auxiliary_task == "click":
        auxiliary_targets = np.asarray([row["click"] for row in train], dtype=np.float32)
    elif args.auxiliary_task == "cwm":
        # The CWM reference rounds milliseconds to seconds and right-censors
        # play time at video duration before applying its likelihood.
        auxiliary_targets = np.asarray(
            [round(min(row["play_time"], row["duration"]) / 1000.0) for row in train],
            dtype=np.float32,
        )
        auxiliary_durations = np.asarray(
            [round(row["duration"] / 1000.0) for row in train],
            dtype=np.float32,
        )

    def within_user_standardize(scores):
        by_user = collections.defaultdict(list)
        for i, user in enumerate(valid_users):
            by_user[user].append(i)
        normalized = np.empty(len(scores), dtype=np.float32)
        for indices in by_user.values():
            values = np.asarray(scores)[indices]
            scale = float(values.std())
            normalized[indices] = (values - values.mean()) / (scale if scale > 1e-6 else 1.0)
        return normalized

    base_scores = None
    base_metric = None
    if args.ensemble_alpha > 0:
        official_splits = organizer_load(args.data_dir)
        official_enc, official_dim = organizer_encode(official_splits)
        Xbase_tr, ybase_tr, _ = official_enc["train"]
        Xbase_va, ybase_va, ubase_va = official_enc["valid"]
        base_model = OrganizerFM(official_dim, k=16, lr=0.001, l2=1e-6, seed=0)
        base_rng = np.random.default_rng(0)
        base_best, base_state, base_bad = -1.0, None, 0
        for _ in range(40):
            order = base_rng.permutation(len(ybase_tr))
            for start in range(0, len(order), 8192):
                ix = order[start : start + 8192]
                base_model.step(Xbase_tr[ix], ybase_tr[ix])
            metric = evaluate(ubase_va, ybase_va, base_model.predict(Xbase_va))
            if metric["primary"] > base_best + 1e-5:
                base_best, base_bad = metric["primary"], 0
                base_state = (base_model.V.copy(), base_model.W.copy(), np.float32(base_model.b))
            else:
                base_bad += 1
                if base_bad >= 4:
                    break
        base_model.V, base_model.W, base_model.b = base_state
        base_scores = base_model.predict(Xbase_va)
        base_metric = evaluate(ubase_va, ybase_va, base_scores)
        base_scores = within_user_standardize(base_scores)

    def predict(
        X,
        history,
        history_tags,
        history_authors,
        history_outcomes,
        history_primary_tags,
        negative_history,
        negative_history_tags,
        aggregate_features,
    ):
        model.eval()
        output = []
        with torch.no_grad():
            for start in range(0, len(X), args.nn_batch_size):
                xb = torch.from_numpy(X[start : start + args.nn_batch_size].astype(np.int64)).to(device)
                hb = torch.from_numpy(history[start : start + args.nn_batch_size].astype(np.int64)).to(device)
                htb = torch.from_numpy(history_tags[start : start + args.nn_batch_size].astype(np.int64)).to(device)
                hab = torch.from_numpy(history_authors[start : start + args.nn_batch_size].astype(np.int64)).to(device)
                hob = torch.from_numpy(history_outcomes[start : start + args.nn_batch_size].astype(np.int64)).to(device)
                hpb = torch.from_numpy(history_primary_tags[start : start + args.nn_batch_size].astype(np.int64)).to(device)
                nhb = torch.from_numpy(
                    negative_history[start : start + args.nn_batch_size].astype(np.int64)
                ).to(device)
                nhtb = torch.from_numpy(
                    negative_history_tags[start : start + args.nn_batch_size].astype(np.int64)
                ).to(device)
                ab = torch.from_numpy(
                    aggregate_features[start : start + args.nn_batch_size].astype(np.float32)
                ).to(device)
                output.append(
                    model(xb, hb, htb, hab, hob, hpb, nhb, nhtb, ab).cpu().numpy()
                )
        return np.concatenate(output)

    rng = np.random.default_rng(args.seed)
    best, best_state, bad = -1.0, None, 0
    trace = []
    for epoch in range(1, args.nn_epochs + 1):
        model.train()
        order = rng.permutation(len(ytr))
        losses = []
        for start in range(0, len(order), args.nn_batch_size):
            ix = order[start : start + args.nn_batch_size]
            xb = torch.from_numpy(Xtr[ix].astype(np.int64)).to(device)
            hb = torch.from_numpy(train_history[ix].astype(np.int64)).to(device)
            htb = torch.from_numpy(train_history_tags[ix].astype(np.int64)).to(device)
            hab = torch.from_numpy(train_history_authors[ix].astype(np.int64)).to(device)
            hob = torch.from_numpy(train_history_outcomes[ix].astype(np.int64)).to(device)
            hpb = torch.from_numpy(train_history_primary_tags[ix].astype(np.int64)).to(device)
            nhb = torch.from_numpy(train_negative_history[ix].astype(np.int64)).to(device)
            nhtb = torch.from_numpy(train_negative_history_tags[ix].astype(np.int64)).to(device)
            ab = torch.from_numpy(aggregate_train[ix].astype(np.float32)).to(device)
            yb = torch.from_numpy(ytr[ix]).to(device)
            optimizer.zero_grad(set_to_none=True)
            if auxiliary_targets is None:
                prediction = model(xb, hb, htb, hab, hob, hpb, nhb, nhtb, ab)
                example_loss = torch.nn.functional.binary_cross_entropy_with_logits(
                    prediction, yb, reduction="none"
                )
                batch_weights = torch.from_numpy(training_weights[ix]).to(device)
                loss = (example_loss * batch_weights).mean()
            else:
                prediction, auxiliary_prediction = model(
                    xb,
                    hb,
                    htb,
                    hab,
                    hob,
                    hpb,
                    nhb,
                    nhtb,
                    ab,
                    return_auxiliary=True,
                )
                assert auxiliary_prediction is not None
                auxiliary_target = torch.from_numpy(auxiliary_targets[ix]).to(device)
                if args.auxiliary_task == "watch_ratio":
                    auxiliary_loss = torch.nn.functional.mse_loss(
                        torch.sigmoid(auxiliary_prediction), auxiliary_target
                    )
                elif args.auxiliary_task == "click":
                    auxiliary_loss = loss_fn(auxiliary_prediction, auxiliary_target)
                else:
                    assert args.auxiliary_task == "cwm" and auxiliary_durations is not None
                    duration = torch.from_numpy(auxiliary_durations[ix]).to(device)
                    interest = torch.exp(-args.cwm_c_inverse / (auxiliary_target + 1.0))
                    interest = interest.clamp(1e-6, 1.0 - 1e-6)
                    threshold = torch.logit(interest)
                    complete = auxiliary_target >= duration
                    cwm_parts = []
                    if (~complete).any():
                        cwm_parts.append(
                            torch.square(auxiliary_prediction[~complete] - threshold[~complete]).mean()
                            / (2.0 * args.cwm_sigma**2)
                        )
                    if complete.any():
                        cwm_parts.append(
                            -torch.nn.functional.logsigmoid(
                                (auxiliary_prediction[complete] - threshold[complete])
                                / args.cwm_sigma
                            ).mean()
                        )
                    auxiliary_loss = sum(cwm_parts)
                example_loss = torch.nn.functional.binary_cross_entropy_with_logits(
                    prediction, yb, reduction="none"
                )
                batch_weights = torch.from_numpy(training_weights[ix]).to(device)
                loss = (example_loss * batch_weights).mean() + args.auxiliary_weight * auxiliary_loss
            loss.backward()
            optimizer.step()
            losses.append(float(loss.detach().cpu()))
        validation_scores = predict(
            Xva, valid_history, valid_history_tags, valid_history_authors, valid_history_outcomes,
            valid_history_primary_tags, valid_negative_history, valid_negative_history_tags,
            aggregate_valid
        )
        raw_metric = evaluate(valid_users, yva, validation_scores)
        if base_scores is not None:
            combined_scores = base_scores + args.ensemble_alpha * within_user_standardize(validation_scores)
            metric = evaluate(valid_users, yva, combined_scores)
        else:
            metric = raw_metric
        trace.append({"epoch": epoch, "loss": float(np.mean(losses)), "valid": metric, "raw_sequence_valid": raw_metric})
        print(
            f"epoch {epoch:2d} loss {np.mean(losses):.5f} GAUC {metric['GAUC']:.5f} "
            f"nDCG@5 {metric['nDCG@5']:.5f} primary {metric['primary']:.5f}",
            flush=True,
        )
        if metric["primary"] > best + 1e-5:
            best = metric["primary"]
            best_state = {key: value.detach().cpu().clone() for key, value in model.state_dict().items()}
            bad = 0
        else:
            bad += 1
            if bad >= args.nn_patience:
                break
    model.load_state_dict(best_state)
    if args.nn_bpr_epochs > 0:
        pair_optimizer = torch.optim.AdamW(
            model.parameters(),
            lr=args.nn_bpr_lr,
            weight_decay=args.nn_weight_decay,
        )
        by_user = collections.defaultdict(lambda: [[], []])
        for i, (row, label) in enumerate(zip(train, ytr)):
            by_user[row["user"]][int(label)].append(i)
        usable = [
            (np.asarray(values[1], dtype=np.int64), np.asarray(values[0], dtype=np.int64))
            for values in by_user.values()
            if values[0] and values[1]
        ]
        if args.nn_bpr_sampling == "hard":
            training_scores = predict(
                Xtr,
                train_history,
                train_history_tags,
                train_history_authors,
                train_history_outcomes,
                train_history_primary_tags,
                train_negative_history,
                train_negative_history_tags,
                aggregate_train,
            )
            restricted = []
            for positives, negatives in usable:
                count = max(1, math.ceil(len(negatives) * args.nn_bpr_hard_fraction))
                hard = negatives[np.argsort(training_scores[negatives])[-count:]]
                restricted.append((positives, hard))
            usable = restricted
        pair_bad = 0
        for epoch in range(1, args.nn_bpr_epochs + 1):
            model.train()
            positive = np.concatenate([p for p, _ in usable])
            negative = np.concatenate([rng.choice(n, size=len(p), replace=True) for p, n in usable])
            order = rng.permutation(len(positive))
            positive, negative = positive[order], negative[order]
            losses = []
            for start in range(0, len(positive), args.nn_bpr_batch_size):
                p = positive[start : start + args.nn_bpr_batch_size]
                n = negative[start : start + args.nn_bpr_batch_size]
                xp = torch.from_numpy(Xtr[p].astype(np.int64)).to(device)
                hp = torch.from_numpy(train_history[p].astype(np.int64)).to(device)
                htp = torch.from_numpy(train_history_tags[p].astype(np.int64)).to(device)
                hap = torch.from_numpy(train_history_authors[p].astype(np.int64)).to(device)
                hop = torch.from_numpy(train_history_outcomes[p].astype(np.int64)).to(device)
                hpp = torch.from_numpy(train_history_primary_tags[p].astype(np.int64)).to(device)
                nhp = torch.from_numpy(train_negative_history[p].astype(np.int64)).to(device)
                nhtp = torch.from_numpy(train_negative_history_tags[p].astype(np.int64)).to(device)
                ap = torch.from_numpy(aggregate_train[p].astype(np.float32)).to(device)
                xn = torch.from_numpy(Xtr[n].astype(np.int64)).to(device)
                hn = torch.from_numpy(train_history[n].astype(np.int64)).to(device)
                htn = torch.from_numpy(train_history_tags[n].astype(np.int64)).to(device)
                han = torch.from_numpy(train_history_authors[n].astype(np.int64)).to(device)
                hon = torch.from_numpy(train_history_outcomes[n].astype(np.int64)).to(device)
                hpn = torch.from_numpy(train_history_primary_tags[n].astype(np.int64)).to(device)
                nhn = torch.from_numpy(train_negative_history[n].astype(np.int64)).to(device)
                nhtn = torch.from_numpy(train_negative_history_tags[n].astype(np.int64)).to(device)
                an = torch.from_numpy(aggregate_train[n].astype(np.float32)).to(device)
                pair_optimizer.zero_grad(set_to_none=True)
                loss = torch.nn.functional.softplus(
                    -(
                        model(xp, hp, htp, hap, hop, hpp, nhp, nhtp, ap)
                        - model(xn, hn, htn, han, hon, hpn, nhn, nhtn, an)
                    )
                ).mean()
                loss.backward()
                pair_optimizer.step()
                losses.append(float(loss.detach().cpu()))
            validation_scores = predict(
                Xva, valid_history, valid_history_tags, valid_history_authors, valid_history_outcomes,
                valid_history_primary_tags, valid_negative_history,
                valid_negative_history_tags, aggregate_valid
            )
            metric = evaluate(valid_users, yva, validation_scores)
            trace.append({"stage": "neural_bpr", "epoch": epoch, "loss": float(np.mean(losses)), "valid": metric})
            print(
                f"neural BPR {epoch:2d} loss {np.mean(losses):.5f} GAUC {metric['GAUC']:.5f} "
                f"nDCG@5 {metric['nDCG@5']:.5f} primary {metric['primary']:.5f}",
                flush=True,
            )
            if metric["primary"] > best + 1e-5:
                best = metric["primary"]
                best_state = {key: value.detach().cpu().clone() for key, value in model.state_dict().items()}
                pair_bad = 0
            else:
                pair_bad += 1
                if pair_bad >= args.nn_bpr_patience:
                    break
        model.load_state_dict(best_state)
    if args.nn_lambda_epochs > 0:
        lambda_optimizer = torch.optim.AdamW(
            model.parameters(),
            lr=args.nn_lambda_lr,
            weight_decay=args.nn_weight_decay,
        )
        user_indices = collections.defaultdict(list)
        for i, row in enumerate(train):
            user_indices[row["user"]].append(i)
        training_scores = predict(
            Xtr,
            train_history,
            train_history_tags,
            train_history_authors,
            train_history_outcomes,
            train_history_primary_tags,
            train_negative_history,
            train_negative_history_tags,
            aggregate_train,
        )
        lambda_users = []
        for indices in user_indices.values():
            indices = np.asarray(indices, dtype=np.int64)
            positives = indices[ytr[indices] > 0]
            negatives = indices[ytr[indices] <= 0]
            if not len(positives) or not len(negatives):
                continue
            # Approximate the head of the current ranked list with the hardest
            # negatives; positives are resampled each epoch for coverage.
            negatives = negatives[np.argsort(training_scores[negatives])[::-1]]
            if args.nn_lambda_max_negatives > 0:
                negatives = negatives[: args.nn_lambda_max_negatives]
            lambda_users.append((positives, negatives))
        lambda_bad = 0
        for epoch in range(1, args.nn_lambda_epochs + 1):
            model.train()
            rng.shuffle(lambda_users)
            losses = []
            for start in range(0, len(lambda_users), args.nn_lambda_batch_users):
                groups = []
                shapes = []
                for positives, negatives in lambda_users[
                    start : start + args.nn_lambda_batch_users
                ]:
                    selected_positives = positives
                    if (
                        args.nn_lambda_max_positives > 0
                        and len(positives) > args.nn_lambda_max_positives
                    ):
                        selected_positives = rng.choice(
                            positives,
                            size=args.nn_lambda_max_positives,
                            replace=False,
                        )
                    groups.append(np.concatenate([selected_positives, negatives]))
                    shapes.append((len(selected_positives), len(negatives)))
                indices = np.concatenate(groups)
                xb = torch.from_numpy(Xtr[indices].astype(np.int64)).to(device)
                hb = torch.from_numpy(train_history[indices].astype(np.int64)).to(device)
                htb = torch.from_numpy(train_history_tags[indices].astype(np.int64)).to(device)
                hab = torch.from_numpy(train_history_authors[indices].astype(np.int64)).to(device)
                hob = torch.from_numpy(train_history_outcomes[indices].astype(np.int64)).to(device)
                hpb = torch.from_numpy(train_history_primary_tags[indices].astype(np.int64)).to(device)
                nhb = torch.from_numpy(train_negative_history[indices].astype(np.int64)).to(device)
                nhtb = torch.from_numpy(train_negative_history_tags[indices].astype(np.int64)).to(device)
                ab = torch.from_numpy(aggregate_train[indices].astype(np.float32)).to(device)
                scores = model(xb, hb, htb, hab, hob, hpb, nhb, nhtb, ab)
                lambda_optimizer.zero_grad(set_to_none=True)
                auc_numerator = scores.new_zeros(())
                positive_total = 0
                ndcg_losses = []
                offset = 0
                for positive_count, negative_count in shapes:
                    size = positive_count + negative_count
                    group_scores = scores[offset : offset + size]
                    offset += size
                    positive_scores = group_scores[:positive_count]
                    negative_scores = group_scores[positive_count:]
                    pair_loss = torch.nn.functional.softplus(
                        -(positive_scores[:, None] - negative_scores[None, :])
                    )
                    auc_numerator = auc_numerator + positive_count * pair_loss.mean()
                    positive_total += positive_count

                    detached_order = torch.argsort(group_scores.detach(), descending=True)
                    ranks = torch.empty_like(detached_order)
                    ranks[detached_order] = torch.arange(size, device=device)
                    discounts = torch.where(
                        ranks < 5,
                        1.0 / torch.log2(ranks.to(scores.dtype) + 2.0),
                        torch.zeros(size, device=device, dtype=scores.dtype),
                    )
                    ideal_count = min(positive_count, 5)
                    ideal_ranks = torch.arange(ideal_count, device=device, dtype=scores.dtype)
                    ideal_dcg = (1.0 / torch.log2(ideal_ranks + 2.0)).sum()
                    delta_ndcg = torch.abs(
                        discounts[:positive_count, None]
                        - discounts[positive_count:, None].transpose(0, 1)
                    ) / ideal_dcg.clamp_min(1e-6)
                    ndcg_losses.append(
                        (delta_ndcg * pair_loss).sum() / delta_ndcg.sum().clamp_min(1e-6)
                    )
                # Mirror the official primary: positive-weighted user AUC and
                # equally weighted per-user nDCG@5 contribute one half each.
                loss = 0.5 * auc_numerator / max(positive_total, 1) + 0.5 * torch.stack(
                    ndcg_losses
                ).mean()
                loss.backward()
                lambda_optimizer.step()
                losses.append(float(loss.detach().cpu()))
            validation_scores = predict(
                Xva,
                valid_history,
                valid_history_tags,
                valid_history_authors,
                valid_history_outcomes,
                valid_history_primary_tags,
                valid_negative_history,
                valid_negative_history_tags,
                aggregate_valid,
            )
            metric = evaluate(valid_users, yva, validation_scores)
            trace.append(
                {
                    "stage": "neural_lambdaloss",
                    "epoch": epoch,
                    "loss": float(np.mean(losses)),
                    "valid": metric,
                }
            )
            print(
                f"neural LambdaLoss {epoch:2d} loss {np.mean(losses):.5f} "
                f"GAUC {metric['GAUC']:.5f} nDCG@5 {metric['nDCG@5']:.5f} "
                f"primary {metric['primary']:.5f}",
                flush=True,
            )
            if metric["primary"] > best + 1e-5:
                best = metric["primary"]
                best_state = {
                    key: value.detach().cpu().clone()
                    for key, value in model.state_dict().items()
                }
                lambda_bad = 0
            else:
                lambda_bad += 1
                if lambda_bad >= args.nn_lambda_patience:
                    break
        model.load_state_dict(best_state)
    if args.nn_listwise_epochs > 0:
        list_optimizer = torch.optim.AdamW(
            model.parameters(),
            lr=args.nn_listwise_lr,
            weight_decay=args.nn_weight_decay,
        )
        user_indices = collections.defaultdict(list)
        for i, row in enumerate(train):
            user_indices[row["user"]].append(i)
        usable_users = []
        for indices in user_indices.values():
            indices = np.asarray(indices, dtype=np.int64)
            positives = indices[ytr[indices] > 0]
            negatives = indices[ytr[indices] <= 0]
            if len(positives) and len(negatives):
                usable_users.append((positives, negatives))
        list_bad = 0
        for epoch in range(1, args.nn_listwise_epochs + 1):
            model.train()
            rng.shuffle(usable_users)
            losses = []
            for start in range(0, len(usable_users), args.nn_listwise_batch_users):
                groups = []
                for positives, negatives in usable_users[
                    start : start + args.nn_listwise_batch_users
                ]:
                    if args.nn_listwise_max_positives > 0 and len(positives) > args.nn_listwise_max_positives:
                        positives = rng.choice(
                            positives,
                            size=args.nn_listwise_max_positives,
                            replace=False,
                        )
                    if args.nn_listwise_max_negatives > 0 and len(negatives) > args.nn_listwise_max_negatives:
                        negatives = rng.choice(
                            negatives,
                            size=args.nn_listwise_max_negatives,
                            replace=False,
                        )
                    groups.append(np.concatenate([positives, negatives]))
                indices = np.concatenate(groups)
                xb = torch.from_numpy(Xtr[indices].astype(np.int64)).to(device)
                hb = torch.from_numpy(train_history[indices].astype(np.int64)).to(device)
                htb = torch.from_numpy(train_history_tags[indices].astype(np.int64)).to(device)
                hab = torch.from_numpy(train_history_authors[indices].astype(np.int64)).to(device)
                hob = torch.from_numpy(train_history_outcomes[indices].astype(np.int64)).to(device)
                hpb = torch.from_numpy(train_history_primary_tags[indices].astype(np.int64)).to(device)
                nhb = torch.from_numpy(train_negative_history[indices].astype(np.int64)).to(device)
                nhtb = torch.from_numpy(train_negative_history_tags[indices].astype(np.int64)).to(device)
                ab = torch.from_numpy(aggregate_train[indices].astype(np.float32)).to(device)
                scores = model(xb, hb, htb, hab, hob, hpb, nhb, nhtb, ab)
                list_optimizer.zero_grad(set_to_none=True)
                group_losses = []
                offset = 0
                for group in groups:
                    size = len(group)
                    labels = torch.from_numpy(ytr[group]).to(device)
                    target = labels / labels.sum().clamp_min(1.0)
                    group_losses.append(
                        -(target * torch.log_softmax(scores[offset : offset + size], dim=0)).sum()
                    )
                    offset += size
                loss = torch.stack(group_losses).mean()
                loss.backward()
                list_optimizer.step()
                losses.append(float(loss.detach().cpu()))
            validation_scores = predict(
                Xva, valid_history, valid_history_tags, valid_history_authors, valid_history_outcomes,
                valid_history_primary_tags, valid_negative_history,
                valid_negative_history_tags, aggregate_valid
            )
            metric = evaluate(valid_users, yva, validation_scores)
            trace.append(
                {"stage": "listwise", "epoch": epoch, "loss": float(np.mean(losses)), "valid": metric}
            )
            print(
                f"listwise {epoch:2d} loss {np.mean(losses):.5f} GAUC {metric['GAUC']:.5f} "
                f"nDCG@5 {metric['nDCG@5']:.5f} primary {metric['primary']:.5f}",
                flush=True,
            )
            if metric["primary"] > best + 1e-5:
                best = metric["primary"]
                best_state = {
                    key: value.detach().cpu().clone() for key, value in model.state_dict().items()
                }
                list_bad = 0
            else:
                list_bad += 1
                if list_bad >= args.nn_listwise_patience:
                    break
        model.load_state_dict(best_state)
    validation_scores = predict(
        Xva, valid_history, valid_history_tags, valid_history_authors, valid_history_outcomes,
        valid_history_primary_tags, valid_negative_history, valid_negative_history_tags,
        aggregate_valid
    )
    if base_scores is not None:
        final_scores = base_scores + args.ensemble_alpha * within_user_standardize(validation_scores)
    else:
        final_scores = validation_scores
    result = {
        "variant": args.variant,
        "valid": evaluate(valid_users, yva, final_scores),
        "raw_sequence_valid": evaluate(valid_users, yva, validation_scores),
        "robustness": robustness_slices(train, splits["valid"], final_scores),
        "base_valid": base_metric,
        "trace": trace,
        "fields": fields,
        "aggregate_feature_names": aggregate_feature_names,
        "parameters": {
            "device": str(device),
            "split_mode": args.split_mode,
            "split_bounds": split_bounds,
            "history_length": history_length,
            "dual_timescale_history": args.dual_timescale_history,
            "hard_history_expert": args.hard_history_expert,
            "recent_history_length": (
                DUAL_RECENT_HISTORY_LENGTH if args.dual_timescale_history else None
            ),
            "history_event": args.history_event,
            "secondary_history_event": args.secondary_history_event,
            "negative_history_event": args.negative_history_event,
            "negative_history_watch_ratio_max": (
                STRICT_SKIP_WATCH_RATIO
                if args.negative_history_event == "strict_skip_005"
                else None
            ),
            "history_order": args.history_order,
            "history_tags": args.history_tags,
            "history_authors": args.history_authors,
            "attention_mode": args.attention_mode,
            "recency_half_life_events": args.recency_half_life_events,
            "auxiliary_task": args.auxiliary_task,
            "auxiliary_architecture": args.auxiliary_architecture,
            "auxiliary_weight": args.auxiliary_weight,
            "cwm_c_inverse": args.cwm_c_inverse,
            "cwm_sigma": args.cwm_sigma,
            "history_match_features": args.history_match_features,
            "sequence_encoder": args.sequence_encoder,
            "user_profile_features": args.user_profile_features,
            "history_primary_tag": args.history_primary_tag,
            "history_categories": args.history_categories,
            "category_file": args.category_file if args.history_categories else None,
            "caption_content": args.caption_content,
            "caption_file": args.caption_file if args.caption_content else None,
            "caption_source_sha256": caption_source_sha256,
            "caption_tfidf": (
                {
                    "analyzer": "char",
                    "ngram_range": [2, 4],
                    "min_df": 2,
                    "max_features": 50000,
                    "sublinear_tf": True,
                    "svd_components": 16,
                    "svd_iterations": 7,
                    "svd_seed": 2026,
                    "explained_variance_ratio_sum": caption_explained_variance,
                }
                if args.caption_content
                else None
            ),
            "user_balance_alpha": args.user_balance_alpha,
            "date_decay_half_life_days": args.date_decay_half_life_days,
            "target_rate_features": args.target_rate_features,
            "causal_aggregate_features": args.causal_aggregate_features,
            "causal_repeat_features": args.causal_repeat_features,
            "multi_behavior_context": args.multi_behavior_context,
            "history_behavior_signals": args.history_behavior_signals,
            "time_features": args.time_features,
            "cross_layers": args.cross_layers,
            "embedding_dim": args.embedding_dim,
            "hidden_dim": args.hidden_dim,
            "dropout": args.dropout,
            "id_embedding_dropout": args.id_embedding_dropout,
            "nn_lr": args.nn_lr,
            "nn_weight_decay": args.nn_weight_decay,
            "seed": args.seed,
            "ensemble_alpha": args.ensemble_alpha,
            "nn_fm_term": args.nn_fm_term,
            "nn_bpr_epochs": args.nn_bpr_epochs,
            "nn_bpr_lr": args.nn_bpr_lr,
            "nn_bpr_sampling": args.nn_bpr_sampling,
            "nn_bpr_hard_fraction": args.nn_bpr_hard_fraction,
            "nn_listwise_epochs": args.nn_listwise_epochs,
            "nn_listwise_lr": args.nn_listwise_lr,
            "nn_listwise_max_positives": args.nn_listwise_max_positives,
            "nn_listwise_max_negatives": args.nn_listwise_max_negatives,
            "nn_lambda_epochs": args.nn_lambda_epochs,
            "nn_lambda_lr": args.nn_lambda_lr,
            "nn_lambda_max_positives": args.nn_lambda_max_positives,
            "nn_lambda_max_negatives": args.nn_lambda_max_negatives,
        },
        "elapsed_seconds": time.time() - t0,
        "label_boundary": label_boundary_attestation(args.split_mode == "official"),
    }
    test_scores = None
    if args.evaluate_test or args.predict_test:
        test_scores = predict(
            Xte, test_history, test_history_tags, test_history_authors, test_history_outcomes,
            test_history_primary_tags, test_negative_history,
            test_negative_history_tags, aggregate_test
        )
    if args.evaluate_forward:
        if args.split_mode == "official":
            raise ValueError("--evaluate-forward is only allowed with a shadow split")
        if test_scores is None:
            test_scores = predict(
                Xte, test_history, test_history_tags, test_history_authors, test_history_outcomes,
                test_history_primary_tags, test_negative_history,
                test_negative_history_tags, aggregate_test
            )
        if yte is None:
            raise RuntimeError("forward labels are unavailable")
        result["forward_valid"] = evaluate(
            [r["user"] for r in splits["test"]],
            yte,
            test_scores,
        )
    if args.evaluate_random:
        assert (
            Xrandom is not None
            and yrandom is not None
            and random_histories is not None
            and random_negative_histories is not None
        )
        random_scores = predict(
            Xrandom,
            *random_histories,
            *random_negative_histories,
            aggregate_random,
        )
        result["random_validation"] = evaluate(
            [row["user"] for row in splits["random"]],
            yrandom,
            random_scores,
        )
    if args.model_out:
        Path(args.model_out).parent.mkdir(parents=True, exist_ok=True)
        torch.save(
            {
                "state_dict": best_state,
                "fields": fields,
                "vocabs": vocabs,
                "duration_edges": duration_edges,
                "aggregate_feature_names": aggregate_feature_names,
                "parameters": result["parameters"],
            },
            args.model_out,
        )
    if args.predictions_out:
        Path(args.predictions_out).parent.mkdir(parents=True, exist_ok=True)
        payload = {"valid": np.asarray(final_scores, dtype=np.float32)}
        if test_scores is not None:
            payload["test"] = np.asarray(test_scores, dtype=np.float32)
        if args.evaluate_random:
            payload["random"] = np.asarray(random_scores, dtype=np.float32)
        np.savez_compressed(args.predictions_out, **payload)
    return result


def evaluate_prediction_ensemble(args):
    if len(args.prediction_files) < 2:
        raise ValueError("prediction_ensemble requires at least two --prediction-files")
    members = [np.load(path) for path in args.prediction_files]
    valid_predictions = [member["valid"] for member in members]
    if len({len(values) for values in valid_predictions}) != 1:
        raise ValueError("validation prediction lengths differ")
    splits = load_rows(
        Path(args.data_dir),
        split_bounds=split_bounds_for_mode(args.split_mode),
    )
    valid_rows = splits["valid"]
    valid_users = [row["user"] for row in valid_rows]
    valid_labels = [row["label"] for row in valid_rows]
    test_users = [row["user"] for row in splits["test"]]
    test_labels = (
        [row["label"] for row in splits["test"]]
        if args.split_mode != "official"
        else None
    )

    if args.prediction_weights:
        if args.prediction_ensemble_mode in {"user_median_rank", "user_copeland_rank"}:
            raise ValueError(
                f"{args.prediction_ensemble_mode} does not accept --prediction-weights"
            )
        if len(args.prediction_weights) != len(members):
            raise ValueError("--prediction-weights must match --prediction-files")
        weights = np.asarray(args.prediction_weights, dtype=np.float64)
        if np.any(weights < 0) or not float(weights.sum()) > 0:
            raise ValueError("--prediction-weights must be nonnegative with a positive sum")
    else:
        weights = np.ones(len(members), dtype=np.float64)

    def normalize_within_user(predictions, users_for_rows):
        if args.prediction_ensemble_mode == "mean":
            return predictions
        users = collections.defaultdict(list)
        for index, user in enumerate(users_for_rows):
            users[user].append(index)
        normalized = []
        for prediction in predictions:
            values = np.asarray(prediction, dtype=np.float64)
            transformed = np.empty_like(values)
            for indices in users.values():
                group = values[indices]
                if args.prediction_ensemble_mode == "user_zscore":
                    scale = float(group.std())
                    transformed[indices] = (group - group.mean()) / (scale if scale > 1e-8 else 1.0)
                else:
                    order = np.argsort(group, kind="stable")
                    ranks = np.empty(len(group), dtype=np.float64)
                    ranks[order] = np.arange(len(group), dtype=np.float64)
                    transformed[indices] = ranks / max(len(group) - 1, 1)
            normalized.append(transformed)
        return normalized

    normalized_valid = normalize_within_user(valid_predictions, valid_users)
    if args.prediction_ensemble_mode == "user_median_rank":
        valid_scores = np.median(normalized_valid, axis=0)
    elif args.prediction_ensemble_mode == "user_copeland_rank":
        valid_scores = copeland_rank_consensus(normalized_valid, valid_users)
    else:
        valid_scores = np.average(normalized_valid, axis=0, weights=weights)
    result = {
        "variant": args.variant,
        "members": args.prediction_files,
        "ensemble_mode": args.prediction_ensemble_mode,
        "weights": weights.tolist(),
        "valid": evaluate(
            valid_users,
            valid_labels,
            valid_scores,
        ),
        "label_boundary": label_boundary_attestation(args.split_mode == "official"),
    }
    if args.split_mode != "official":
        result["robustness"] = robustness_slices(splits["train"], valid_rows, valid_scores)
    if args.evaluate_forward:
        if args.split_mode == "official":
            raise ValueError("--evaluate-forward is only allowed with a shadow split")
        if not all("test" in member.files for member in members):
            raise ValueError("every ensemble member needs forward predictions")
        test_predictions = [member["test"] for member in members]
        normalized_test = normalize_within_user(test_predictions, test_users)
        if args.prediction_ensemble_mode == "user_median_rank":
            test_scores = np.median(normalized_test, axis=0)
        elif args.prediction_ensemble_mode == "user_copeland_rank":
            test_scores = copeland_rank_consensus(normalized_test, test_users)
        else:
            test_scores = np.average(normalized_test, axis=0, weights=weights)
        if test_labels is None:
            raise RuntimeError("forward labels are unavailable")
        result["forward_valid"] = evaluate(test_users, test_labels, test_scores)
    if args.predictions_out:
        payload = {"valid": valid_scores.astype(np.float32)}
        if all("test" in member.files for member in members):
            normalized_test = normalize_within_user(
                [member["test"] for member in members],
                test_users,
            )
            if args.prediction_ensemble_mode == "user_median_rank":
                payload["test"] = np.median(normalized_test, axis=0).astype(np.float32)
            elif args.prediction_ensemble_mode == "user_copeland_rank":
                payload["test"] = copeland_rank_consensus(
                    normalized_test,
                    test_users,
                ).astype(np.float32)
            else:
                payload["test"] = np.average(
                    normalized_test,
                    axis=0,
                    weights=weights,
                ).astype(np.float32)
        Path(args.predictions_out).parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(args.predictions_out, **payload)
    return result


def train_fm_ensemble(args):
    t0 = time.time()
    splits = organizer_load(args.data_dir)
    enc, dim = organizer_encode(splits)
    Xtr, ytr, _ = enc["train"]
    Xva, yva, uva = enc["valid"]
    Xte, yte, ute = enc["test"]
    validation_predictions = []
    test_predictions = []
    members = []
    for seed in range(args.fm_ensemble_seeds):
        model = OrganizerFM(dim, k=args.fm_k, lr=args.fm_lr, l2=args.fm_l2, seed=seed)
        rng = np.random.default_rng(seed)
        best, state, bad = -1.0, None, 0
        for epoch in range(1, args.fm_epochs + 1):
            order = rng.permutation(len(ytr))
            for start in range(0, len(order), args.fm_batch_size):
                ix = order[start : start + args.fm_batch_size]
                model.step(Xtr[ix], ytr[ix])
            prediction = model.predict(Xva)
            metric = evaluate(uva, yva, prediction)
            if metric["primary"] > best + 1e-5:
                best, bad = metric["primary"], 0
                state = (model.V.copy(), model.W.copy(), np.float32(model.b))
            else:
                bad += 1
                if bad >= args.fm_patience:
                    break
        model.V, model.W, model.b = state
        prediction = model.predict(Xva)
        validation_predictions.append(prediction)
        members.append({"seed": seed, "valid": evaluate(uva, yva, prediction)})
        if args.evaluate_test:
            test_predictions.append(model.predict(Xte))
        running = np.mean(validation_predictions, axis=0)
        print(f"member {seed} running ensemble {evaluate(uva, yva, running)}", flush=True)
    ensemble_validation = np.mean(validation_predictions, axis=0)
    result = {
        "variant": args.variant,
        "valid": evaluate(uva, yva, ensemble_validation),
        "members": members,
        "parameters": {
            "fm_ensemble_seeds": args.fm_ensemble_seeds,
            "fm_k": args.fm_k,
            "fm_lr": args.fm_lr,
            "fm_l2": args.fm_l2,
        },
        "elapsed_seconds": time.time() - t0,
    }
    if args.evaluate_test:
        result["test"] = evaluate(ute, yte, np.mean(test_predictions, axis=0))
    return result


def within_user_percentile_rank(users, scores):
    """Convert aligned scores to stable percentile ranks within each user."""
    grouped = collections.defaultdict(list)
    for index, user in enumerate(users):
        grouped[user].append(index)
    ranks = np.empty(len(scores), dtype=np.float64)
    values = np.asarray(scores, dtype=np.float64)
    if values.ndim != 1 or not np.isfinite(values).all():
        raise ValueError("parent scores must be finite and one-dimensional")
    for indices in grouped.values():
        order = np.argsort(values[indices], kind="stable")
        local = np.empty(len(indices), dtype=np.float64)
        local[order] = np.arange(len(indices), dtype=np.float64)
        ranks[indices] = local / max(len(indices) - 1, 1)
    return ranks


def copeland_rank_consensus(normalized_predictions, users):
    """Aggregate aligned within-user member ranks by majority pairwise wins."""
    predictions = np.asarray(normalized_predictions, dtype=np.float64)
    if predictions.ndim != 2 or predictions.shape[0] < 2:
        raise ValueError("Copeland consensus requires at least two aligned members")
    users = np.asarray(users)
    if predictions.shape[1] != len(users):
        raise ValueError("Copeland predictions and users are not aligned")
    grouped = collections.defaultdict(list)
    for index, user in enumerate(users):
        grouped[user].append(index)
    scores = np.zeros(len(users), dtype=np.float64)
    for indices in grouped.values():
        if len(indices) == 1:
            scores[indices[0]] = 0.0
            continue
        values = predictions[:, indices]
        wins_by_member = values[:, :, None] > values[:, None, :]
        losses_by_member = values[:, :, None] < values[:, None, :]
        wins = wins_by_member.sum(axis=0)
        losses = losses_by_member.sum(axis=0)
        majority_wins = (wins > losses).sum(axis=1).astype(np.float64)
        tied_votes = (wins == losses).sum(axis=1).astype(np.float64) - 1.0
        copeland = majority_wins + 0.5 * tied_votes
        borda_tie_break = values.mean(axis=0) * 1e-6
        scores[np.asarray(indices)] = copeland + borda_tie_break
    return scores


def bounded_user_groups(ordered_users, maximum=10_000):
    """Return LightGBM-compatible group sizes without mixing users."""
    ordered_users = np.asarray(ordered_users)
    if ordered_users.ndim != 1 or maximum <= 0:
        raise ValueError("invalid grouped-user input")
    if len(ordered_users) == 0:
        return np.empty(0, dtype=np.int32)
    boundaries = np.flatnonzero(ordered_users[1:] != ordered_users[:-1]) + 1
    counts = np.diff(np.concatenate(([0], boundaries, [len(ordered_users)])))
    groups = []
    for count in counts:
        groups.extend([maximum] * (int(count) // maximum))
        if int(count) % maximum:
            groups.append(int(count) % maximum)
    result = np.asarray(groups, dtype=np.int32)
    if int(result.sum()) != len(ordered_users):
        raise ValueError("query groups do not conserve rows")
    return result


def load_prediction_archive(path, valid_rows, test_rows):
    """Load one aligned finite valid/test prediction archive."""
    with np.load(path) as archive:
        if not {"valid", "test"}.issubset(archive.files):
            raise ValueError(f"prediction archive lacks valid/test arrays: {path}")
        valid = np.asarray(archive["valid"], dtype=np.float64)
        test = np.asarray(archive["test"], dtype=np.float64)
    if valid.ndim != 1 or len(valid) != valid_rows:
        raise ValueError(f"validation prediction length mismatch: {len(valid)} != {valid_rows}")
    if test.ndim != 1 or len(test) != test_rows:
        raise ValueError(f"test prediction length mismatch: {len(test)} != {test_rows}")
    if not np.isfinite(valid).all() or not np.isfinite(test).all():
        raise ValueError("prediction archive contains non-finite values")
    return valid, test


def advance_aggregate_builder(builder, rows):
    """Advance an aggregate builder chronologically using labeled training rows."""
    builder._prepare(rows)
    for index in sorted(range(len(rows)), key=lambda i: (rows[i]["time_ms"], i)):
        builder._update(rows[index])


def grouped_residual_inputs(rows, features, parent_scores):
    """Group one feature matrix and aligned labels/init scores by user."""
    users = np.asarray([row["user"] for row in rows])
    parent_rank = np.asarray(parent_scores, dtype=np.float64)
    if parent_rank.ndim != 1 or len(parent_rank) != len(rows):
        raise ValueError("parent rank does not align with residual rows")
    if not np.isfinite(parent_rank).all():
        raise ValueError("parent rank must be finite")
    matrix = np.column_stack([features, parent_rank.astype(np.float32)]).astype(np.float32)
    order = np.argsort(users, kind="stable")
    ordered_users = users[order]
    labels = np.asarray([rows[index]["label"] for index in order], dtype=np.int32)
    groups = bounded_user_groups(ordered_users)
    return matrix[order], labels, groups, order, parent_rank


def restore_grouped_scores(order, grouped_scores):
    """Restore scores from stable user-group order to source-row order."""
    order = np.asarray(order, dtype=np.int64)
    grouped_scores = np.asarray(grouped_scores, dtype=np.float64)
    if len(order) != len(grouped_scores):
        raise ValueError("grouped score alignment mismatch")
    scores = np.empty(len(order), dtype=np.float64)
    scores[order] = grouped_scores
    return scores


def train_crossfit_lambdamart_residual(args):
    """Fit a chronological residual tree to frozen out-of-time parent ranks."""
    if args.split_mode not in ("shadow_late", "official"):
        raise ValueError("crossfit residual target must be shadow_late or official")
    if not args.meta_parent_predictions or not args.target_parent_predictions:
        raise ValueError("crossfit residual requires both parent prediction archives")
    if not args.model_out or not args.predictions_out:
        raise ValueError("crossfit residual requires model and prediction outputs")

    started = time.time()
    data_dir = Path(args.data_dir)
    meta = load_rows(data_dir, split_bounds=SHADOW_SPLITS["shadow_early"])
    target = load_rows(data_dir, split_bounds=split_bounds_for_mode(args.split_mode))
    meta_parent_train, meta_parent_valid = load_prediction_archive(
        args.meta_parent_predictions,
        len(meta["valid"]),
        len(meta["test"]),
    )
    target_parent_valid, target_parent_test = load_prediction_archive(
        args.target_parent_predictions,
        len(target["valid"]),
        len(target["test"]),
    )

    meta_builder = CausalAggregateBuilder(meta["train"])
    meta_builder.fit_transform(meta["train"])
    meta_train_features, feature_names, categorical = meta_builder.transform(meta["valid"])
    meta_valid_features, valid_names, valid_categorical = meta_builder.transform(meta["test"])
    if feature_names != valid_names or categorical != valid_categorical:
        raise RuntimeError("meta feature schema drift")

    base_target_rows = [
        row for row in target["train"] if row["date"] <= SHADOW_SPLITS["shadow_early"]["train"][1]
    ]
    extra_target_rows = [
        row for row in target["train"] if row["date"] > SHADOW_SPLITS["shadow_early"]["train"][1]
    ]
    target_builder = CausalAggregateBuilder(base_target_rows)
    target_builder.fit_transform(base_target_rows)
    advance_aggregate_builder(target_builder, extra_target_rows)
    target_valid_features, target_names, target_categorical = target_builder.transform(
        target["valid"]
    )
    target_test_features, test_names, test_categorical = target_builder.transform(
        target["test"]
    )
    if not (
        feature_names == target_names == test_names
        and categorical == target_categorical == test_categorical
    ):
        raise RuntimeError("target feature schema drift")

    (
        meta_train_matrix,
        meta_train_labels,
        meta_train_groups,
        meta_train_order,
        meta_train_rank,
    ) = grouped_residual_inputs(meta["valid"], meta_train_features, meta_parent_train)
    (
        meta_valid_matrix,
        meta_valid_labels,
        meta_valid_groups,
        meta_valid_order,
        meta_valid_rank,
    ) = grouped_residual_inputs(meta["test"], meta_valid_features, meta_parent_valid)
    all_feature_names = feature_names + ["parent_within_user_rank"]
    train_set = lgb.Dataset(
        meta_train_matrix,
        label=meta_train_labels,
        group=meta_train_groups,
        init_score=meta_train_rank[meta_train_order],
        feature_name=all_feature_names,
        categorical_feature=categorical,
        free_raw_data=True,
    )
    valid_set = lgb.Dataset(
        meta_valid_matrix,
        label=meta_valid_labels,
        group=meta_valid_groups,
        init_score=meta_valid_rank[meta_valid_order],
        feature_name=all_feature_names,
        categorical_feature=categorical,
        reference=train_set,
        free_raw_data=True,
    )
    parameters = {
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
        "verbosity": -1,
        "num_threads": 16,
        "seed": 2027,
        "data_random_seed": 2027,
        "feature_fraction_seed": 2027,
        "bagging_seed": 2027,
        "deterministic": True,
        "force_col_wise": True,
    }
    booster = lgb.train(
        parameters,
        train_set,
        num_boost_round=200,
        valid_sets=[valid_set],
        valid_names=["meta_valid"],
        callbacks=[lgb.early_stopping(20), lgb.log_evaluation(10)],
    )
    best_iteration = int(booster.best_iteration or 200)
    meta_delta_grouped = booster.predict(
        meta_valid_matrix,
        num_iteration=best_iteration,
        raw_score=True,
    )
    meta_delta = restore_grouped_scores(meta_valid_order, meta_delta_grouped)
    meta_scores = meta_valid_rank + meta_delta
    meta_users = [row["user"] for row in meta["test"]]
    meta_labels = [row["label"] for row in meta["test"]]

    target_valid_users = [row["user"] for row in target["valid"]]
    target_valid_rank = target_parent_valid
    target_valid_matrix = np.column_stack(
        [target_valid_features, target_valid_rank.astype(np.float32)]
    ).astype(np.float32)
    target_valid_scores = target_valid_rank + booster.predict(
        target_valid_matrix,
        num_iteration=best_iteration,
        raw_score=True,
    )
    target_test_users = [row["user"] for row in target["test"]]
    target_test_rank = target_parent_test
    target_test_matrix = np.column_stack(
        [target_test_features, target_test_rank.astype(np.float32)]
    ).astype(np.float32)
    target_test_scores = target_test_rank + booster.predict(
        target_test_matrix,
        num_iteration=best_iteration,
        raw_score=True,
    )

    result = {
        "variant": args.variant,
        "best_iteration": best_iteration,
        "features": all_feature_names,
        "meta_parent_valid": evaluate(meta_users, meta_labels, meta_valid_rank),
        "meta_corrected_valid": evaluate(meta_users, meta_labels, meta_scores),
        "parent_valid": evaluate(
            target_valid_users,
            [row["label"] for row in target["valid"]],
            target_valid_rank,
        ),
        "valid": evaluate(
            target_valid_users,
            [row["label"] for row in target["valid"]],
            target_valid_scores,
        ),
        "robustness": robustness_slices(
            target["train"],
            target["valid"],
            target_valid_scores,
        ),
        "parameters": {
            "meta_split_mode": "shadow_early",
            "target_split_mode": args.split_mode,
            "meta_parent_predictions": args.meta_parent_predictions,
            "target_parent_predictions": args.target_parent_predictions,
            "tree": parameters,
        },
        "label_boundary": label_boundary_attestation(args.split_mode == "official"),
        "elapsed_seconds": time.time() - started,
    }
    if args.split_mode != "official":
        target_test_labels = [row["label"] for row in target["test"]]
        result["parent_forward_valid"] = evaluate(
            target_test_users,
            target_test_labels,
            target_test_rank,
        )
        result["forward_valid"] = evaluate(
            target_test_users,
            target_test_labels,
            target_test_scores,
        )
    Path(args.model_out).parent.mkdir(parents=True, exist_ok=True)
    booster.save_model(args.model_out, num_iteration=best_iteration)
    Path(args.predictions_out).parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        args.predictions_out,
        valid=np.asarray(target_valid_scores, dtype=np.float32),
        test=np.asarray(target_test_scores, dtype=np.float32),
    )
    return result


def train_and_score(args):
    if args.variant == "crossfit_lambdamart_residual":
        return train_crossfit_lambdamart_residual(args)
    if args.variant == "aggregate_binary":
        return train_aggregate_binary(args)
    if args.variant in ("bpr_fm", "fm_then_bpr"):
        return train_pairwise_fm(args)
    if args.variant == "softlabel_fm":
        return train_softlabel_fm(args)
    if args.variant == "extended_fm":
        return train_extended_fm(args)
    if args.variant == "svd_cf":
        return train_svd_cf(args)
    if args.variant == "sequence_nn":
        return train_sequence_nn(args)
    if args.variant == "fm_ensemble":
        return train_fm_ensemble(args)
    if args.variant == "prediction_ensemble":
        return evaluate_prediction_ensemble(args)
    t0 = time.time()
    splits = load_rows(Path(args.data_dir))
    builder = FeatureBuilder(
        splits["train"],
        include_history=args.variant in ("history_lambdarank", "history_diagnostic"),
    )
    if args.variant == "history_diagnostic":
        builder.include_history = True
        Xva, names, _ = builder.transform(splits["valid"], training=False)
        users = [r["user"] for r in splits["valid"]]
        labels = [r["label"] for r in splits["valid"]]
        diagnostic = {}
        for i, name in enumerate(names):
            if name.endswith("_rate"):
                diagnostic[name] = evaluate(users, labels, Xva[:, i])
        best_name = max(diagnostic, key=lambda name: diagnostic[name]["primary"])
        return {
            "variant": args.variant,
            "valid": diagnostic[best_name],
            "best_signal": best_name,
            "diagnostic": diagnostic,
            "elapsed_seconds": time.time() - t0,
        }
    Xtr, names, categorical = builder.transform(splits["train"], training=True)
    Xva, _, _ = builder.transform(splits["valid"], training=False)
    Xtr_s, ytr_s, gtr, _ = group_sort(splits["train"], Xtr)
    Xva_s, yva_s, gva, va_order = group_sort(splits["valid"], Xva)

    train_set = lgb.Dataset(
        Xtr_s,
        label=ytr_s,
        group=gtr,
        feature_name=names,
        categorical_feature=categorical,
        free_raw_data=False,
    )
    valid_set = lgb.Dataset(
        Xva_s,
        label=yva_s,
        group=gva,
        feature_name=names,
        categorical_feature=categorical,
        reference=train_set,
        free_raw_data=False,
    )
    params = {
        "objective": "lambdarank",
        "metric": "ndcg",
        "ndcg_eval_at": [5],
        "learning_rate": args.learning_rate,
        "num_leaves": args.num_leaves,
        "min_data_in_leaf": args.min_data_in_leaf,
        "feature_fraction": args.feature_fraction,
        "bagging_fraction": args.bagging_fraction,
        "bagging_freq": 1 if args.bagging_fraction < 1 else 0,
        "lambda_l2": args.lambda_l2,
        "verbosity": -1,
        "seed": args.seed,
        "num_threads": args.threads,
        "deterministic": True,
        "force_col_wise": True,
    }
    model = lgb.train(
        params,
        train_set,
        num_boost_round=args.num_boost_round,
        valid_sets=[valid_set],
        callbacks=[lgb.early_stopping(args.early_stopping_rounds), lgb.log_evaluation(20)],
    )
    pred_sorted = model.predict(Xva_s, num_iteration=model.best_iteration)
    pred = np.empty(len(pred_sorted), dtype=np.float64)
    pred[va_order] = pred_sorted
    valid = evaluate(
        [r["user"] for r in splits["valid"]],
        [r["label"] for r in splits["valid"]],
        pred,
    )
    result = {
        "variant": args.variant,
        "valid": valid,
        "best_iteration": model.best_iteration,
        "features": names,
        "parameters": params,
        "elapsed_seconds": time.time() - t0,
    }
    if args.evaluate_test:
        Xte, _, _ = builder.transform(splits["test"], training=False)
        pred_te = model.predict(Xte, num_iteration=model.best_iteration)
        result["test"] = evaluate(
            [r["user"] for r in splits["test"]],
            [r["label"] for r in splits["test"]],
            pred_te,
        )
    if args.model_out:
        Path(args.model_out).parent.mkdir(parents=True, exist_ok=True)
        model.save_model(args.model_out, num_iteration=model.best_iteration)
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", required=True)
    ap.add_argument(
        "--variant",
        choices=("raw_lambdarank", "history_lambdarank", "history_diagnostic", "aggregate_binary", "bpr_fm", "fm_then_bpr", "softlabel_fm", "extended_fm", "svd_cf", "sequence_nn", "fm_ensemble", "prediction_ensemble", "crossfit_lambdamart_residual"),
        default="raw_lambdarank",
    )
    ap.add_argument("--learning-rate", type=float, default=0.05)
    ap.add_argument("--num-leaves", type=int, default=63)
    ap.add_argument("--min-data-in-leaf", type=int, default=100)
    ap.add_argument("--feature-fraction", type=float, default=0.9)
    ap.add_argument("--bagging-fraction", type=float, default=0.9)
    ap.add_argument("--lambda-l2", type=float, default=1.0)
    ap.add_argument("--num-boost-round", type=int, default=600)
    ap.add_argument("--early-stopping-rounds", type=int, default=50)
    ap.add_argument("--threads", type=int, default=8)
    ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--fm-k", type=int, default=16)
    ap.add_argument("--fm-lr", type=float, default=0.001)
    ap.add_argument("--fm-l2", type=float, default=1e-6)
    ap.add_argument("--fm-epochs", type=int, default=40)
    ap.add_argument("--fm-batch-size", type=int, default=8192)
    ap.add_argument("--fm-patience", type=int, default=4)
    ap.add_argument("--bpr-epochs", type=int, default=12)
    ap.add_argument("--bpr-batch-size", type=int, default=4096)
    ap.add_argument("--bpr-patience", type=int, default=4)
    ap.add_argument("--bpr-lr", type=float, default=0.001)
    ap.add_argument("--bpr-sampling", choices=("random", "hard"), default="random")
    ap.add_argument("--hard-negative-pool", type=int, default=3)
    ap.add_argument("--aux-target", choices=("click", "watch_ratio", "engagement"), default="watch_ratio")
    ap.add_argument("--aux-weight", type=float, default=0.5)
    ap.add_argument("--feature-set", choices=("base", "tags", "extended"), default="tags")
    ap.add_argument("--svd-components", type=int, default=64)
    ap.add_argument("--svd-iterations", type=int, default=7)
    ap.add_argument("--svd-weighting", choices=("positive", "centered"), default="centered")
    ap.add_argument("--history-length", type=int, default=20)
    ap.add_argument("--dual-timescale-history", action="store_true")
    ap.add_argument("--hard-history-expert", action="store_true")
    ap.add_argument(
        "--history-order",
        choices=("causal", "source"),
        default="causal",
        help="training-history traversal; source is a diagnostic legacy comparator",
    )
    ap.add_argument(
        "--split-mode",
        choices=("official", "shadow", "shadow_early", "shadow_middle", "shadow_late"),
        default="official",
    )
    ap.add_argument(
        "--history-event",
        choices=("long_view", "click", "like", "behavior", "all"),
        default="long_view",
    )
    ap.add_argument(
        "--negative-history-event",
        choices=("none", "strict_skip_005"),
        default="none",
        help=(
            "optional separate causal history of training-only non-long-view, "
            "non-click impressions watched for at most five percent"
        ),
    )
    ap.add_argument(
        "--secondary-history-event",
        choices=("none", "click", "engagement"),
        default="none",
        help=(
            "optional distinct causal profile for earlier clicks or explicit "
            "positive engagements; mutually exclusive with negative history"
        ),
    )
    ap.add_argument("--history-behavior-signals", action="store_true")
    ap.add_argument("--history-tags", action="store_true")
    ap.add_argument("--history-primary-tag", action="store_true")
    ap.add_argument("--history-categories", action="store_true")
    ap.add_argument(
        "--category-file",
        default=str(
            ROOT
            / "data"
            / "kuairand-supplemental"
            / "kuairand_video_categories_pure.csv"
        ),
    )
    ap.add_argument("--caption-content", action="store_true")
    ap.add_argument(
        "--caption-file",
        default=str(
            ROOT
            / "data"
            / "kuairand-supplemental"
            / "kuairand_video_captions_pure.csv"
        ),
    )
    ap.add_argument("--history-authors", action="store_true")
    ap.add_argument("--attention-mode", choices=("dot", "din"), default="dot")
    ap.add_argument("--recency-half-life-events", type=float, default=0.0)
    ap.add_argument(
        "--auxiliary-task",
        choices=("none", "watch_ratio", "click", "cwm"),
        default="none",
    )
    ap.add_argument(
        "--auxiliary-architecture",
        choices=("shared", "task_protected"),
        default="shared",
    )
    ap.add_argument("--auxiliary-weight", type=float, default=0.2)
    ap.add_argument("--cwm-c-inverse", type=float, default=40.0)
    ap.add_argument("--cwm-sigma", type=float, default=2.0)
    ap.add_argument("--history-match-features", action="store_true")
    ap.add_argument(
        "--sequence-encoder",
        choices=("none", "gru", "transformer"),
        default="none",
    )
    ap.add_argument("--user-profile-features", action="store_true")
    ap.add_argument("--user-balance-alpha", type=float, default=0.0)
    ap.add_argument("--date-decay-half-life-days", type=float, default=0.0)
    ap.add_argument("--target-rate-features", action="store_true")
    ap.add_argument("--causal-aggregate-features", action="store_true")
    ap.add_argument("--causal-repeat-features", action="store_true")
    ap.add_argument("--multi-behavior-context", action="store_true")
    ap.add_argument("--time-features", action="store_true")
    ap.add_argument("--cross-layers", type=int, default=0)
    ap.add_argument("--embedding-dim", type=int, default=32)
    ap.add_argument("--hidden-dim", type=int, default=256)
    ap.add_argument("--dropout", type=float, default=0.1)
    ap.add_argument("--id-embedding-dropout", type=float, default=0.0)
    ap.add_argument("--nn-lr", type=float, default=0.001)
    ap.add_argument("--nn-weight-decay", type=float, default=1e-5)
    ap.add_argument("--nn-epochs", type=int, default=8)
    ap.add_argument("--nn-batch-size", type=int, default=4096)
    ap.add_argument("--nn-patience", type=int, default=3)
    ap.add_argument("--device", choices=("auto", "cpu", "mps"), default="auto")
    ap.add_argument("--ensemble-alpha", type=float, default=0.0)
    ap.add_argument("--fm-ensemble-seeds", type=int, default=3)
    ap.add_argument("--nn-fm-term", action="store_true")
    ap.add_argument("--nn-bpr-epochs", type=int, default=0)
    ap.add_argument("--nn-bpr-lr", type=float, default=0.0001)
    ap.add_argument("--nn-bpr-batch-size", type=int, default=2048)
    ap.add_argument("--nn-bpr-patience", type=int, default=2)
    ap.add_argument("--nn-bpr-sampling", choices=("random", "hard"), default="random")
    ap.add_argument("--nn-bpr-hard-fraction", type=float, default=0.2)
    ap.add_argument("--nn-listwise-epochs", type=int, default=0)
    ap.add_argument("--nn-listwise-lr", type=float, default=0.00005)
    ap.add_argument("--nn-listwise-batch-users", type=int, default=64)
    ap.add_argument("--nn-listwise-patience", type=int, default=2)
    ap.add_argument("--nn-listwise-max-positives", type=int, default=0)
    ap.add_argument("--nn-listwise-max-negatives", type=int, default=0)
    ap.add_argument("--nn-lambda-epochs", type=int, default=0)
    ap.add_argument("--nn-lambda-lr", type=float, default=0.00002)
    ap.add_argument("--nn-lambda-batch-users", type=int, default=64)
    ap.add_argument("--nn-lambda-patience", type=int, default=1)
    ap.add_argument("--nn-lambda-max-positives", type=int, default=5)
    ap.add_argument("--nn-lambda-max-negatives", type=int, default=20)
    ap.add_argument("--evaluate-test", action="store_true", help=argparse.SUPPRESS)
    ap.add_argument("--evaluate-forward", action="store_true")
    ap.add_argument("--evaluate-random", action="store_true")
    ap.add_argument("--predict-test", action="store_true")
    ap.add_argument("--model-out")
    ap.add_argument("--predictions-out")
    ap.add_argument("--prediction-files", nargs="+", default=[])
    ap.add_argument("--prediction-weights", nargs="+", type=float, default=[])
    ap.add_argument("--meta-parent-predictions")
    ap.add_argument("--target-parent-predictions")
    ap.add_argument(
        "--prediction-ensemble-mode",
        choices=("mean", "user_zscore", "user_rank", "user_median_rank", "user_copeland_rank"),
        default="mean",
    )
    ap.add_argument("--json-out")
    args = ap.parse_args()
    if args.evaluate_test:
        ap.error("official test-label evaluation is forbidden by the organizer clarification")
    legacy_outcome_loading_variants = {
        "bpr_fm",
        "fm_then_bpr",
        "softlabel_fm",
        "fm_ensemble",
    }
    if args.split_mode == "official" and args.variant in legacy_outcome_loading_variants:
        ap.error(
            f"{args.variant} is quarantined in official mode because its legacy "
            "organizer loader materializes final-test outcomes"
        )
    if args.split_mode == "official" and args.variant == "sequence_nn" and args.ensemble_alpha > 0:
        ap.error(
            "--ensemble-alpha is quarantined in official mode because its legacy "
            "organizer-FM path materializes final-test outcomes"
        )
    result = train_and_score(args)
    def json_default(value):
        if isinstance(value, np.generic):
            return value.item()
        raise TypeError(f"cannot encode {type(value).__name__}")

    encoded = json.dumps(result, indent=2, sort_keys=True, default=json_default)
    print("RESULT_JSON=" + json.dumps(result, sort_keys=True, default=json_default))
    if args.json_out:
        path = Path(args.json_out)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(encoded + "\n")


if __name__ == "__main__":
    main()
