#!/usr/bin/env python3
"""Build leakage-safe item/author history from all KuaiRand-27K dev events.

Only videos present in the fixed deterministic scored sample are tracked.  A
training row receives statistics from earlier calendar days; validation and
forward rows receive state frozen at the split's training cutoff.  This
deliberately conservative day boundary prevents the current row or any
same-day outcome from entering its own features.
"""
from __future__ import annotations

import argparse
import csv
import json
import resource
import time
from pathlib import Path

import numpy as np

try:
    from scripts.prepare_kuairand_1k_history import SPLITS, rate_bucket, sha256
    from scripts.prepare_kuairand_27k_full_history import source_files
    from scripts.sample_kuairand_27k_logs import DEV_END, EXPECTED_COLUMNS
except ModuleNotFoundError:  # Direct ``python scripts/...`` execution.
    from prepare_kuairand_1k_history import SPLITS, rate_bucket, sha256
    from prepare_kuairand_27k_full_history import source_files
    from sample_kuairand_27k_logs import DEV_END, EXPECTED_COLUMNS


DEV_DATES = np.arange(20220408, 20220429, dtype=np.int32)
FEATURE_NAMES = (
    "prior_day_video_count_log2",
    "prior_day_video_long_view_rate_21",
    "prior_day_author_count_log2",
    "prior_day_author_long_view_rate_21",
)
ALLOWED_BENCHMARKS = {
    "KuaiRand-27K deterministic development sample",
    "KuaiRand-27K expanded-training deterministic development sample",
    "KuaiRand-27K quarter-training deterministic development sample",
    "KuaiRand-27K half-training deterministic development sample",
    "KuaiRand-27K full-training deterministic development sample",
}


def validate_cache_benchmark(manifest: dict[str, object]) -> None:
    if manifest.get("benchmark") not in ALLOWED_BENCHMARKS:
        raise ValueError("causal item history requires the verified 27K sampled cache")


def checked_reader(path: Path):
    handle = path.open("r", encoding="utf-8", newline="")
    reader = csv.reader(handle)
    header = tuple(next(reader))
    if header != EXPECTED_COLUMNS:
        handle.close()
        raise ValueError(f"unexpected log schema in {path}: {header}")
    return handle, reader, {name: header.index(name) for name in header}


def ensure_partitioned_video_ids(
    sources: list[Path], work_dir: Path, *, allow_reuse: bool
) -> tuple[Path, bool]:
    """Align raw video IDs with the already-validated user-partitioned work."""
    offsets = np.load(work_dir / "user_offsets.npy", mmap_mode="r")
    retained = int(offsets[-1])
    path = work_dir / "video_source_id.npy"
    if path.exists():
        video = np.load(path, mmap_mode="r")
        if video.shape != (retained,) or video.dtype != np.int32:
            raise ValueError(f"invalid reusable video work array: {video.shape} {video.dtype}")
        if not allow_reuse:
            raise FileExistsError(f"refusing unrequested reuse of {path}")
        return path, True

    video = np.lib.format.open_memmap(path, mode="w+", dtype="int32", shape=(retained,))
    cursor = np.asarray(offsets[:-1], dtype=np.int64).copy()
    for source in sources:
        handle, reader, pos = checked_reader(source)
        with handle:
            for row in reader:
                date = int(row[pos["date"]])
                if date > DEV_END:
                    continue
                user = int(row[pos["user_id"]])
                index = int(cursor[user])
                cursor[user] += 1
                video[index] = int(row[pos["video_id"]])
    if not np.array_equal(cursor, offsets[1:]):
        raise RuntimeError("video fill does not match validated user partition")
    video.flush()
    return path, False


def build_daily_video_totals(cache_dir: Path, work_dir: Path) -> dict[str, object]:
    source_ids = np.load(cache_dir / "source_video_ids.npy", mmap_mode="r")
    videos = np.load(work_dir / "video_source_id.npy", mmap_mode="r")
    dates = np.load(work_dir / "date.npy", mmap_mode="r")
    labels = np.load(work_dir / "label.npy", mmap_mode="r")
    video_count = len(source_ids)
    count_path = work_dir / "item_daily_count.npy"
    positive_path = work_dir / "item_daily_positive.npy"
    daily_count = np.lib.format.open_memmap(
        count_path, mode="w+", dtype="uint32", shape=(len(DEV_DATES), video_count)
    )
    daily_positive = np.lib.format.open_memmap(
        positive_path, mode="w+", dtype="uint32", shape=(len(DEV_DATES), video_count)
    )
    daily_count[:] = 0
    daily_positive[:] = 0
    flat_count = daily_count.reshape(-1)
    flat_positive = daily_positive.reshape(-1)
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
        np.add.at(flat_count, flat, 1)
        np.add.at(
            flat_positive,
            flat,
            np.asarray(labels[start:end], dtype=np.uint8)[valid],
        )
        matched += int(valid.sum())
    daily_count.flush()
    daily_positive.flush()
    if np.any(daily_positive > daily_count):
        raise RuntimeError("daily positive total exceeds exposure total")
    return {
        "matched_full_events": matched,
        "count_path": count_path.name,
        "positive_path": positive_path.name,
        "count_sha256": sha256(count_path),
        "positive_sha256": sha256(positive_path),
    }


def video_author_map(cache_dir: Path) -> np.ndarray:
    manifest = json.loads((cache_dir / "manifest.json").read_text())
    videos = np.load(cache_dir / "video.npy", mmap_mode="r")
    authors = np.load(cache_dir / "author.npy", mmap_mode="r")
    result = np.full(int(manifest["video_count"]), -1, dtype=np.int32)
    chunk = 1_000_000
    for start in range(0, len(videos), chunk):
        end = min(start + chunk, len(videos))
        result[np.asarray(videos[start:end], dtype=np.int64)] = np.asarray(
            authors[start:end], dtype=np.int32
        )
    observed = result[np.asarray(videos, dtype=np.int64)]
    if not np.array_equal(observed, np.asarray(authors, dtype=np.int32)):
        raise ValueError("sampled video maps to inconsistent author IDs")
    return result


def log_buckets(values: np.ndarray) -> np.ndarray:
    return np.minimum(np.floor(np.log2(values.astype(np.float64) + 1.0)), 15).astype(
        np.int16
    )


def build_split(cache_dir: Path, work_dir: Path, split: str, cutoff: int) -> dict[str, object]:
    manifest = json.loads((cache_dir / "manifest.json").read_text())
    row_dates = np.load(cache_dir / "date.npy", mmap_mode="r")
    row_videos = np.load(cache_dir / "video.npy", mmap_mode="r")
    row_authors = np.load(cache_dir / "author.npy", mmap_mode="r")
    daily_count = np.load(work_dir / "item_daily_count.npy", mmap_mode="r")
    daily_positive = np.load(work_dir / "item_daily_positive.npy", mmap_mode="r")
    mapping = video_author_map(cache_dir)
    video_count = int(manifest["video_count"])
    author_count = int(manifest["author_count"])
    seen_video = np.zeros(video_count, dtype=np.uint64)
    positive_video = np.zeros(video_count, dtype=np.uint64)
    seen_author = np.zeros(author_count, dtype=np.uint64)
    positive_author = np.zeros(author_count, dtype=np.uint64)
    output_path = cache_dir / f"item_history_{split}.npy"
    output = np.lib.format.open_memmap(
        output_path,
        mode="w+",
        dtype="int16",
        shape=(int(manifest["rows"]), len(FEATURE_NAMES)),
    )
    written = 0
    for day_index, date in enumerate(DEV_DATES):
        indices = np.flatnonzero(row_dates == date).astype(np.int64)
        videos = np.asarray(row_videos[indices], dtype=np.int64)
        authors = np.asarray(row_authors[indices], dtype=np.int64)
        output[indices, 0] = log_buckets(seen_video[videos])
        output[indices, 1] = rate_bucket(positive_video[videos], seen_video[videos])
        valid_author = authors >= 0
        output[indices, 2] = 0
        output[indices, 3] = int(rate_bucket(0, 0))
        if np.any(valid_author):
            selected = indices[valid_author]
            author_values = authors[valid_author]
            output[selected, 2] = log_buckets(seen_author[author_values])
            output[selected, 3] = rate_bucket(
                positive_author[author_values], seen_author[author_values]
            )
        written += len(indices)
        if int(date) <= cutoff:
            day_count = np.asarray(daily_count[day_index], dtype=np.uint64)
            day_positive = np.asarray(daily_positive[day_index], dtype=np.uint64)
            seen_video += day_count
            positive_video += day_positive
            active = (mapping >= 0) & (day_count > 0)
            np.add.at(seen_author, mapping[active], day_count[active])
            np.add.at(positive_author, mapping[active], day_positive[active])
    if written != int(manifest["rows"]):
        raise RuntimeError(f"item-history row mismatch: {written} != {manifest['rows']}")
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
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--cache-dir", type=Path, required=True)
    parser.add_argument("--reuse-video-work", action="store_true")
    parser.add_argument("--split", choices=tuple(SPLITS))
    args = parser.parse_args()
    started = time.time()
    cache_dir = args.cache_dir.resolve()
    data_dir = args.data_dir.resolve()
    manifest = json.loads((cache_dir / "manifest.json").read_text())
    validate_cache_benchmark(manifest)
    work_dir = cache_dir / "full_history_work"
    if not work_dir.is_dir():
        raise FileNotFoundError("validated full-history work is required")
    sources = source_files(data_dir)
    for source in sources:
        if not source.is_file():
            raise FileNotFoundError(source)
    record_path = cache_dir / "item_history_manifest.json"
    previous = json.loads(record_path.read_text()) if record_path.is_file() else {}
    previous_splits = dict(previous.get("splits", {}))
    if args.split is not None:
        if args.split in previous_splits:
            raise FileExistsError(f"item-history split already exists: {args.split}")
        video_path = work_dir / previous.get("video_work_path", "video_source_id.npy")
        if not video_path.is_file():
            raise FileNotFoundError("validated item-history video work is absent")
        for name in ("item_daily_count.npy", "item_daily_positive.npy"):
            if not (work_dir / name).is_file():
                raise FileNotFoundError(f"validated item-history daily work is absent: {name}")
        reused = True
        daily = previous.get("daily")
        result = build_split(cache_dir, work_dir, args.split, SPLITS[args.split][1])
        previous_splits[args.split] = result
    else:
        video_path, reused = ensure_partitioned_video_ids(
            sources, work_dir, allow_reuse=args.reuse_video_work
        )
        daily = build_daily_video_totals(cache_dir, work_dir)
        duplicate = [name for name in SPLITS if name in previous_splits]
        if duplicate:
            raise FileExistsError(f"item-history splits already exist: {duplicate}")
        previous_splits.update({
            split: build_split(cache_dir, work_dir, split, bounds[1])
            for split, bounds in SPLITS.items()
        })
    record = {
        "format_version": 1,
        "base_cache_manifest_sha256": sha256(cache_dir / "manifest.json"),
        "causal_contract": (
            "Training rows use full-corpus sampled-video and author totals from "
            "earlier calendar days only; scoring rows freeze at the split cutoff."
        ),
        "feature_names": list(FEATURE_NAMES),
        "video_work_path": video_path.name,
        "video_work_reused": reused,
        "video_work_sha256": sha256(video_path),
        "daily": daily,
        "splits": previous_splits,
        "elapsed_seconds": time.time() - started,
        "max_rss_bytes": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
    }
    record_path.write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(record, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
