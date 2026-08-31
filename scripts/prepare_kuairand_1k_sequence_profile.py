#!/usr/bin/env python3
"""Build strictly causal recent-interest profiles for KuaiRand splits."""
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
    "official": (20220408, 20220421),
    "shadow_early": (20220408, 20220411),
    "shadow_middle": (20220408, 20220414),
    "shadow_late": (20220408, 20220417),
}
FEATURE_NAMES = (
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


def recency_bucket(
    current_ms: np.ndarray | int, previous_ms: np.ndarray | int
) -> np.ndarray:
    current = np.asarray(current_ms, dtype=np.int64)
    previous = np.asarray(previous_ms, dtype=np.int64)
    current, previous = np.broadcast_arrays(current, previous)
    output = np.full(current.shape, 16, dtype=np.int16)
    seen = previous >= 0
    hours = np.maximum(current[seen] - previous[seen], 0).astype(np.float64) / 3_600_000.0
    output[seen] = np.minimum(np.floor(np.log2(hours + 1.0)), 15).astype(np.int16)
    return output


def load(cache_dir: Path, name: str) -> np.ndarray:
    return np.load(cache_dir / f"{name}.npy", mmap_mode="r")


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
    # Sort within user by timestamp and source row so history is causal even
    # when source shards are concatenated in a non-chronological order.
    order = np.lexsort((train_indices, train_times, train_users))
    ordered = train_indices[order]
    ordered_users = train_users[order]
    user_starts = np.r_[0, np.flatnonzero(ordered_users[1:] != ordered_users[:-1]) + 1]
    user_ends = np.r_[user_starts[1:], len(ordered)]

    output_path = cache_dir / f"sequence_profile_{split}.npy"
    output = np.lib.format.open_memmap(
        output_path, mode="w+", dtype="int16", shape=(row_count, len(FEATURE_NAMES))
    )
    output[:] = 0
    output[:, :5] = -1
    output[:, 6] = -1
    output[:, 8] = -1
    output[:, 10] = 16
    final_recent = np.full((user_count, 5), -1, dtype=np.int16)
    final_strong = np.full(user_count, -1, dtype=np.int16)
    final_hate = np.full(user_count, -1, dtype=np.int16)
    final_positive_time = np.full(user_count, -1, dtype=np.int64)
    simultaneous_batches = 0
    timestamp_inversions = 0

    for user_start, user_end in zip(user_starts, user_ends):
        user_indices = ordered[user_start:user_end]
        user = int(users[user_indices[0]])
        user_times = np.asarray(times[user_indices], dtype=np.int64)
        inversions = int(np.sum(user_times[1:] < user_times[:-1]))
        timestamp_inversions += inversions
        if inversions:
            raise ValueError("training interactions are not ordered by user timestamp")
        recent = np.full(5, -1, dtype=np.int16)
        last_strong = -1
        last_hate = -1
        last_positive_time = -1
        position = 0
        while position < len(user_indices):
            batch_end = position + 1
            while batch_end < len(user_indices) and user_times[batch_end] == user_times[position]:
                batch_end += 1
            batch = user_indices[position:batch_end]
            batch_tags = np.asarray(tags[batch], dtype=np.int16)
            output[batch, :5] = recent
            output[batch, 6] = last_strong
            output[batch, 8] = last_hate
            output[batch, 10] = recency_bucket(user_times[position], last_positive_time)
            valid_tag = batch_tags >= 0
            if np.any(valid_tag):
                selected = batch[valid_tag]
                selected_tags = batch_tags[valid_tag]
                output[selected, 5] = np.sum(
                    selected_tags[:, None] == recent[None, :], axis=1
                ).astype(np.int16)
                output[selected, 7] = (selected_tags == last_strong).astype(np.int16)
                output[selected, 9] = (selected_tags == last_hate).astype(np.int16)

            batch_labels = np.asarray(labels[batch], dtype=np.uint8)
            batch_strong = (
                np.asarray(likes[batch], dtype=np.uint8)
                | np.asarray(follows[batch], dtype=np.uint8)
                | np.asarray(comments[batch], dtype=np.uint8)
                | np.asarray(forwards[batch], dtype=np.uint8)
            )
            positive_tags = batch_tags[valid_tag & (batch_labels == 1)]
            for positive_tag in positive_tags:
                recent[1:] = recent[:-1]
                recent[0] = positive_tag
                last_positive_time = int(user_times[position])
            strong_tags = batch_tags[valid_tag & (batch_strong == 1)]
            if len(strong_tags):
                last_strong = int(strong_tags[-1])
            hate_tags = batch_tags[valid_tag & (np.asarray(hates[batch], dtype=np.uint8) == 1)]
            if len(hate_tags):
                last_hate = int(hate_tags[-1])
            simultaneous_batches += int(len(batch) > 1)
            position = batch_end

        final_recent[user] = recent
        final_strong[user] = last_strong
        final_hate[user] = last_hate
        final_positive_time[user] = last_positive_time

    score_indices = np.flatnonzero(dates > hi).astype(np.int64)
    score_users = np.asarray(users[score_indices], dtype=np.int64)
    score_tags = np.asarray(tags[score_indices], dtype=np.int16)
    output[score_indices, :5] = final_recent[score_users]
    output[score_indices, 6] = final_strong[score_users]
    output[score_indices, 8] = final_hate[score_users]
    output[score_indices, 10] = recency_bucket(
        np.asarray(times[score_indices], dtype=np.int64),
        final_positive_time[score_users],
    )
    valid_tag = score_tags >= 0
    if np.any(valid_tag):
        selected = score_indices[valid_tag]
        selected_users = score_users[valid_tag]
        selected_tags = score_tags[valid_tag]
        output[selected, 5] = np.sum(
            selected_tags[:, None] == final_recent[selected_users], axis=1
        ).astype(np.int16)
        output[selected, 7] = (
            selected_tags == final_strong[selected_users]
        ).astype(np.int16)
        output[selected, 9] = (
            selected_tags == final_hate[selected_users]
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
        raise ValueError(f"sequence-profile cache is missing required arrays: {missing}")
    if manifest.get("retained_date_range") != [20220408, 20220428]:
        raise ValueError("sequence-profile cache is not the locked April 8-28 development range")
    record_path = args.cache_dir / "sequence_profile_manifest.json"
    previous = json.loads(record_path.read_text()) if record_path.is_file() else {}
    selected = (
        [(args.split, SPLITS[args.split])]
        if args.split is not None
        else list(SPLITS.items())
    )
    previous_splits = dict(previous.get("splits", {}))
    duplicate = [name for name, _ in selected if name in previous_splits]
    if duplicate:
        raise FileExistsError(f"sequence profiles already exist for: {duplicate}")
    results = [build_split(args.cache_dir, name, bounds) for name, bounds in selected]
    previous_splits.update({entry["split"]: entry for entry in results})
    record = {
        "format_version": 1,
        "feature_names": FEATURE_NAMES,
        "causal_contract": (
            "Training profiles use only earlier user timestamps; same-timestamp rows "
            "update after the full batch. Validation and forward profiles freeze at "
            "the training cutoff."
        ),
        "feedback_used": [
            "long_view", "is_like", "is_follow", "is_comment", "is_forward", "is_hate"
        ],
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
