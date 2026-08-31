#!/usr/bin/env python3
"""Build causal per-user creator strong/negative feedback rates.

For each user-author pair, rows receive rates from strictly earlier timestamps.
Rows sharing the same timestamp update together. Outcomes after the declared
training cutoff are masked, so validation and forward features remain frozen.
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
    from scripts.prepare_kuairand_27k_user_entity_history import (
        source_segments,
        user_indices,
    )
except ModuleNotFoundError:  # Direct ``python scripts/...`` execution.
    from prepare_kuairand_1k_history import SPLITS, rate_bucket, sha256
    from prepare_kuairand_27k_user_entity_history import source_segments, user_indices


FEATURE_NAMES = (
    "prior_user_author_strong_feedback_rate_21",
    "prior_user_author_hate_rate_21",
)


def causal_author_behavior_features(
    authors: np.ndarray,
    times: np.ndarray,
    dates: np.ndarray,
    strong: np.ndarray,
    hate: np.ndarray,
    cutoff: int,
) -> np.ndarray:
    """Return prior strong/hate rate buckets for one user's creator sequence."""
    authors = np.asarray(authors, dtype=np.int64)
    times = np.asarray(times, dtype=np.int64)
    dates = np.asarray(dates, dtype=np.int32)
    strong = np.asarray(strong, dtype=np.uint8)
    hate = np.asarray(hate, dtype=np.uint8)
    if not (
        authors.shape == times.shape == dates.shape == strong.shape == hate.shape
    ):
        raise ValueError("author behavior inputs must have matching shapes")
    if np.any((strong > 1) | (hate > 1)):
        raise ValueError("author behavior outcomes must be binary")

    prior = int(rate_bucket(0, 0))
    output = np.full((len(authors), 2), prior, dtype=np.int16)
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

    eligible = dates[selected] <= cutoff
    eligible_count = eligible.astype(np.int64)
    eligible_strong = strong[selected].astype(np.int64) * eligible_count
    eligible_hate = hate[selected].astype(np.int64) * eligible_count
    batch_count = np.add.reduceat(eligible_count, batch_starts)
    batch_strong = np.add.reduceat(eligible_strong, batch_starts)
    batch_hate = np.add.reduceat(eligible_hate, batch_starts)

    cumulative_count = np.cumsum(batch_count) - batch_count
    cumulative_strong = np.cumsum(batch_strong) - batch_strong
    cumulative_hate = np.cumsum(batch_hate) - batch_hate
    batch_author = ordered_author[batch_starts]
    identity_start = np.r_[True, batch_author[1:] != batch_author[:-1]]
    roots = np.maximum.accumulate(
        np.where(identity_start, np.arange(len(batch_starts)), 0)
    )
    prior_count = cumulative_count - cumulative_count[roots]
    prior_strong = cumulative_strong - cumulative_strong[roots]
    prior_hate = cumulative_hate - cumulative_hate[roots]

    row_count = np.repeat(prior_count, batch_sizes)
    output[selected, 0] = rate_bucket(np.repeat(prior_strong, batch_sizes), row_count)
    output[selected, 1] = rate_bucket(np.repeat(prior_hate, batch_sizes), row_count)
    return output


def build_split(cache_dir: Path, split: str, cutoff: int) -> dict[str, object]:
    users = np.load(cache_dir / "user.npy", mmap_mode="r")
    authors = np.load(cache_dir / "author.npy", mmap_mode="r")
    times = np.load(cache_dir / "time_ms.npy", mmap_mode="r")
    dates = np.load(cache_dir / "date.npy", mmap_mode="r")
    likes = np.load(cache_dir / "is_like.npy", mmap_mode="r")
    follows = np.load(cache_dir / "is_follow.npy", mmap_mode="r")
    comments = np.load(cache_dir / "is_comment.npy", mmap_mode="r")
    forwards = np.load(cache_dir / "is_forward.npy", mmap_mode="r")
    hates = np.load(cache_dir / "is_hate.npy", mmap_mode="r")
    manifest = json.loads((cache_dir / "manifest.json").read_text())
    row_count = int(manifest["rows"])
    arrays = (users, authors, times, dates, likes, follows, comments, forwards, hates)
    if any(len(array) != row_count for array in arrays):
        raise ValueError("user-author behavior input lengths do not match manifest")

    segments = source_segments(users)
    output_path = cache_dir / f"user_author_behavior_{split}.npy"
    output = np.lib.format.open_memmap(
        output_path, mode="w+", dtype="int16", shape=(row_count, len(FEATURE_NAMES))
    )
    written = 0
    for user in range(int(manifest["user_count"])):
        indices = user_indices(users, segments, user)
        if not len(indices):
            continue
        strong = (
            np.asarray(likes[indices], dtype=np.uint8)
            | np.asarray(follows[indices], dtype=np.uint8)
            | np.asarray(comments[indices], dtype=np.uint8)
            | np.asarray(forwards[indices], dtype=np.uint8)
        )
        output[indices] = causal_author_behavior_features(
            authors[indices],
            times[indices],
            dates[indices],
            strong,
            hates[indices],
            cutoff,
        )
        written += len(indices)
    if written != row_count:
        raise RuntimeError(f"user-author behavior rows mismatch: {written} != {row_count}")
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
        raise ValueError("user-author behavior requires the verified full-training cache")

    split = args.split
    record_path = cache_dir / "user_author_behavior_manifest.json"
    previous = json.loads(record_path.read_text()) if record_path.is_file() else {}
    splits = dict(previous.get("splits", {}))
    if split in splits:
        raise FileExistsError(f"user-author behavior already exists for {split}")
    splits[split] = build_split(cache_dir, split, SPLITS[split][1])
    record = {
        "format_version": 1,
        "feature_names": FEATURE_NAMES,
        "strong_feedback_definition": "is_like OR is_follow OR is_comment OR is_forward",
        "causal_contract": (
            "Per-user author rates use only earlier timestamps through the training "
            "cutoff; same-timestamp rows update after the whole batch and validation/"
            "forward state is frozen."
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
