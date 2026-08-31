#!/usr/bin/env python3
"""Build a compact, label-safe development cache for KuaiRand-1K.

Only rows dated 2022-04-08 through 2022-04-28 are retained.  For later rows,
the parser reads the date needed to reject the row and never accesses the
``long_view`` field.  The resulting cache is an ignored local acceleration
artifact, not a competition deliverable.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import math
import os
import resource
import time
from pathlib import Path

import numpy as np


DEV_START = 20220408
DEV_END = 20220428
TRAIN_END = 20220421
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


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def count_rows(path: Path, *, retain_through: int | None) -> tuple[int, dict[int, int], int]:
    retained = 0
    skipped_after_dev = 0
    by_date: dict[int, int] = {}
    with path.open(newline="") as handle:
        reader = csv.reader(handle)
        header = tuple(next(reader))
        if header != EXPECTED_COLUMNS:
            raise ValueError(f"unexpected log schema in {path}: {header}")
        date_index = header.index("date")
        for row in reader:
            date = int(row[date_index])
            if retain_through is not None and date > retain_through:
                skipped_after_dev += 1
                continue
            if date < DEV_START:
                raise ValueError(f"unexpected pre-development date {date} in {path}")
            retained += 1
            by_date[date] = by_date.get(date, 0) + 1
    return retained, by_date, skipped_after_dev


def build_video_lookup(path: Path) -> tuple[dict[str, np.ndarray], dict[str, int]]:
    row_count = 0
    max_video = -1
    with path.open(newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        video_index = header.index("video_id")
        author_index = header.index("author_id")
        for row in reader:
            row_count += 1
            max_video = max(max_video, int(row[video_index]))
    video_id_space = max_video + 1
    raw_authors = np.full(video_id_space, -1, dtype=np.int64)
    primary_tag_by_video = np.full(video_id_space, -1, dtype=np.int32)
    secondary_tag_by_video = np.full(video_id_space, -1, dtype=np.int32)
    tertiary_tag_by_video = np.full(video_id_space, -1, dtype=np.int32)
    upload_type_by_video = np.full(video_id_space, -1, dtype=np.int16)
    video_type_by_video = np.full(video_id_space, -1, dtype=np.int16)
    music_type_by_video = np.full(video_id_space, -1, dtype=np.int16)
    visible_status_by_video = np.full(video_id_space, -1, dtype=np.int16)
    aspect_by_video = np.full(video_id_space, -1, dtype=np.int8)
    upload_ordinal_by_video = np.full(video_id_space, -1, dtype=np.int32)
    seen = np.zeros(video_id_space, dtype=np.bool_)
    upload_vocab: dict[str, int] = {}
    type_vocab: dict[str, int] = {}
    music_type_vocab: dict[str, int] = {}
    visible_vocab: dict[str, int] = {}
    with path.open(newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        video_index = header.index("video_id")
        author_index = header.index("author_id")
        tag_index = header.index("tag")
        upload_index = header.index("upload_type")
        type_index = header.index("video_type")
        music_type_index = header.index("music_type")
        visible_index = header.index("visible_status")
        width_index = header.index("server_width")
        height_index = header.index("server_height")
        upload_date_index = header.index("upload_dt")
        for row in reader:
            video = int(row[video_index])
            if seen[video]:
                raise ValueError(f"duplicate video id {video} in {path}")
            seen[video] = True
            raw_authors[video] = int(row[author_index])
            tag_tokens = [token.strip() for token in row[tag_index].split(",") if token.strip()]
            for target, position in (
                (primary_tag_by_video, 0),
                (secondary_tag_by_video, 1),
                (tertiary_tag_by_video, 2),
            ):
                if position < len(tag_tokens):
                    try:
                        target[video] = int(tag_tokens[position])
                    except ValueError:
                        target[video] = -1
            upload_value = row[upload_index] or "UNKNOWN"
            type_value = row[type_index] or "UNKNOWN"
            upload_type_by_video[video] = upload_vocab.setdefault(
                upload_value, len(upload_vocab)
            )
            video_type_by_video[video] = type_vocab.setdefault(
                type_value, len(type_vocab)
            )
            music_type_value = row[music_type_index] or "UNKNOWN"
            visible_value = row[visible_index] or "UNKNOWN"
            music_type_by_video[video] = music_type_vocab.setdefault(
                music_type_value, len(music_type_vocab)
            )
            visible_status_by_video[video] = visible_vocab.setdefault(
                visible_value, len(visible_vocab)
            )
            try:
                width = float(row[width_index])
                height = float(row[height_index])
                if not math.isfinite(width) or not math.isfinite(height) or height <= 0:
                    raise ValueError("invalid aspect ratio")
                ratio = width / height
                aspect_by_video[video] = 0 if ratio < 0.8 else 1 if ratio <= 1.2 else 2
            except (ValueError, ZeroDivisionError):
                aspect_by_video[video] = -1
            try:
                upload_ordinal_by_video[video] = dt.date.fromisoformat(
                    row[upload_date_index]
                ).toordinal()
            except ValueError:
                upload_ordinal_by_video[video] = -1
    unique_authors = np.unique(raw_authors[seen])
    author_by_video = np.full(video_id_space, -1, dtype=np.int32)
    author_by_video[seen] = np.searchsorted(unique_authors, raw_authors[seen]).astype(np.int32)
    missing_video_ids = int((~seen).sum())
    lookups = {
        "author": author_by_video,
        "tag": primary_tag_by_video,
        "tag2": secondary_tag_by_video,
        "tag3": tertiary_tag_by_video,
        "upload_type": upload_type_by_video,
        "video_type": video_type_by_video,
        "music_type": music_type_by_video,
        "visible_status": visible_status_by_video,
        "aspect": aspect_by_video,
        "upload_ordinal": upload_ordinal_by_video,
    }
    metadata = {
        "video_count": video_id_space,
        "video_feature_rows": row_count,
        "missing_video_ids": missing_video_ids,
        "author_count": int(len(unique_authors)),
        "tag_count": int(primary_tag_by_video.max()) + 1,
        "upload_type_count": len(upload_vocab),
        "video_type_count": len(type_vocab),
        "music_type_count": len(music_type_vocab),
        "visible_status_count": len(visible_vocab),
        "aspect_count": 3,
    }
    return lookups, metadata


def allocate(path: Path, dtype: str, count: int) -> np.memmap:
    return np.lib.format.open_memmap(path, mode="w+", dtype=dtype, shape=(count,))


def fill_log(
    path: Path,
    *,
    retain_through: int | None,
    start: int,
    arrays: dict[str, np.memmap],
    video_lookups: dict[str, np.ndarray],
) -> int:
    index = start
    with path.open(newline="") as handle:
        reader = csv.reader(handle)
        header = tuple(next(reader))
        if header != EXPECTED_COLUMNS:
            raise ValueError(f"unexpected log schema in {path}")
        positions = {name: header.index(name) for name in EXPECTED_COLUMNS}
        for row in reader:
            date = int(row[positions["date"]])
            if retain_through is not None and date > retain_through:
                # Do not access labels or feedback columns for held-out dates.
                continue
            if not DEV_START <= date <= DEV_END:
                raise ValueError(f"unexpected retained date {date} in {path}")
            video = int(row[positions["video_id"]])
            if not 0 <= video < len(video_lookups["author"]):
                raise ValueError(f"video id {video} has no basic feature row")
            arrays["user"][index] = int(row[positions["user_id"]])
            arrays["video"][index] = video
            arrays["author"][index] = video_lookups["author"][video]
            arrays["tag"][index] = video_lookups["tag"][video]
            arrays["tag2"][index] = video_lookups["tag2"][video]
            arrays["tag3"][index] = video_lookups["tag3"][video]
            arrays["upload_type"][index] = video_lookups["upload_type"][video]
            arrays["video_type"][index] = video_lookups["video_type"][video]
            arrays["music_type"][index] = video_lookups["music_type"][video]
            arrays["visible_status"][index] = video_lookups["visible_status"][video]
            arrays["aspect"][index] = video_lookups["aspect"][video]
            arrays["upload_ordinal"][index] = video_lookups["upload_ordinal"][video]
            arrays["tab"][index] = int(row[positions["tab"]])
            arrays["duration"][index] = float(row[positions["duration_ms"]])
            arrays["time_ms"][index] = int(row[positions["time_ms"]])
            arrays["is_click"][index] = int(row[positions["is_click"]])
            arrays["is_like"][index] = int(row[positions["is_like"]])
            arrays["is_follow"][index] = int(row[positions["is_follow"]])
            arrays["is_comment"][index] = int(row[positions["is_comment"]])
            arrays["is_forward"][index] = int(row[positions["is_forward"]])
            arrays["is_hate"][index] = int(row[positions["is_hate"]])
            arrays["date"][index] = date
            arrays["label"][index] = 0 if row[positions["long_view"]] == "0" else 1
            index += 1
    return index


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--cache-dir", type=Path, required=True)
    args = parser.parse_args()
    started = time.time()
    args.cache_dir.mkdir(parents=True, exist_ok=True)

    basic = args.data_dir / "video_features_basic_1k.csv"
    early = args.data_dir / "log_standard_4_08_to_4_21_1k.csv"
    later = args.data_dir / "log_standard_4_22_to_5_08_1k.csv"
    for source in (basic, early, later):
        if not source.is_file():
            raise FileNotFoundError(source)

    video_lookups, video_metadata = build_video_lookup(basic)
    early_count, early_dates, early_skipped = count_rows(early, retain_through=None)
    later_count, later_dates, later_skipped = count_rows(later, retain_through=DEV_END)
    if early_skipped:
        raise ValueError("early log unexpectedly contained rows beyond the development window")
    if not early_dates or max(early_dates) > TRAIN_END:
        raise ValueError(f"unexpected training dates: {sorted(early_dates)}")
    total = early_count + later_count

    arrays = {
        "user": allocate(args.cache_dir / "user.npy", "int32", total),
        "video": allocate(args.cache_dir / "video.npy", "int32", total),
        "author": allocate(args.cache_dir / "author.npy", "int32", total),
        "tag": allocate(args.cache_dir / "tag.npy", "int32", total),
        "tag2": allocate(args.cache_dir / "tag2.npy", "int32", total),
        "tag3": allocate(args.cache_dir / "tag3.npy", "int32", total),
        "upload_type": allocate(args.cache_dir / "upload_type.npy", "int16", total),
        "video_type": allocate(args.cache_dir / "video_type.npy", "int16", total),
        "music_type": allocate(args.cache_dir / "music_type.npy", "int16", total),
        "visible_status": allocate(args.cache_dir / "visible_status.npy", "int16", total),
        "aspect": allocate(args.cache_dir / "aspect.npy", "int8", total),
        "upload_ordinal": allocate(args.cache_dir / "upload_ordinal.npy", "int32", total),
        "tab": allocate(args.cache_dir / "tab.npy", "int16", total),
        "duration": allocate(args.cache_dir / "duration.npy", "float32", total),
        "time_ms": allocate(args.cache_dir / "time_ms.npy", "int64", total),
        "is_click": allocate(args.cache_dir / "is_click.npy", "uint8", total),
        "is_like": allocate(args.cache_dir / "is_like.npy", "uint8", total),
        "is_follow": allocate(args.cache_dir / "is_follow.npy", "uint8", total),
        "is_comment": allocate(args.cache_dir / "is_comment.npy", "uint8", total),
        "is_forward": allocate(args.cache_dir / "is_forward.npy", "uint8", total),
        "is_hate": allocate(args.cache_dir / "is_hate.npy", "uint8", total),
        "date": allocate(args.cache_dir / "date.npy", "int32", total),
        "label": allocate(args.cache_dir / "label.npy", "uint8", total),
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
        retain_through=DEV_END,
        start=next_index,
        arrays=arrays,
        video_lookups=video_lookups,
    )
    if next_index != total:
        raise RuntimeError(f"cache fill mismatch: {next_index} != {total}")
    for array in arrays.values():
        array.flush()

    dates = {**early_dates, **later_dates}
    manifest = {
        "format_version": 5,
        "created_at": __import__("datetime").datetime.now().astimezone().isoformat(),
        "source_data_dir": str(args.data_dir.resolve()),
        "source_archive_sha256": "dfaafbb5fd16e9e6d2f9a6adaa4ea25df20a14bc26a90961c136e26c00a7bb2c",
        "retained_date_range": [DEV_START, DEV_END],
        "test_label_policy": (
            "Rows after 20220428 are counted as skipped from the date column only; "
            "their labels and feedback fields are never accessed or retained."
        ),
        "rows": total,
        "train_rows": early_count,
        "post_train_dev_rows": later_count,
        "skipped_rows_after_20220428": later_skipped,
        "rows_by_date": {str(key): dates[key] for key in sorted(dates)},
        "video_count": video_metadata["video_count"],
        "video_feature_rows": video_metadata["video_feature_rows"],
        "missing_video_ids_in_reindexed_space": video_metadata["missing_video_ids"],
        "published_item_count": 4369953,
        "item_count_note": (
            "The checksum-verified 2025 archive differs from the project-page count; "
            "the cache uses the observed max-id space and maps missing metadata to unknown."
        ),
        "author_count": video_metadata["author_count"],
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
    }
    (args.cache_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
