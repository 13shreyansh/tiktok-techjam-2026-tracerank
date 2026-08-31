#!/usr/bin/env python3
"""Build sampled-row features from every earlier KuaiRand-27K dev event.

The scored rows remain the fixed deterministic 1/32 sample. User-level history
state, however, is updated from every official event through each split's
training cutoff. Rows at one user/timestamp are emitted before the entire batch
updates state. Events after 2022-04-28 are rejected before outcome fields are
interpreted.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import resource
import time
from pathlib import Path

import numpy as np

try:
    from scripts.prepare_kuairand_1k_history import SPLITS, log_bucket, rate_bucket, sha256
    from scripts.sample_kuairand_27k_logs import DEV_END, EXPECTED_COLUMNS, keep_event
except ModuleNotFoundError:  # Direct ``python scripts/...`` execution.
    from prepare_kuairand_1k_history import SPLITS, log_bucket, rate_bucket, sha256
    from sample_kuairand_27k_logs import DEV_END, EXPECTED_COLUMNS, keep_event


def allocate(path: Path, dtype: str, length: int, fill: int = 0) -> np.memmap:
    array = np.lib.format.open_memmap(path, mode="w+", dtype=dtype, shape=(length,))
    if fill:
        array[:] = fill
    return array


def source_files(data_dir: Path) -> list[Path]:
    return [
        data_dir / "log_standard_4_08_to_4_21_27k_part1.csv",
        data_dir / "log_standard_4_08_to_4_21_27k_part2.csv",
        data_dir / "log_standard_4_22_to_5_08_27k_part1.csv",
        data_dir / "log_standard_4_22_to_5_08_27k_part2.csv",
    ]


def checked_reader(path: Path):
    handle = path.open("r", encoding="utf-8", newline="")
    reader = csv.reader(handle)
    header = tuple(next(reader))
    if header != EXPECTED_COLUMNS:
        handle.close()
        raise ValueError(f"unexpected log schema in {path}: {header}")
    return handle, reader, {name: header.index(name) for name in header}


def count_by_user(sources: list[Path], user_count: int) -> tuple[np.ndarray, int, int]:
    counts = np.zeros(user_count, dtype=np.int64)
    retained = skipped = 0
    for source in sources:
        handle, reader, pos = checked_reader(source)
        with handle:
            for row in reader:
                date = int(row[pos["date"]])
                if date > DEV_END:
                    skipped += 1
                    continue
                user = int(row[pos["user_id"]])
                if not 0 <= user < user_count:
                    raise ValueError(f"user {user} outside declared range")
                counts[user] += 1
                retained += 1
    return counts, retained, skipped


def fill_partitioned_events(
    sources: list[Path],
    work_dir: Path,
    cache_dir: Path,
    counts: np.ndarray,
    modulus: int,
    residue: int,
) -> dict[str, object]:
    offsets = np.r_[0, np.cumsum(counts, dtype=np.int64)]
    total = int(offsets[-1])
    cursor = offsets[:-1].copy()
    arrays = {
        "time_ms": allocate(work_dir / "time_ms.npy", "int64", total),
        "date": allocate(work_dir / "date.npy", "int32", total),
        "sample_index": allocate(work_dir / "sample_index.npy", "int32", total, -1),
        "label": allocate(work_dir / "label.npy", "uint8", total),
        "strong": allocate(work_dir / "strong.npy", "uint8", total),
        "hate": allocate(work_dir / "hate.npy", "uint8", total),
    }
    cache_user = np.load(cache_dir / "user.npy", mmap_mode="r")
    cache_video = np.load(cache_dir / "video.npy", mmap_mode="r")
    cache_time = np.load(cache_dir / "time_ms.npy", mmap_mode="r")
    source_video_ids = np.load(cache_dir / "source_video_ids.npy", mmap_mode="r")
    sample_rows = len(cache_user)
    next_sample = 0
    simultaneous_source_rows = 0

    for source in sources:
        handle, reader, pos = checked_reader(source)
        with handle:
            for row in reader:
                date = int(row[pos["date"]])
                if date > DEV_END:
                    continue
                user = int(row[pos["user_id"]])
                video = int(row[pos["video_id"]])
                event_time = int(row[pos["time_ms"]])
                index = int(cursor[user])
                cursor[user] += 1
                arrays["time_ms"][index] = event_time
                arrays["date"][index] = date
                arrays["label"][index] = int(row[pos["long_view"]])
                arrays["strong"][index] = (
                    int(row[pos["is_like"]])
                    | int(row[pos["is_follow"]])
                    | int(row[pos["is_comment"]])
                    | int(row[pos["is_forward"]])
                )
                arrays["hate"][index] = int(row[pos["is_hate"]])
                if keep_event(user, video, event_time, modulus, residue):
                    if next_sample >= sample_rows:
                        raise ValueError("full-log sampler produced too many sampled rows")
                    expected_video = int(source_video_ids[int(cache_video[next_sample])])
                    if (
                        int(cache_user[next_sample]) != user
                        or int(cache_time[next_sample]) != event_time
                        or expected_video != video
                    ):
                        raise ValueError(
                            f"sample/cache order mismatch at sampled row {next_sample}"
                        )
                    arrays["sample_index"][index] = next_sample
                    next_sample += 1

    if not np.array_equal(cursor, offsets[1:]):
        raise RuntimeError("user-partition fill counts do not match first pass")
    if next_sample != sample_rows:
        raise RuntimeError(f"sample/cache row mismatch: {next_sample} != {sample_rows}")
    for array in arrays.values():
        array.flush()
    np.save(work_dir / "user_offsets.npy", offsets)
    return {
        "retained_events": total,
        "sample_rows_matched": next_sample,
        "working_bytes": int(sum(array.nbytes for array in arrays.values()) + offsets.nbytes),
        "simultaneous_source_rows": simultaneous_source_rows,
    }


def validate_work_partition(work_dir: Path, sample_rows: int) -> dict[str, object]:
    required = {
        "time_ms": "int64", "date": "int32", "sample_index": "int32",
        "label": "uint8", "strong": "uint8", "hate": "uint8",
    }
    offsets = np.load(work_dir / "user_offsets.npy", mmap_mode="r")
    if np.any(offsets[1:] < offsets[:-1]):
        raise ValueError("full-history work offsets are not monotonic")
    retained = int(offsets[-1])
    working_bytes = int(offsets.nbytes)
    for name, dtype in required.items():
        array = np.load(work_dir / f"{name}.npy", mmap_mode="r")
        if len(array) != retained or str(array.dtype) != dtype:
            raise ValueError(f"invalid reusable work array {name}: {array.shape} {array.dtype}")
        working_bytes += int(array.nbytes)
    sampled = np.load(work_dir / "sample_index.npy", mmap_mode="r")
    observed = np.asarray(sampled[sampled >= 0], dtype=np.int64)
    if len(observed) != sample_rows or not np.array_equal(
        np.sort(observed), np.arange(sample_rows, dtype=np.int64)
    ):
        raise ValueError("reusable work partition does not map every sampled row exactly once")
    return {
        "retained_events": retained,
        "sample_rows_matched": sample_rows,
        "working_bytes": working_bytes,
        "validated_reuse": True,
    }


def build_split(cache_dir: Path, work_dir: Path, split: str, cutoff: int) -> dict[str, object]:
    offsets = np.load(work_dir / "user_offsets.npy", mmap_mode="r")
    times = np.load(work_dir / "time_ms.npy", mmap_mode="r")
    dates = np.load(work_dir / "date.npy", mmap_mode="r")
    sample_indices = np.load(work_dir / "sample_index.npy", mmap_mode="r")
    labels = np.load(work_dir / "label.npy", mmap_mode="r")
    strong = np.load(work_dir / "strong.npy", mmap_mode="r")
    hates = np.load(work_dir / "hate.npy", mmap_mode="r")
    sample_history = np.load(cache_dir / f"history_{split}.npy", mmap_mode="r")
    output_path = cache_dir / f"full_history_{split}.npy"
    output = np.lib.format.open_memmap(
        output_path, mode="w+", dtype="int16", shape=sample_history.shape
    )
    output[:] = sample_history
    sampled_written = 0
    simultaneous_batches = 0
    for user in range(len(offsets) - 1):
        start, end = int(offsets[user]), int(offsets[user + 1])
        if start == end:
            continue
        order = np.argsort(np.asarray(times[start:end]), kind="stable") + start
        user_times = np.asarray(times[order], dtype=np.int64)
        count = positive = strong_count = hate_count = 0
        position = 0
        while position < len(order):
            batch_end = position + 1
            while batch_end < len(order) and user_times[batch_end] == user_times[position]:
                batch_end += 1
            batch = order[position:batch_end]
            sampled = np.asarray(sample_indices[batch], dtype=np.int64)
            sampled = sampled[sampled >= 0]
            if len(sampled):
                output[sampled, 0] = log_bucket(count, 15)
                output[sampled, 1] = int(rate_bucket(positive, count))
                output[sampled, 2] = log_bucket(strong_count, 10)
                output[sampled, 3] = log_bucket(hate_count, 10)
                sampled_written += len(sampled)
            batch_dates = np.asarray(dates[batch], dtype=np.int32)
            # Identical epoch timestamps occasionally have adjacent local-date
            # labels. Preserve the simultaneous batch, but allow only rows on
            # the training side of the declared date cutoff to update state.
            eligible = batch[batch_dates <= cutoff]
            if len(eligible):
                count += len(eligible)
                positive += int(np.asarray(labels[eligible], dtype=np.uint8).sum())
                strong_count += int(np.asarray(strong[eligible], dtype=np.uint8).sum())
                hate_count += int(np.asarray(hates[eligible], dtype=np.uint8).sum())
            simultaneous_batches += int(len(batch) > 1)
            position = batch_end
    if sampled_written != sample_history.shape[0]:
        raise RuntimeError(
            f"full-history feature rows mismatch: {sampled_written} != {sample_history.shape[0]}"
        )
    output.flush()
    return {
        "split": split,
        "train_bounds": list(SPLITS[split]),
        "path": output_path.name,
        "bytes": output_path.stat().st_size,
        "sha256": sha256(output_path),
        "sample_rows": sampled_written,
        "simultaneous_full_history_batches": simultaneous_batches,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--cache-dir", type=Path, required=True)
    parser.add_argument("--reuse-complete-work", action="store_true")
    args = parser.parse_args()
    started = time.time()
    data_dir = args.data_dir.resolve()
    cache_dir = args.cache_dir.resolve()
    manifest_path = cache_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    if manifest.get("benchmark") != "KuaiRand-27K deterministic development sample":
        raise ValueError("full history requires the verified 27K sampled cache")
    sampling = manifest.get("sampling", {})
    modulus, residue = int(sampling["modulus"]), int(sampling["residue"])
    sources = source_files(data_dir)
    for source in sources:
        if not source.is_file():
            raise FileNotFoundError(source)
    for split in SPLITS:
        if not (cache_dir / f"history_{split}.npy").is_file():
            raise FileNotFoundError(f"sample history missing for {split}")

    work_dir = cache_dir / "full_history_work"
    if args.reuse_complete_work:
        if not work_dir.is_dir():
            raise FileNotFoundError("requested reusable full-history work is absent")
        fill = validate_work_partition(work_dir, int(manifest["rows"]))
        retained = int(fill["retained_events"])
        skipped = None
    else:
        work_dir.mkdir(exist_ok=False)
        counts, retained, skipped = count_by_user(sources, int(manifest["user_count"]))
        fill = fill_partitioned_events(
            sources, work_dir, cache_dir, counts, modulus, residue
        )
        if fill["retained_events"] != retained:
            raise RuntimeError("retained-event count changed between passes")
    results = [
        build_split(cache_dir, work_dir, name, bounds[1])
        for name, bounds in SPLITS.items()
    ]
    record = {
        "format_version": 1,
        "feature_names": [
            "full_prior_user_count_log2",
            "full_prior_user_long_view_rate_21",
            "full_prior_user_strong_feedback_count_log2",
            "full_prior_user_hate_count_log2",
            "sample_prior_user_tag_count_log2",
            "sample_prior_user_tag_long_view_rate_21",
            "sample_current_tag_matches_last_positive_tag",
            "sample_last_positive_tag",
        ],
        "causal_contract": (
            "User-level fields use all official events at earlier timestamps through the "
            "training cutoff; same-timestamp rows update after the batch. Tag-level fields "
            "remain from the fixed sample. Outcomes after 2022-04-28 are never interpreted."
        ),
        "base_cache_manifest_sha256": sha256(manifest_path),
        "source_files": [
            {"name": path.name, "bytes": path.stat().st_size} for path in sources
        ],
        "retained_events": retained,
        "skipped_post_boundary_rows": skipped,
        "working_set": fill,
        "splits": {entry["split"]: entry for entry in results},
        "elapsed_seconds": time.time() - started,
        "max_rss_bytes": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    (cache_dir / "full_history_manifest.json").write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(record, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
