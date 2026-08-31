#!/usr/bin/env python3
"""Build causal per-user creator exposure and positive-recency buckets."""
from __future__ import annotations

import argparse
import hashlib
import json
import resource
import time
from pathlib import Path

import numpy as np

try:
    from scripts.prepare_kuairand_1k_history import SPLITS, sha256
    from scripts.prepare_kuairand_27k_user_entity_history import (
        source_segments,
        user_indices,
    )
except ModuleNotFoundError:  # Direct ``python scripts/...`` execution.
    from prepare_kuairand_1k_history import SPLITS, sha256
    from prepare_kuairand_27k_user_entity_history import source_segments, user_indices


FEATURE_NAMES = (
    "prior_user_author_exposure_gap_hours_log2",
    "prior_user_author_long_view_gap_hours_log2",
)
NEVER_BUCKET = 16
MAX_GAP_BUCKET = 15
MILLISECONDS_PER_HOUR = 3_600_000.0
GROUP_SHIFT = np.int64(1 << 32)


def gap_bucket(current_time: np.ndarray, prior_time: np.ndarray) -> np.ndarray:
    """Map nonnegative millisecond gaps to log2-hour buckets plus never."""
    current_time = np.asarray(current_time, dtype=np.int64)
    prior_time = np.asarray(prior_time, dtype=np.int64)
    if current_time.shape != prior_time.shape:
        raise ValueError("current and prior times must have matching shapes")
    result = np.full(current_time.shape, NEVER_BUCKET, dtype=np.int16)
    seen = prior_time >= 0
    if np.any(seen):
        delta = current_time[seen] - prior_time[seen]
        if np.any(delta < 0):
            raise ValueError("prior author time occurs after current time")
        result[seen] = np.minimum(
            np.floor(np.log2(delta / MILLISECONDS_PER_HOUR + 1.0)),
            MAX_GAP_BUCKET,
        ).astype(np.int16)
    return result


def prior_batch_time(
    batch_author: np.ndarray,
    batch_time: np.ndarray,
    update: np.ndarray,
) -> np.ndarray:
    """Return the last updating batch time before each author/time batch."""
    batch_author = np.asarray(batch_author, dtype=np.int64)
    batch_time = np.asarray(batch_time, dtype=np.int64)
    update = np.asarray(update, dtype=np.bool_)
    if not (batch_author.shape == batch_time.shape == update.shape):
        raise ValueError("batch recency inputs must have matching shapes")
    if not len(batch_author):
        return np.empty(0, dtype=np.int64)
    identity_start = np.r_[True, batch_author[1:] != batch_author[:-1]]
    group = np.cumsum(identity_start, dtype=np.int64) - 1
    relative_time = batch_time - batch_time.min()
    if np.any(relative_time >= GROUP_SHIFT):
        raise ValueError("per-user timestamp span exceeds recency group shift")
    base = group * GROUP_SHIFT
    candidates = np.where(update, base + relative_time, base - 1)
    latest = np.maximum.accumulate(candidates)
    prior_encoded = np.r_[base[0] - 1, latest[:-1]]
    prior_encoded[identity_start] = base[identity_start] - 1
    prior_relative = prior_encoded - base
    result = np.full(len(batch_time), -1, dtype=np.int64)
    seen = prior_relative >= 0
    result[seen] = prior_relative[seen] + batch_time.min()
    return result


def causal_author_recency_features(
    authors: np.ndarray,
    times: np.ndarray,
    dates: np.ndarray,
    labels: np.ndarray,
    cutoff: int,
) -> np.ndarray:
    """Return prior exposure/positive recency for one user's author sequence."""
    authors = np.asarray(authors, dtype=np.int64)
    times = np.asarray(times, dtype=np.int64)
    dates = np.asarray(dates, dtype=np.int32)
    labels = np.asarray(labels, dtype=np.uint8)
    if not (authors.shape == times.shape == dates.shape == labels.shape):
        raise ValueError("author recency inputs must have matching shapes")
    if np.any(labels > 1):
        raise ValueError("long-view labels must be binary")
    output = np.full((len(authors), 2), NEVER_BUCKET, dtype=np.int16)
    valid = authors >= 0
    if not np.any(valid):
        return output

    positions = np.flatnonzero(valid)
    order = np.lexsort((positions, times[positions], authors[positions]))
    selected = positions[order]
    ordered_author = authors[selected]
    ordered_time = times[selected]
    batch_starts = np.r_[
        0,
        np.flatnonzero(
            (ordered_author[1:] != ordered_author[:-1])
            | (ordered_time[1:] != ordered_time[:-1])
        )
        + 1,
    ].astype(np.int64)
    batch_ends = np.r_[batch_starts[1:], len(selected)]
    batch_sizes = batch_ends - batch_starts
    batch_author = ordered_author[batch_starts]
    batch_time = ordered_time[batch_starts]

    eligible = dates[selected] <= cutoff
    batch_eligible_count = np.add.reduceat(eligible.astype(np.int64), batch_starts)
    batch_positive = np.add.reduceat(
        labels[selected].astype(np.int64) * eligible.astype(np.int64), batch_starts
    )
    prior_exposure = prior_batch_time(
        batch_author, batch_time, batch_eligible_count > 0
    )
    prior_positive = prior_batch_time(batch_author, batch_time, batch_positive > 0)
    output[selected, 0] = np.repeat(
        gap_bucket(batch_time, prior_exposure), batch_sizes
    )
    output[selected, 1] = np.repeat(
        gap_bucket(batch_time, prior_positive), batch_sizes
    )
    return output


def build_split(cache_dir: Path, split: str, cutoff: int) -> dict[str, object]:
    users = np.load(cache_dir / "user.npy", mmap_mode="r")
    authors = np.load(cache_dir / "author.npy", mmap_mode="r")
    times = np.load(cache_dir / "time_ms.npy", mmap_mode="r")
    dates = np.load(cache_dir / "date.npy", mmap_mode="r")
    labels = np.load(cache_dir / "label.npy", mmap_mode="r")
    manifest = json.loads((cache_dir / "manifest.json").read_text())
    row_count = int(manifest["rows"])
    if any(len(array) != row_count for array in (users, authors, times, dates, labels)):
        raise ValueError("user-author recency input lengths do not match manifest")

    segments = source_segments(users)
    output_path = cache_dir / f"user_author_recency_{split}.npy"
    output = np.lib.format.open_memmap(
        output_path, mode="w+", dtype="int16", shape=(row_count, len(FEATURE_NAMES))
    )
    written = 0
    for user in range(int(manifest["user_count"])):
        indices = user_indices(users, segments, user)
        if not len(indices):
            continue
        output[indices] = causal_author_recency_features(
            authors[indices], times[indices], dates[indices], labels[indices], cutoff
        )
        written += len(indices)
    if written != row_count:
        raise RuntimeError(f"user-author recency rows mismatch: {written} != {row_count}")
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
    expected = "KuaiRand-27K full-training deterministic development sample"
    if manifest.get("benchmark") != expected:
        raise ValueError("user-author recency requires the verified full-training cache")

    split = args.split
    record_path = cache_dir / "user_author_recency_manifest.json"
    previous = json.loads(record_path.read_text()) if record_path.is_file() else {}
    splits = dict(previous.get("splits", {}))
    if split in splits:
        raise FileExistsError(f"user-author recency already exists for {split}")
    splits[split] = build_split(cache_dir, split, SPLITS[split][1])
    record = {
        "format_version": 1,
        "feature_names": FEATURE_NAMES,
        "never_bucket": NEVER_BUCKET,
        "max_gap_bucket": MAX_GAP_BUCKET,
        "gap_definition": "floor(log2(elapsed_hours + 1)), capped at 15; never is 16",
        "causal_contract": (
            "Per-user author exposure and long-view timestamps use only earlier "
            "timestamps through the training cutoff; same-timestamp rows update "
            "after the whole batch and validation/forward state is frozen."
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
