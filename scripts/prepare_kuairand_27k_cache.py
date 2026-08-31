#!/usr/bin/env python3
"""Build a compact local cache from a declared KuaiRand-27K row sample."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import resource
import time
from pathlib import Path

import numpy as np

from prepare_kuairand_1k_cache import (
    DEV_END,
    DEV_START,
    TRAIN_END,
    allocate,
    build_video_lookup,
    count_rows,
    fill_log,
    sha256,
)
from sample_kuairand_27k_logs import event_hash_array


EXPECTED_ARCHIVE_BYTES = 9_892_191_178
EXPECTED_ARCHIVE_MD5 = "3e3c799a24e2d23a4d2c757fbf9adf59"
BENCHMARK_NAMES = (
    "KuaiRand-27K deterministic development sample",
    "KuaiRand-27K expanded-training deterministic development sample",
    "KuaiRand-27K quarter-training deterministic development sample",
    "KuaiRand-27K half-training deterministic development sample",
    "KuaiRand-27K full-training deterministic development sample",
)


def md5(path: Path) -> str:
    digest = hashlib.md5()  # noqa: S324 - required upstream integrity checksum
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_archive(path: Path) -> dict[str, object]:
    observed_bytes = path.stat().st_size
    if observed_bytes != EXPECTED_ARCHIVE_BYTES:
        raise ValueError(
            f"27K archive byte mismatch: {observed_bytes} != {EXPECTED_ARCHIVE_BYTES}"
        )
    observed_md5 = md5(path)
    if observed_md5 != EXPECTED_ARCHIVE_MD5:
        raise ValueError(
            f"27K archive MD5 mismatch: {observed_md5} != {EXPECTED_ARCHIVE_MD5}"
        )
    return {"bytes": observed_bytes, "md5": observed_md5}


def remap_observed_ids(
    array: np.memmap,
    mapping_path: Path,
    *,
    allow_missing: bool,
) -> int:
    """Remap only IDs present in the sample and preserve the sorted source IDs."""

    values = np.asarray(array)
    valid = values >= 0
    if not allow_missing and not bool(np.all(valid)):
        raise ValueError(f"unexpected missing ID while creating {mapping_path}")
    source_ids, inverse = np.unique(values[valid], return_inverse=True)
    array[valid] = inverse.astype(array.dtype, copy=False)
    if allow_missing:
        array[~valid] = -1
    array.flush()
    np.save(mapping_path, source_ids.astype(np.int32, copy=False))
    return int(len(source_ids))


def write_evaluation_remainders(
    cache_dir: Path,
    users: np.ndarray,
    remapped_videos: np.ndarray,
    times: np.ndarray,
    *,
    modulus: int,
) -> Path:
    """Persist deterministic hash remainders for a stricter evaluation subset."""
    if not 1 <= modulus <= 256:
        raise ValueError("evaluation modulus must be in [1, 256]")
    source_video_ids = np.load(cache_dir / "source_video_ids.npy", mmap_mode="r")
    output_path = cache_dir / "evaluation_remainder.npy"
    output = np.lib.format.open_memmap(
        output_path, mode="w+", dtype="uint8", shape=(len(users),)
    )
    chunk = 1_000_000
    for start in range(0, len(users), chunk):
        end = min(start + chunk, len(users))
        source_videos = source_video_ids[
            np.asarray(remapped_videos[start:end], dtype=np.int64)
        ]
        output[start:end] = (
            event_hash_array(
                np.asarray(users[start:end], dtype=np.uint64),
                source_videos,
                np.asarray(times[start:end], dtype=np.uint64),
            )
            % np.uint64(modulus)
        ).astype(np.uint8)
    output.flush()
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--sample-dir", type=Path, required=True)
    parser.add_argument("--cache-dir", type=Path, required=True)
    parser.add_argument("--evaluation-modulus", type=int)
    parser.add_argument("--evaluation-residue", type=int, default=0)
    parser.add_argument(
        "--benchmark-name",
        choices=BENCHMARK_NAMES,
        default="KuaiRand-27K deterministic development sample",
    )
    args = parser.parse_args()
    started = time.time()

    archive = args.archive.resolve()
    data_dir = args.data_dir.resolve()
    sample_dir = args.sample_dir.resolve()
    cache_dir = args.cache_dir.resolve()
    cache_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = cache_dir / "manifest.json"
    if manifest_path.exists():
        raise FileExistsError(f"refusing to overwrite {manifest_path}")

    archive_evidence = validate_archive(archive)
    basic = data_dir / "video_features_basic_27k.csv"
    early = sample_dir / "log_standard_4_08_to_4_21_27k_sample.csv"
    later = sample_dir / "log_standard_4_22_to_4_28_27k_sample.csv"
    sample_manifest_path = sample_dir / "sample_manifest.json"
    for source in (basic, early, later, sample_manifest_path):
        if not source.is_file():
            raise FileNotFoundError(source)

    sample_manifest = json.loads(sample_manifest_path.read_text())
    if sample_manifest.get("retained_date_range") != [DEV_START, DEV_END]:
        raise ValueError("sample manifest does not have the locked development range")

    video_lookups, video_metadata = build_video_lookup(basic)
    early_count, early_dates, early_skipped = count_rows(early, retain_through=None)
    later_count, later_dates, later_skipped = count_rows(later, retain_through=None)
    if early_skipped or later_skipped:
        raise ValueError("sample unexpectedly contains skipped post-boundary rows")
    if not early_dates or not later_dates:
        raise ValueError("sample has an empty train or validation partition")
    if min(early_dates) < DEV_START or max(early_dates) > TRAIN_END:
        raise ValueError(f"unexpected early dates: {sorted(early_dates)}")
    if min(later_dates) <= TRAIN_END or max(later_dates) > DEV_END:
        raise ValueError(f"unexpected later dates: {sorted(later_dates)}")
    total = early_count + later_count

    arrays = {
        "user": allocate(cache_dir / "user.npy", "int32", total),
        "video": allocate(cache_dir / "video.npy", "int32", total),
        "author": allocate(cache_dir / "author.npy", "int32", total),
        "tag": allocate(cache_dir / "tag.npy", "int32", total),
        "tag2": allocate(cache_dir / "tag2.npy", "int32", total),
        "tag3": allocate(cache_dir / "tag3.npy", "int32", total),
        "upload_type": allocate(cache_dir / "upload_type.npy", "int16", total),
        "video_type": allocate(cache_dir / "video_type.npy", "int16", total),
        "music_type": allocate(cache_dir / "music_type.npy", "int16", total),
        "visible_status": allocate(cache_dir / "visible_status.npy", "int16", total),
        "aspect": allocate(cache_dir / "aspect.npy", "int8", total),
        "upload_ordinal": allocate(cache_dir / "upload_ordinal.npy", "int32", total),
        "tab": allocate(cache_dir / "tab.npy", "int16", total),
        "duration": allocate(cache_dir / "duration.npy", "float32", total),
        "time_ms": allocate(cache_dir / "time_ms.npy", "int64", total),
        "is_click": allocate(cache_dir / "is_click.npy", "uint8", total),
        "is_like": allocate(cache_dir / "is_like.npy", "uint8", total),
        "is_follow": allocate(cache_dir / "is_follow.npy", "uint8", total),
        "is_comment": allocate(cache_dir / "is_comment.npy", "uint8", total),
        "is_forward": allocate(cache_dir / "is_forward.npy", "uint8", total),
        "is_hate": allocate(cache_dir / "is_hate.npy", "uint8", total),
        "date": allocate(cache_dir / "date.npy", "int32", total),
        "label": allocate(cache_dir / "label.npy", "uint8", total),
    }
    next_index = fill_log(
        early,
        retain_through=None,
        start=0,
        arrays=arrays,
        video_lookups=video_lookups,
    )
    next_index = fill_log(
        later,
        retain_through=None,
        start=next_index,
        arrays=arrays,
        video_lookups=video_lookups,
    )
    if next_index != total:
        raise RuntimeError(f"cache fill mismatch: {next_index} != {total}")
    for array in arrays.values():
        array.flush()

    source_video_id_space = video_metadata["video_count"]
    source_author_id_space = video_metadata["author_count"]
    sampled_video_count = remap_observed_ids(
        arrays["video"], cache_dir / "source_video_ids.npy", allow_missing=False
    )
    sampled_author_count = remap_observed_ids(
        arrays["author"], cache_dir / "source_author_ids.npy", allow_missing=True
    )
    evaluation_path = None
    if args.evaluation_modulus is not None:
        if not 0 <= args.evaluation_residue < args.evaluation_modulus:
            raise ValueError("evaluation residue must be in [0, evaluation modulus)")
        evaluation_path = write_evaluation_remainders(
            cache_dir,
            arrays["user"],
            arrays["video"],
            arrays["time_ms"],
            modulus=args.evaluation_modulus,
        )

    dates = {**early_dates, **later_dates}
    manifest = {
        "format_version": 1,
        "benchmark": args.benchmark_name,
        "created_at": __import__("datetime").datetime.now().astimezone().isoformat(),
        "source_data_dir": str(data_dir),
        "source_archive": archive_evidence,
        "source_sample_manifest_sha256": sha256(sample_manifest_path),
        "sampling": sample_manifest["sampling"],
        "evaluation_sampling": (
            {
                "algorithm": "splitmix64(user_id, video_id, time_ms) modulo",
                "modulus": args.evaluation_modulus,
                "residue": args.evaluation_residue,
                "path": evaluation_path.name,
                "sha256": sha256(evaluation_path),
            }
            if evaluation_path is not None
            else None
        ),
        "retained_date_range": [DEV_START, DEV_END],
        "test_label_policy": sample_manifest["test_label_policy"],
        "rows": total,
        "train_rows": early_count,
        "post_train_dev_rows": later_count,
        "rows_by_date": {str(key): dates[key] for key in sorted(dates)},
        "video_count": sampled_video_count,
        "source_video_id_space": source_video_id_space,
        "video_feature_rows": video_metadata["video_feature_rows"],
        "missing_video_ids_in_reindexed_space": video_metadata["missing_video_ids"],
        "published_item_count": 32_038_725,
        "author_count": sampled_author_count,
        "source_author_id_space": source_author_id_space,
        "tag_count": video_metadata["tag_count"],
        "upload_type_count": video_metadata["upload_type_count"],
        "video_type_count": video_metadata["video_type_count"],
        "music_type_count": video_metadata["music_type_count"],
        "visible_status_count": video_metadata["visible_status_count"],
        "aspect_count": video_metadata["aspect_count"],
        "user_count": int(np.max(arrays["user"])) + 1,
        "tab_count": int(np.max(arrays["tab"])) + 1,
        "long_view_rate_dev": float(np.mean(arrays["label"])),
        "source_sha256": {
            basic.name: sha256(basic),
            early.name: sha256(early),
            later.name: sha256(later),
        },
        "elapsed_seconds": time.time() - started,
        "max_rss_bytes": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
        "pid": os.getpid(),
        "score_scope_warning": (
            "Metrics from this cache describe a deterministic development sample, "
            "not the full 27K benchmark or hidden test."
        ),
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
