#!/usr/bin/env python3
"""Add causal strong-feedback and hate item/author rates to the 27K sample."""
from __future__ import annotations

import argparse
import json
import resource
import time
from pathlib import Path

import numpy as np

try:
    from scripts.prepare_kuairand_1k_history import SPLITS, rate_bucket, sha256
    from scripts.prepare_kuairand_27k_item_history import DEV_DATES, video_author_map
except ModuleNotFoundError:  # Direct ``python scripts/...`` execution.
    from prepare_kuairand_1k_history import SPLITS, rate_bucket, sha256
    from prepare_kuairand_27k_item_history import DEV_DATES, video_author_map


FEATURE_NAMES = (
    "prior_day_video_count_log2",
    "prior_day_video_long_view_rate_21",
    "prior_day_author_count_log2",
    "prior_day_author_long_view_rate_21",
    "prior_day_video_strong_feedback_rate_21",
    "prior_day_video_hate_rate_21",
    "prior_day_author_strong_feedback_rate_21",
    "prior_day_author_hate_rate_21",
)


def build_daily_behavior(cache_dir: Path, work_dir: Path) -> dict[str, object]:
    source_ids = np.load(cache_dir / "source_video_ids.npy", mmap_mode="r")
    videos = np.load(work_dir / "video_source_id.npy", mmap_mode="r")
    dates = np.load(work_dir / "date.npy", mmap_mode="r")
    strong = np.load(work_dir / "strong.npy", mmap_mode="r")
    hate = np.load(work_dir / "hate.npy", mmap_mode="r")
    video_count = len(source_ids)
    strong_path = work_dir / "item_daily_strong.npy"
    hate_path = work_dir / "item_daily_hate.npy"
    daily_strong = np.lib.format.open_memmap(
        strong_path, mode="w+", dtype="uint32", shape=(len(DEV_DATES), video_count)
    )
    daily_hate = np.lib.format.open_memmap(
        hate_path, mode="w+", dtype="uint32", shape=(len(DEV_DATES), video_count)
    )
    daily_strong[:] = 0
    daily_hate[:] = 0
    flat_strong = daily_strong.reshape(-1)
    flat_hate = daily_hate.reshape(-1)
    matched = 0
    chunk = 1_000_000
    for start in range(0, len(videos), chunk):
        end = min(start + chunk, len(videos))
        values = np.asarray(videos[start:end], dtype=np.int32)
        positions = np.searchsorted(source_ids, values)
        valid = positions < video_count
        valid[valid] &= source_ids[positions[valid]] == values[valid]
        if not np.any(valid):
            continue
        day = np.asarray(dates[start:end], dtype=np.int32)[valid] % 100 - 8
        if np.any((day < 0) | (day >= len(DEV_DATES))):
            raise ValueError("retained work contains a date outside April 8-28")
        flat = day.astype(np.int64) * video_count + positions[valid]
        np.add.at(
            flat_strong, flat, np.asarray(strong[start:end], dtype=np.uint8)[valid]
        )
        np.add.at(flat_hate, flat, np.asarray(hate[start:end], dtype=np.uint8)[valid])
        matched += int(valid.sum())
    daily_strong.flush()
    daily_hate.flush()
    daily_count = np.load(work_dir / "item_daily_count.npy", mmap_mode="r")
    if np.any(daily_strong > daily_count) or np.any(daily_hate > daily_count):
        raise RuntimeError("behavior total exceeds exposure total")
    return {
        "matched_full_events": matched,
        "strong_path": strong_path.name,
        "hate_path": hate_path.name,
        "strong_sha256": sha256(strong_path),
        "hate_sha256": sha256(hate_path),
    }


def build_split(cache_dir: Path, work_dir: Path, split: str, cutoff: int) -> dict[str, object]:
    manifest = json.loads((cache_dir / "manifest.json").read_text())
    row_dates = np.load(cache_dir / "date.npy", mmap_mode="r")
    row_videos = np.load(cache_dir / "video.npy", mmap_mode="r")
    row_authors = np.load(cache_dir / "author.npy", mmap_mode="r")
    daily_count = np.load(work_dir / "item_daily_count.npy", mmap_mode="r")
    daily_strong = np.load(work_dir / "item_daily_strong.npy", mmap_mode="r")
    daily_hate = np.load(work_dir / "item_daily_hate.npy", mmap_mode="r")
    base = np.load(cache_dir / f"item_history_{split}.npy", mmap_mode="r")
    mapping = video_author_map(cache_dir)
    video_count = int(manifest["video_count"])
    author_count = int(manifest["author_count"])
    seen_video = np.zeros(video_count, dtype=np.uint64)
    strong_video = np.zeros(video_count, dtype=np.uint64)
    hate_video = np.zeros(video_count, dtype=np.uint64)
    seen_author = np.zeros(author_count, dtype=np.uint64)
    strong_author = np.zeros(author_count, dtype=np.uint64)
    hate_author = np.zeros(author_count, dtype=np.uint64)
    output_path = cache_dir / f"item_behavior_{split}.npy"
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
        output[indices, 4] = rate_bucket(strong_video[videos], seen_video[videos])
        output[indices, 5] = rate_bucket(hate_video[videos], seen_video[videos])
        output[indices, 6] = int(rate_bucket(0, 0))
        output[indices, 7] = int(rate_bucket(0, 0))
        valid_author = authors >= 0
        if np.any(valid_author):
            selected = indices[valid_author]
            author_values = authors[valid_author]
            output[selected, 6] = rate_bucket(
                strong_author[author_values], seen_author[author_values]
            )
            output[selected, 7] = rate_bucket(
                hate_author[author_values], seen_author[author_values]
            )
        written += len(indices)
        if int(date) <= cutoff:
            day_count = np.asarray(daily_count[day_index], dtype=np.uint64)
            day_strong = np.asarray(daily_strong[day_index], dtype=np.uint64)
            day_hate = np.asarray(daily_hate[day_index], dtype=np.uint64)
            seen_video += day_count
            strong_video += day_strong
            hate_video += day_hate
            active = (mapping >= 0) & (day_count > 0)
            np.add.at(seen_author, mapping[active], day_count[active])
            np.add.at(strong_author, mapping[active], day_strong[active])
            np.add.at(hate_author, mapping[active], day_hate[active])
    if written != int(manifest["rows"]):
        raise RuntimeError(f"item-behavior row mismatch: {written} != {manifest['rows']}")
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
        raise ValueError("causal item behavior requires the verified 27K sampled cache")
    work_dir = cache_dir / "full_history_work"
    for required in (
        work_dir / "video_source_id.npy",
        work_dir / "item_daily_count.npy",
        cache_dir / "item_history_manifest.json",
    ):
        if not required.is_file():
            raise FileNotFoundError(required)
    daily = build_daily_behavior(cache_dir, work_dir)
    splits = {
        split: build_split(cache_dir, work_dir, split, bounds[1])
        for split, bounds in SPLITS.items()
    }
    record = {
        "format_version": 1,
        "base_cache_manifest_sha256": sha256(cache_dir / "manifest.json"),
        "item_history_manifest_sha256": sha256(cache_dir / "item_history_manifest.json"),
        "causal_contract": (
            "Strong-feedback and hate rates use all sampled-video events from "
            "earlier calendar days; scoring rows freeze at the split cutoff."
        ),
        "strong_feedback_definition": "is_like OR is_follow OR is_comment OR is_forward",
        "feature_names": list(FEATURE_NAMES),
        "daily": daily,
        "splits": splits,
        "elapsed_seconds": time.time() - started,
        "max_rss_bytes": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
    }
    (cache_dir / "item_behavior_manifest.json").write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(record, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
