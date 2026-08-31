#!/usr/bin/env python3
"""Build causal per-user creator/video repeat features for KuaiRand-27K.

The full cache is a concatenation of four source files, each sorted by user.
For every user, this builder gathers the user's rows from those monotonic
segments, orders them stably by entity and timestamp, and emits prior-only
counts and smoothed long-view rates. Rows at the same timestamp never update
one another. Outcomes after the declared training cutoff are masked before
aggregation, so validation and forward features remain frozen.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import resource
import time
from pathlib import Path

import numpy as np

try:
    from scripts.prepare_kuairand_1k_history import SPLITS, rate_bucket, sha256
except ModuleNotFoundError:  # Direct ``python scripts/...`` execution.
    from prepare_kuairand_1k_history import SPLITS, rate_bucket, sha256


FEATURE_NAMES = (
    "prior_user_author_count_log2",
    "prior_user_author_long_view_rate_21",
    "prior_user_video_count_log2",
    "prior_user_video_long_view_rate_21",
)


def source_segments(users: np.ndarray) -> list[tuple[int, int]]:
    """Return monotonic user-id segments and reject an unexpected layout."""
    inversions = np.flatnonzero(users[1:] < users[:-1]) + 1
    bounds = np.r_[0, inversions, len(users)].astype(np.int64)
    segments = [(int(left), int(right)) for left, right in zip(bounds[:-1], bounds[1:])]
    for left, right in segments:
        if np.any(users[left + 1 : right] < users[left : right - 1]):
            raise ValueError("cache user segment is not monotonic")
    return segments


def causal_entity_features(
    entity: np.ndarray,
    times: np.ndarray,
    dates: np.ndarray,
    labels: np.ndarray,
    cutoff: int,
) -> np.ndarray:
    """Return prior count/rate buckets for one user's entity sequence."""
    entity = np.asarray(entity, dtype=np.int64)
    times = np.asarray(times, dtype=np.int64)
    dates = np.asarray(dates, dtype=np.int32)
    labels = np.asarray(labels, dtype=np.uint8)
    output = np.empty((len(entity), 2), dtype=np.int16)
    output[:, 0] = 0
    output[:, 1] = int(rate_bucket(0, 0))
    valid = entity >= 0
    if not np.any(valid):
        return output

    positions = np.flatnonzero(valid)
    order = np.lexsort((positions, times[positions], entity[positions]))
    selected = positions[order]
    ordered_entity = entity[selected]
    ordered_time = times[selected]
    batch_starts = np.r_[
        0,
        np.flatnonzero(
            (ordered_entity[1:] != ordered_entity[:-1])
            | (ordered_time[1:] != ordered_time[:-1])
        )
        + 1,
    ].astype(np.int64)
    batch_ends = np.r_[batch_starts[1:], len(selected)]
    batch_sizes = batch_ends - batch_starts

    eligible = dates[selected] <= cutoff
    positive = np.zeros(len(selected), dtype=np.int64)
    positive[eligible] = labels[selected[eligible]]
    batch_count = np.add.reduceat(eligible.astype(np.int64), batch_starts)
    batch_positive = np.add.reduceat(positive, batch_starts)
    cumulative_count_before = np.cumsum(batch_count) - batch_count
    cumulative_positive_before = np.cumsum(batch_positive) - batch_positive

    batch_entity = ordered_entity[batch_starts]
    identity_start = np.r_[True, batch_entity[1:] != batch_entity[:-1]]
    roots = np.maximum.accumulate(
        np.where(identity_start, np.arange(len(batch_starts)), 0)
    )
    prior_count = cumulative_count_before - cumulative_count_before[roots]
    prior_positive = cumulative_positive_before - cumulative_positive_before[roots]
    row_count = np.repeat(prior_count, batch_sizes)
    row_positive = np.repeat(prior_positive, batch_sizes)

    count_bucket = np.minimum(
        np.floor(np.log2(row_count + 1)), 15
    ).astype(np.int16)
    output[selected, 0] = count_bucket
    output[selected, 1] = rate_bucket(row_positive, row_count)
    return output


def user_indices(
    users: np.ndarray, segments: list[tuple[int, int]], user: int
) -> np.ndarray:
    ranges: list[np.ndarray] = []
    for left, right in segments:
        segment = users[left:right]
        lo = left + int(np.searchsorted(segment, user, side="left"))
        hi = left + int(np.searchsorted(segment, user, side="right"))
        if hi > lo:
            ranges.append(np.arange(lo, hi, dtype=np.int64))
    if not ranges:
        return np.empty(0, dtype=np.int64)
    return ranges[0] if len(ranges) == 1 else np.concatenate(ranges)


def build_split(cache_dir: Path, split: str, cutoff: int) -> dict[str, object]:
    users = np.load(cache_dir / "user.npy", mmap_mode="r")
    videos = np.load(cache_dir / "video.npy", mmap_mode="r")
    authors = np.load(cache_dir / "author.npy", mmap_mode="r")
    times = np.load(cache_dir / "time_ms.npy", mmap_mode="r")
    dates = np.load(cache_dir / "date.npy", mmap_mode="r")
    labels = np.load(cache_dir / "label.npy", mmap_mode="r")
    manifest = json.loads((cache_dir / "manifest.json").read_text())
    row_count = int(manifest["rows"])
    if any(len(array) != row_count for array in (users, videos, authors, times, dates, labels)):
        raise ValueError("user-entity history input lengths do not match manifest")
    segments = source_segments(users)
    output_path = cache_dir / f"user_entity_history_{split}.npy"
    output = np.lib.format.open_memmap(
        output_path, mode="w+", dtype="int16", shape=(row_count, len(FEATURE_NAMES))
    )
    written = 0
    for user in range(int(manifest["user_count"])):
        indices = user_indices(users, segments, user)
        if not len(indices):
            continue
        local_times = np.asarray(times[indices], dtype=np.int64)
        local_dates = np.asarray(dates[indices], dtype=np.int32)
        local_labels = np.asarray(labels[indices], dtype=np.uint8)
        output[indices, :2] = causal_entity_features(
            authors[indices], local_times, local_dates, local_labels, cutoff
        )
        output[indices, 2:] = causal_entity_features(
            videos[indices], local_times, local_dates, local_labels, cutoff
        )
        written += len(indices)
    if written != row_count:
        raise RuntimeError(f"user-entity feature rows mismatch: {written} != {row_count}")
    output.flush()
    return {
        "split": split,
        "train_bounds": list(SPLITS[split]),
        "path": output_path.name,
        "bytes": output_path.stat().st_size,
        "sha256": sha256(output_path),
        "rows": written,
        "source_user_segments": len(segments),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache-dir", type=Path, required=True)
    parser.add_argument("--split", choices=tuple(SPLITS), required=True)
    args = parser.parse_args()
    started = time.time()
    cache_dir = args.cache_dir.resolve()
    manifest_path = cache_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    if manifest.get("benchmark") != "KuaiRand-27K full-training deterministic development sample":
        raise ValueError("user-entity history requires the verified full-training cache")
    split = args.split
    record_path = cache_dir / "user_entity_history_manifest.json"
    previous = json.loads(record_path.read_text()) if record_path.is_file() else {}
    splits = dict(previous.get("splits", {}))
    if split in splits:
        raise FileExistsError(f"user-entity history already exists for {split}")
    result = build_split(cache_dir, split, SPLITS[split][1])
    splits[split] = result
    record = {
        "format_version": 1,
        "feature_names": FEATURE_NAMES,
        "causal_contract": (
            "Per-user author/video fields use only earlier timestamps through the "
            "training cutoff; same-timestamp rows update after the whole batch and "
            "validation/forward state is frozen."
        ),
        "base_cache_manifest_sha256": sha256(manifest_path),
        "splits": splits,
        "last_build_elapsed_seconds": time.time() - started,
        "max_rss_bytes": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    record_path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    print(json.dumps(record, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
