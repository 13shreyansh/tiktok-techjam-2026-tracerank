#!/usr/bin/env python3
"""Build five strictly causal recent positive-author IDs for one 27K split."""
from __future__ import annotations

import argparse
import hashlib
import json
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


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def update_recent(recent: np.ndarray, positive_authors: np.ndarray) -> None:
    """Append positive authors in stable source order, newest first."""
    for author in positive_authors:
        recent[1:] = recent[:-1]
        recent[0] = author


def build(cache_dir: Path, split: str) -> dict[str, object]:
    started = time.time()
    manifest_path = cache_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    if manifest.get("retained_date_range") != [20220408, 20220428]:
        raise ValueError("cache is not the locked development range")
    users = np.load(cache_dir / "user.npy", mmap_mode="r")
    authors = np.load(cache_dir / "author.npy", mmap_mode="r")
    dates = np.load(cache_dir / "date.npy", mmap_mode="r")
    times = np.load(cache_dir / "time_ms.npy", mmap_mode="r")
    labels = np.load(cache_dir / "label.npy", mmap_mode="r")
    row_count = int(manifest["rows"])
    if {len(users), len(authors), len(dates), len(times), len(labels)} != {row_count}:
        raise ValueError("positive-author source arrays have different lengths")
    lo, hi = SPLITS[split]
    train_indices = np.flatnonzero((dates >= lo) & (dates <= hi)).astype(np.int64)
    train_users = np.asarray(users[train_indices], dtype=np.int32)
    train_times = np.asarray(times[train_indices], dtype=np.int64)
    order = np.lexsort((train_indices, train_times, train_users))
    ordered = train_indices[order]
    ordered_users = train_users[order]
    starts = np.r_[0, np.flatnonzero(ordered_users[1:] != ordered_users[:-1]) + 1]
    ends = np.r_[starts[1:], len(ordered)]
    output_path = cache_dir / f"positive_author_sequence_{split}.npy"
    if output_path.exists():
        raise FileExistsError(output_path)
    output = np.lib.format.open_memmap(
        output_path, mode="w+", dtype="int32", shape=(row_count, 5)
    )
    output[:] = -1
    final_recent = np.full((int(manifest["user_count"]), 5), -1, dtype=np.int32)
    simultaneous_batches = 0
    timestamp_inversions = 0
    for user_start, user_end in zip(starts, ends):
        indices = ordered[user_start:user_end]
        user = int(users[indices[0]])
        user_times = np.asarray(times[indices], dtype=np.int64)
        inversions = int(np.sum(user_times[1:] < user_times[:-1]))
        timestamp_inversions += inversions
        if inversions:
            raise ValueError("positive-author history is not chronological")
        recent = np.full(5, -1, dtype=np.int32)
        position = 0
        while position < len(indices):
            end = position + 1
            while end < len(indices) and user_times[end] == user_times[position]:
                end += 1
            batch = indices[position:end]
            output[batch] = recent
            batch_authors = np.asarray(authors[batch], dtype=np.int32)
            batch_labels = np.asarray(labels[batch], dtype=np.uint8)
            update_recent(recent, batch_authors[(batch_authors >= 0) & (batch_labels == 1)])
            simultaneous_batches += int(len(batch) > 1)
            position = end
        final_recent[user] = recent
    score_indices = np.flatnonzero(dates > hi).astype(np.int64)
    output[score_indices] = final_recent[np.asarray(users[score_indices], dtype=np.int64)]
    output.flush()
    return {
        "split": split,
        "train_bounds": [lo, hi],
        "train_rows": int(len(train_indices)),
        "frozen_score_rows": int(len(score_indices)),
        "timestamp_inversions": timestamp_inversions,
        "simultaneous_multirow_batches": simultaneous_batches,
        "path": output_path.name,
        "shape": [row_count, 5],
        "dtype": "int32",
        "bytes": output_path.stat().st_size,
        "sha256": sha256(output_path),
        "base_cache_manifest_sha256": sha256(manifest_path),
        "causal_contract": (
            "Training rows use only strictly earlier user timestamps; equal-time "
            "rows update only after the entire batch; scoring rows freeze at cutoff."
        ),
        "elapsed_seconds": time.time() - started,
        "max_rss_bytes": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache-dir", type=Path, required=True)
    parser.add_argument("--split", choices=tuple(SPLITS), required=True)
    args = parser.parse_args()
    record_path = args.cache_dir / "positive_author_sequence_manifest.json"
    previous = json.loads(record_path.read_text()) if record_path.exists() else {
        "format_version": 1,
        "history_length": 5,
        "positive_rule": "long_view == 1 and author >= 0",
        "splits": {},
    }
    if args.split in previous.get("splits", {}):
        raise FileExistsError(f"positive-author sequence already exists for {args.split}")
    record = build(args.cache_dir, args.split)
    previous["splits"][args.split] = record
    record_path.write_text(json.dumps(previous, indent=2, sort_keys=True) + "\n")
    print(json.dumps(previous, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
