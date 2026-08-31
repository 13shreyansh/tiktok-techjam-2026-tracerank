#!/usr/bin/env python3
"""Create deterministic, label-safe development samples from KuaiRand-27K."""

from __future__ import annotations

import argparse
import csv
import json
import os
import resource
import time
from pathlib import Path


DEV_START = 20220408
TRAIN_END = 20220421
DEV_END = 20220428
EXPECTED_COLUMNS = (
    "user_id",
    "video_id",
    "date",
    "hourmin",
    "time_ms",
    "is_click",
    "is_like",
    "is_follow",
    "is_comment",
    "is_forward",
    "is_hate",
    "long_view",
    "play_time_ms",
    "duration_ms",
    "profile_stay_time",
    "comment_stay_time",
    "is_profile_enter",
    "is_rand",
    "tab",
)


def event_hash(user_id: int, video_id: int, time_ms: int) -> int:
    """Stable 64-bit SplitMix-style hash for deterministic row sampling."""

    mask = (1 << 64) - 1
    value = (
        (user_id * 0x9E3779B97F4A7C15)
        ^ (video_id * 0xBF58476D1CE4E5B9)
        ^ time_ms
    ) & mask
    value = ((value ^ (value >> 30)) * 0xBF58476D1CE4E5B9) & mask
    value = ((value ^ (value >> 27)) * 0x94D049BB133111EB) & mask
    return (value ^ (value >> 31)) & mask


def event_hash_array(
    user_id: "np.ndarray", video_id: "np.ndarray", time_ms: "np.ndarray"
) -> "np.ndarray":
    """Vectorized uint64 equivalent of :func:`event_hash`."""
    import numpy as np

    user = np.asarray(user_id, dtype=np.uint64)
    video = np.asarray(video_id, dtype=np.uint64)
    timestamp = np.asarray(time_ms, dtype=np.uint64)
    value = (
        user * np.uint64(0x9E3779B97F4A7C15)
        ^ video * np.uint64(0xBF58476D1CE4E5B9)
        ^ timestamp
    )
    value = (value ^ (value >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9)
    value = (value ^ (value >> np.uint64(27))) * np.uint64(0x94D049BB133111EB)
    return value ^ (value >> np.uint64(31))


def keep_event(
    user_id: int,
    video_id: int,
    time_ms: int,
    modulus: int,
    residue: int,
) -> bool:
    return event_hash(user_id, video_id, time_ms) % modulus == residue


def sample_group(
    sources: list[Path],
    destination: Path,
    *,
    modulus: int,
    residue: int,
    minimum_date: int,
    maximum_date: int,
    allow_after_boundary: bool,
) -> dict[str, object]:
    partial = destination.with_suffix(destination.suffix + ".part")
    if destination.exists() or partial.exists():
        raise FileExistsError(f"refusing to overwrite {destination} or {partial}")

    retained = 0
    sampled = 0
    skipped_after_boundary = 0
    dates: dict[int, dict[str, int]] = {}
    with partial.open("w", encoding="utf-8", newline="") as output:
        writer = csv.writer(output)
        writer.writerow(EXPECTED_COLUMNS)
        for source in sources:
            with source.open("r", encoding="utf-8", newline="") as handle:
                reader = csv.reader(handle)
                header = tuple(next(reader))
                if header != EXPECTED_COLUMNS:
                    raise ValueError(f"unexpected log schema in {source}: {header}")
                positions = {name: header.index(name) for name in EXPECTED_COLUMNS}
                for row in reader:
                    date = int(row[positions["date"]])
                    if date > maximum_date:
                        if not allow_after_boundary:
                            raise ValueError(f"unexpected date {date} in {source}")
                        # Do not interpret outcome or feedback fields beyond DEV_END.
                        skipped_after_boundary += 1
                        continue
                    if date < minimum_date:
                        raise ValueError(f"unexpected date {date} in {source}")
                    retained += 1
                    date_counts = dates.setdefault(date, {"eligible": 0, "sampled": 0})
                    date_counts["eligible"] += 1
                    user_id = int(row[positions["user_id"]])
                    video_id = int(row[positions["video_id"]])
                    time_ms = int(row[positions["time_ms"]])
                    if keep_event(user_id, video_id, time_ms, modulus, residue):
                        writer.writerow(row)
                        sampled += 1
                        date_counts["sampled"] += 1
        output.flush()
        os.fsync(output.fileno())
    partial.replace(destination)
    return {
        "destination": str(destination),
        "bytes": destination.stat().st_size,
        "eligible_rows": retained,
        "sampled_rows": sampled,
        "skipped_after_boundary": skipped_after_boundary,
        "dates": {str(date): dates[date] for date in sorted(dates)},
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--modulus", type=int, default=32)
    parser.add_argument("--residue", type=int, default=0)
    args = parser.parse_args()
    if args.modulus < 1:
        raise ValueError("--modulus must be positive")
    if not 0 <= args.residue < args.modulus:
        raise ValueError("--residue must be in [0, modulus)")

    data_dir = args.data_dir.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "sample_manifest.json"
    if manifest_path.exists():
        raise FileExistsError(f"refusing to overwrite {manifest_path}")

    early_sources = [
        data_dir / "log_standard_4_08_to_4_21_27k_part1.csv",
        data_dir / "log_standard_4_08_to_4_21_27k_part2.csv",
    ]
    later_sources = [
        data_dir / "log_standard_4_22_to_5_08_27k_part1.csv",
        data_dir / "log_standard_4_22_to_5_08_27k_part2.csv",
    ]
    for source in early_sources + later_sources:
        if not source.is_file():
            raise FileNotFoundError(source)

    started = time.time()
    early = sample_group(
        early_sources,
        output_dir / "log_standard_4_08_to_4_21_27k_sample.csv",
        modulus=args.modulus,
        residue=args.residue,
        minimum_date=DEV_START,
        maximum_date=TRAIN_END,
        allow_after_boundary=False,
    )
    later = sample_group(
        later_sources,
        output_dir / "log_standard_4_22_to_4_28_27k_sample.csv",
        modulus=args.modulus,
        residue=args.residue,
        minimum_date=TRAIN_END + 1,
        maximum_date=DEV_END,
        allow_after_boundary=True,
    )
    manifest = {
        "format_version": 1,
        "source_data_dir": str(data_dir),
        "sampling": {
            "algorithm": "splitmix64(user_id, video_id, time_ms) modulo",
            "modulus": args.modulus,
            "residue": args.residue,
        },
        "retained_date_range": [DEV_START, DEV_END],
        "test_label_policy": (
            "For rows after 20220428, only date is interpreted before rejection; "
            "outcome and feedback values are never used or retained."
        ),
        "early": early,
        "later": later,
        "elapsed_seconds": time.time() - started,
        "max_rss_bytes": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
