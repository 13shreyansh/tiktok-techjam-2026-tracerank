#!/usr/bin/env python3
"""Precompute strictly causal KuaiRand history fields for each dev split.

Training-row fields use only earlier timestamps for the same user. Rows sharing
one user/timestamp are treated as a simultaneous impression batch: every field
is emitted before any outcome in that batch updates state. Validation and
forward rows use state frozen at the training cutoff and never update from
validation outcomes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import resource
import time
from pathlib import Path

import numpy as np


SPLITS = {
    "stack_early": (20220408, 20220409),
    "official": (20220408, 20220421),
    "shadow_early": (20220408, 20220411),
    "shadow_middle": (20220408, 20220414),
    "shadow_late": (20220408, 20220417),
}
FEATURE_NAMES = (
    "prior_user_count_log2",
    "prior_user_long_view_rate_21",
    "prior_user_strong_feedback_count_log2",
    "prior_user_hate_count_log2",
    "prior_user_tag_count_log2",
    "prior_user_tag_long_view_rate_21",
    "current_tag_matches_last_positive_tag",
    "last_positive_tag",
)
REQUIRED_ARRAYS = (
    "user", "tag", "date", "time_ms", "label", "is_like", "is_follow",
    "is_comment", "is_forward", "is_hate",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def log_bucket(value: int, cap: int) -> int:
    return min(int(math.log2(value + 1)), cap)


def rate_bucket(positive: np.ndarray | int, count: np.ndarray | int) -> np.ndarray:
    # Fixed Beta(1, 3) prior; 21 equally spaced categorical values.
    rate = (np.asarray(positive, dtype=np.float64) + 1.0) / (
        np.asarray(count, dtype=np.float64) + 4.0
    )
    return np.minimum((rate * 21.0).astype(np.int16), 20)


def load(cache_dir: Path, name: str, mmap_mode: str = "r") -> np.ndarray:
    return np.load(cache_dir / f"{name}.npy", mmap_mode=mmap_mode)


def build_split(cache_dir: Path, split: str, train_bounds: tuple[int, int]) -> dict:
    users = load(cache_dir, "user")
    tags = load(cache_dir, "tag")
    dates = load(cache_dir, "date")
    times = load(cache_dir, "time_ms")
    labels = load(cache_dir, "label")
    likes = load(cache_dir, "is_like")
    follows = load(cache_dir, "is_follow")
    comments = load(cache_dir, "is_comment")
    forwards = load(cache_dir, "is_forward")
    hates = load(cache_dir, "is_hate")
    manifest = json.loads((cache_dir / "manifest.json").read_text())
    row_count = int(manifest["rows"])
    user_count = int(manifest["user_count"])
    tag_count = int(manifest["tag_count"])
    lo, hi = train_bounds
    train_indices = np.flatnonzero((dates >= lo) & (dates <= hi)).astype(np.int64)
    train_users = np.asarray(users[train_indices], dtype=np.int32)
    train_times = np.asarray(times[train_indices], dtype=np.int64)
    source_order = np.argsort(train_users, kind="stable")
    source_users = train_users[source_order]
    source_starts = np.r_[0, np.flatnonzero(source_users[1:] != source_users[:-1]) + 1]
    source_ends = np.r_[source_starts[1:], len(source_order)]
    source_timestamp_inversions = sum(
        int(np.sum(train_times[source_order[start:end]][1:] < train_times[source_order[start:end]][:-1]))
        for start, end in zip(source_starts, source_ends)
    )
    # The official files and deterministic samples need not be ordered within
    # user. Sort causally, preserving source row order inside equal timestamps.
    order = np.lexsort((train_indices, train_times, train_users))
    ordered = train_indices[order]
    ordered_users = train_users[order]
    user_starts = np.r_[0, np.flatnonzero(ordered_users[1:] != ordered_users[:-1]) + 1]
    user_ends = np.r_[user_starts[1:], len(ordered)]

    output_path = cache_dir / f"history_{split}.npy"
    output = np.lib.format.open_memmap(
        output_path, mode="w+", dtype="int16", shape=(row_count, len(FEATURE_NAMES))
    )
    output[:] = 0
    final_count = np.zeros(user_count, dtype=np.int64)
    final_positive = np.zeros(user_count, dtype=np.int64)
    final_strong = np.zeros(user_count, dtype=np.int64)
    final_hate = np.zeros(user_count, dtype=np.int64)
    final_tag_count = np.zeros((user_count, tag_count), dtype=np.int64)
    final_tag_positive = np.zeros((user_count, tag_count), dtype=np.int64)
    final_last_positive_tag = np.full(user_count, -1, dtype=np.int16)
    timestamp_inversions = 0
    simultaneous_batches = 0

    for user_start, user_end in zip(user_starts, user_ends):
        user_indices = ordered[user_start:user_end]
        user = int(users[user_indices[0]])
        user_times = np.asarray(times[user_indices], dtype=np.int64)
        timestamp_inversions += int(np.sum(user_times[1:] < user_times[:-1]))
        if timestamp_inversions:
            raise ValueError("training interactions are not ordered by user timestamp")
        count = positive = strong = hate = 0
        tag_seen = np.zeros(tag_count, dtype=np.int64)
        tag_positive = np.zeros(tag_count, dtype=np.int64)
        last_positive_tag = -1
        position = 0
        while position < len(user_indices):
            batch_end = position + 1
            while (
                batch_end < len(user_indices)
                and user_times[batch_end] == user_times[position]
            ):
                batch_end += 1
            batch = user_indices[position:batch_end]
            batch_tags = np.asarray(tags[batch], dtype=np.int64)
            valid_tag = batch_tags >= 0
            output[batch, 0] = log_bucket(count, 15)
            output[batch, 1] = int(rate_bucket(positive, count))
            output[batch, 2] = log_bucket(strong, 10)
            output[batch, 3] = log_bucket(hate, 10)
            output[batch, 4] = 0
            output[batch, 5] = int(rate_bucket(0, 0))
            output[batch, 6] = 0
            output[batch, 7] = last_positive_tag
            if np.any(valid_tag):
                selected = batch[valid_tag]
                selected_tags = batch_tags[valid_tag]
                output[selected, 4] = np.minimum(
                    np.floor(np.log2(tag_seen[selected_tags] + 1)), 15
                ).astype(np.int16)
                output[selected, 5] = rate_bucket(
                    tag_positive[selected_tags], tag_seen[selected_tags]
                )
                output[selected, 6] = (selected_tags == last_positive_tag).astype(np.int16)

            batch_labels = np.asarray(labels[batch], dtype=np.int64)
            batch_strong = (
                np.asarray(likes[batch], dtype=np.uint8)
                | np.asarray(follows[batch], dtype=np.uint8)
                | np.asarray(comments[batch], dtype=np.uint8)
                | np.asarray(forwards[batch], dtype=np.uint8)
            )
            count += len(batch)
            positive += int(batch_labels.sum())
            strong += int(batch_strong.sum())
            hate += int(np.asarray(hates[batch], dtype=np.uint8).sum())
            if np.any(valid_tag):
                tag_seen += np.bincount(batch_tags[valid_tag], minlength=tag_count)
                positive_tags = batch_tags[valid_tag & (batch_labels == 1)]
                if len(positive_tags):
                    tag_positive += np.bincount(positive_tags, minlength=tag_count)
                    last_positive_tag = int(positive_tags[-1])
            simultaneous_batches += int(len(batch) > 1)
            position = batch_end

        final_count[user] = count
        final_positive[user] = positive
        final_strong[user] = strong
        final_hate[user] = hate
        final_tag_count[user] = tag_seen
        final_tag_positive[user] = tag_positive
        final_last_positive_tag[user] = last_positive_tag

    score_indices = np.flatnonzero(dates > hi).astype(np.int64)
    score_users = np.asarray(users[score_indices], dtype=np.int64)
    score_tags = np.asarray(tags[score_indices], dtype=np.int64)
    valid_tag = score_tags >= 0
    output[score_indices, 0] = np.minimum(
        np.floor(np.log2(final_count[score_users] + 1)), 15
    ).astype(np.int16)
    output[score_indices, 1] = rate_bucket(
        final_positive[score_users], final_count[score_users]
    )
    output[score_indices, 2] = np.minimum(
        np.floor(np.log2(final_strong[score_users] + 1)), 10
    ).astype(np.int16)
    output[score_indices, 3] = np.minimum(
        np.floor(np.log2(final_hate[score_users] + 1)), 10
    ).astype(np.int16)
    output[score_indices, 4] = 0
    output[score_indices, 5] = int(rate_bucket(0, 0))
    output[score_indices, 6] = 0
    output[score_indices, 7] = final_last_positive_tag[score_users]
    if np.any(valid_tag):
        selected = score_indices[valid_tag]
        selected_users = score_users[valid_tag]
        selected_tags = score_tags[valid_tag]
        counts = final_tag_count[selected_users, selected_tags]
        positives = final_tag_positive[selected_users, selected_tags]
        output[selected, 4] = np.minimum(
            np.floor(np.log2(counts + 1)), 15
        ).astype(np.int16)
        output[selected, 5] = rate_bucket(positives, counts)
        output[selected, 6] = (
            selected_tags == final_last_positive_tag[selected_users]
        ).astype(np.int16)
    output.flush()
    return {
        "split": split,
        "train_bounds": list(train_bounds),
        "train_rows": int(len(train_indices)),
        "frozen_score_rows": int(len(score_indices)),
        "timestamp_inversions": timestamp_inversions,
        "source_timestamp_inversions": source_timestamp_inversions,
        "simultaneous_multirow_batches": simultaneous_batches,
        "path": output_path.name,
        "bytes": output_path.stat().st_size,
        "sha256": sha256(output_path),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache-dir", type=Path, required=True)
    parser.add_argument("--split", choices=tuple(SPLITS))
    args = parser.parse_args()
    started = time.time()
    base_manifest = args.cache_dir / "manifest.json"
    manifest = json.loads(base_manifest.read_text())
    missing = [name for name in REQUIRED_ARRAYS if not (args.cache_dir / f"{name}.npy").is_file()]
    if missing:
        raise ValueError(f"history cache is missing required arrays: {missing}")
    if manifest.get("retained_date_range") != [20220408, 20220428]:
        raise ValueError("history cache is not the locked April 8-28 development range")
    record_path = args.cache_dir / "history_manifest.json"
    previous = json.loads(record_path.read_text()) if record_path.is_file() else {}
    previous_splits = dict(previous.get("splits", {}))
    selected = (
        [(args.split, SPLITS[args.split])]
        if args.split is not None
        else list(SPLITS.items())
    )
    duplicate = [name for name, _ in selected if name in previous_splits]
    if duplicate:
        raise FileExistsError(f"history splits already exist: {duplicate}")
    results = [build_split(args.cache_dir, name, bounds) for name, bounds in selected]
    previous_splits.update({entry["split"]: entry for entry in results})
    record = {
        "format_version": 1,
        "feature_names": FEATURE_NAMES,
        "causal_contract": (
            "Training features use only prior user timestamps; same-timestamp rows update "
            "after the whole batch. Validation and forward features freeze at train cutoff."
        ),
        "feedback_used": ["long_view", "is_like", "is_follow", "is_comment", "is_forward", "is_hate"],
        "base_cache_manifest_sha256": sha256(base_manifest),
        "splits": previous_splits,
        "elapsed_seconds": time.time() - started,
        "max_rss_bytes": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
    }
    record_path.write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(record, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
