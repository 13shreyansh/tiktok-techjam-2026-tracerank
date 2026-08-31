#!/usr/bin/env python3
"""Build fixed three-day causal video/author trend fields."""
from __future__ import annotations

import argparse
import json
import resource
import time
from collections import deque
from pathlib import Path

import numpy as np

try:
    from scripts.prepare_kuairand_1k_history import SPLITS, rate_bucket, sha256
    from scripts.prepare_kuairand_27k_item_history import (
        DEV_DATES,
        log_buckets,
        video_author_map,
    )
except ModuleNotFoundError:  # Direct ``python scripts/...`` execution.
    from prepare_kuairand_1k_history import SPLITS, rate_bucket, sha256
    from prepare_kuairand_27k_item_history import DEV_DATES, log_buckets, video_author_map


WINDOW_DAYS = 3
FEATURE_NAMES = (
    "prior_day_video_count_log2",
    "prior_day_video_long_view_rate_21",
    "prior_day_author_count_log2",
    "prior_day_author_long_view_rate_21",
    "prior_3d_video_count_log2",
    "prior_3d_video_long_view_rate_21",
    "prior_3d_author_count_log2",
    "prior_3d_author_long_view_rate_21",
)


def build_split(cache_dir: Path, work_dir: Path, split: str, cutoff: int) -> dict[str, object]:
    manifest = json.loads((cache_dir / "manifest.json").read_text())
    row_dates = np.load(cache_dir / "date.npy", mmap_mode="r")
    row_videos = np.load(cache_dir / "video.npy", mmap_mode="r")
    row_authors = np.load(cache_dir / "author.npy", mmap_mode="r")
    daily_count = np.load(work_dir / "item_daily_count.npy", mmap_mode="r")
    daily_positive = np.load(work_dir / "item_daily_positive.npy", mmap_mode="r")
    base = np.load(cache_dir / f"item_history_{split}.npy", mmap_mode="r")
    mapping = video_author_map(cache_dir)
    video_count = int(manifest["video_count"])
    author_count = int(manifest["author_count"])
    recent_video = np.zeros(video_count, dtype=np.uint64)
    positive_video = np.zeros(video_count, dtype=np.uint64)
    recent_author = np.zeros(author_count, dtype=np.uint64)
    positive_author = np.zeros(author_count, dtype=np.uint64)
    video_days: deque[tuple[np.ndarray, np.ndarray]] = deque()
    author_days: deque[tuple[np.ndarray, np.ndarray]] = deque()
    output_path = cache_dir / f"item_trend_{split}.npy"
    output = np.lib.format.open_memmap(
        output_path,
        mode="w+",
        dtype="int16",
        shape=(int(manifest["rows"]), len(FEATURE_NAMES)),
    )
    output[:, :4] = base
    written = 0
    for day_index, date in enumerate(DEV_DATES):
        indices = np.flatnonzero(row_dates == date).astype(np.int64)
        videos = np.asarray(row_videos[indices], dtype=np.int64)
        authors = np.asarray(row_authors[indices], dtype=np.int64)
        output[indices, 4] = log_buckets(recent_video[videos])
        output[indices, 5] = rate_bucket(positive_video[videos], recent_video[videos])
        output[indices, 6] = 0
        output[indices, 7] = int(rate_bucket(0, 0))
        valid_author = authors >= 0
        if np.any(valid_author):
            selected = indices[valid_author]
            author_values = authors[valid_author]
            output[selected, 6] = log_buckets(recent_author[author_values])
            output[selected, 7] = rate_bucket(
                positive_author[author_values], recent_author[author_values]
            )
        written += len(indices)
        if int(date) <= cutoff:
            day_count = np.asarray(daily_count[day_index], dtype=np.uint64).copy()
            day_positive = np.asarray(daily_positive[day_index], dtype=np.uint64).copy()
            day_author = np.zeros(author_count, dtype=np.uint64)
            day_author_positive = np.zeros(author_count, dtype=np.uint64)
            active = (mapping >= 0) & (day_count > 0)
            np.add.at(day_author, mapping[active], day_count[active])
            np.add.at(day_author_positive, mapping[active], day_positive[active])
            recent_video += day_count
            positive_video += day_positive
            recent_author += day_author
            positive_author += day_author_positive
            video_days.append((day_count, day_positive))
            author_days.append((day_author, day_author_positive))
            if len(video_days) > WINDOW_DAYS:
                old_count, old_positive = video_days.popleft()
                old_author, old_author_positive = author_days.popleft()
                recent_video -= old_count
                positive_video -= old_positive
                recent_author -= old_author
                positive_author -= old_author_positive
    if written != int(manifest["rows"]):
        raise RuntimeError(f"item-trend row mismatch: {written} != {manifest['rows']}")
    output.flush()
    return {
        "split": split,
        "train_bounds": list(SPLITS.get(split, (int(DEV_DATES[0]), cutoff))),
        "path": output_path.name,
        "bytes": output_path.stat().st_size,
        "sha256": sha256(output_path),
        "sample_rows": written,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache-dir", type=Path, required=True)
    args = parser.parse_args()
    started = time.time()
    cache_dir = args.cache_dir.resolve()
    manifest = json.loads((cache_dir / "manifest.json").read_text())
    if manifest.get("benchmark") != "KuaiRand-27K deterministic development sample":
        raise ValueError("causal item trend requires the verified 27K sampled cache")
    work_dir = cache_dir / "full_history_work"
    for required in (
        work_dir / "item_daily_count.npy",
        work_dir / "item_daily_positive.npy",
        cache_dir / "item_history_manifest.json",
    ):
        if not required.is_file():
            raise FileNotFoundError(required)
    splits = {
        split: build_split(cache_dir, work_dir, split, bounds[1])
        for split, bounds in SPLITS.items()
    }
    record = {
        "format_version": 1,
        "base_cache_manifest_sha256": sha256(cache_dir / "manifest.json"),
        "item_history_manifest_sha256": sha256(cache_dir / "item_history_manifest.json"),
        "causal_contract": (
            "Trend fields use the final three eligible calendar days before a "
            "training row and freeze the final three training days for scoring rows."
        ),
        "window_days": WINDOW_DAYS,
        "feature_names": list(FEATURE_NAMES),
        "splits": splits,
        "elapsed_seconds": time.time() - started,
        "max_rss_bytes": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
    }
    (cache_dir / "item_trend_manifest.json").write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(record, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
