#!/usr/bin/env python3
"""Create and label-blindly check a KuaiRand-1K post-April-28 CSV.

The source CSV physically contains outcome columns, but this script resolves
and accesses only date, user, video, tab, and duration positions. It never
indexes, evaluates, aggregates, or exports any post-April-28 outcome field.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import resource
import sys
import time
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.prepare_kuairand_1k_cache import build_video_lookup, sha256
from solution.kuairand_1k_ranker import SparseFM


HEADER = ["row_id", "user_id", "video_id", "score"]
TEST_START = 20220429
TEST_END = 20220508


def load_model(checkpoint_path: Path) -> tuple[SparseFM, dict]:
    checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
    if checkpoint.get("feature_set") != "content":
        raise ValueError("the frozen 1K candidate must use feature_set=content")
    latent = checkpoint["latent"]
    linear = checkpoint["linear"]
    if latent.ndim != 2 or linear.shape != (latent.shape[0], 1):
        raise ValueError("checkpoint embedding shapes are inconsistent")
    model = SparseFM(
        int(latent.shape[0]),
        int(latent.shape[1]),
        np.asarray(checkpoint["offsets"], dtype=np.int64),
        int(checkpoint["seed"]),
    )
    with torch.no_grad():
        model.latent.weight.copy_(latent)
        model.linear.weight.copy_(linear)
    model.eval()
    return model, checkpoint


def encode_content(
    checkpoint: dict,
    lookups: dict[str, np.ndarray],
    users: np.ndarray,
    videos: np.ndarray,
    tabs: np.ndarray,
    durations: np.ndarray,
) -> np.ndarray:
    offsets = np.asarray(checkpoint["offsets"], dtype=np.int64)
    if len(offsets) != 8:
        raise ValueError(f"content checkpoint must have 8 fields, found {len(offsets)}")
    if np.any(videos < 0) or np.any(videos >= len(lookups["author"])):
        raise ValueError("test row contains a video outside the official basic table ID space")
    authors = lookups["author"][videos].astype(np.int64)
    tags = lookups["tag"][videos].astype(np.int64)
    upload_types = lookups["upload_type"][videos].astype(np.int64)
    video_types = lookups["video_type"][videos].astype(np.int64)
    output = np.empty((len(users), 8), dtype=np.int64)
    seen_user = np.asarray(checkpoint["seen_user"], dtype=np.bool_)
    seen_video = np.asarray(checkpoint["seen_video"], dtype=np.bool_)
    seen_author = np.asarray(checkpoint["seen_author"], dtype=np.bool_)
    output[:, 0] = np.where(seen_user[users], users + 1, 0) + offsets[0]
    output[:, 1] = np.where(seen_video[videos], videos + 1, 0) + offsets[1]
    author_seen = authors >= 0
    author_seen[author_seen] &= seen_author[authors[author_seen]]
    output[:, 2] = np.where(author_seen, authors + 1, 0) + offsets[2]
    output[:, 3] = tabs + 1 + offsets[3]
    output[:, 4] = (
        np.searchsorted(np.asarray(checkpoint["duration_edges"]), durations) + 1 + offsets[4]
    )
    for column, values, seen_name in (
        (5, tags, "seen_tag"),
        (6, upload_types, "seen_upload_type"),
        (7, video_types, "seen_video_type"),
    ):
        seen = np.asarray(checkpoint[seen_name], dtype=np.bool_)
        value_seen = values >= 0
        value_seen[value_seen] &= seen[values[value_seen]]
        output[:, column] = np.where(value_seen, values + 1, 0) + offsets[column]
    return output


def iter_test_chunks(log_path: Path, chunk_size: int):
    with log_path.open(newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        positions = {
            name: header.index(name)
            for name in ("user_id", "video_id", "date", "tab", "duration_ms")
        }
        users: list[int] = []
        videos: list[int] = []
        tabs: list[int] = []
        durations: list[float] = []
        for row in reader:
            date = int(row[positions["date"]])
            if date < TEST_START:
                continue
            if date > TEST_END:
                raise ValueError(f"unexpected row after fixed test end: {date}")
            # No outcome-column position is resolved or indexed here.
            users.append(int(row[positions["user_id"]]))
            videos.append(int(row[positions["video_id"]]))
            tabs.append(int(row[positions["tab"]]))
            durations.append(float(row[positions["duration_ms"]]))
            if len(users) == chunk_size:
                yield (
                    np.asarray(users, dtype=np.int64),
                    np.asarray(videos, dtype=np.int64),
                    np.asarray(tabs, dtype=np.int64),
                    np.asarray(durations, dtype=np.float32),
                )
                users.clear(); videos.clear(); tabs.clear(); durations.clear()
        if users:
            yield (
                np.asarray(users, dtype=np.int64),
                np.asarray(videos, dtype=np.int64),
                np.asarray(tabs, dtype=np.int64),
                np.asarray(durations, dtype=np.float32),
            )


def write_candidate(
    data_dir: Path,
    checkpoint_path: Path,
    output_path: Path,
    chunk_size: int,
) -> dict:
    if output_path.exists():
        raise FileExistsError(f"refusing to overwrite existing candidate: {output_path}")
    basic = data_dir / "video_features_basic_1k.csv"
    log_path = data_dir / "log_standard_4_22_to_5_08_1k.csv"
    lookups, metadata = build_video_lookup(basic)
    model, checkpoint = load_model(checkpoint_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    row_id = 0
    with output_path.open("x", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(HEADER)
        with torch.no_grad():
            for users, videos, tabs, durations in iter_test_chunks(log_path, chunk_size):
                fields = encode_content(
                    checkpoint, lookups, users, videos, tabs, durations
                )
                scores = model(torch.from_numpy(fields)).numpy()
                if not np.all(np.isfinite(scores)):
                    raise ValueError("model emitted NaN or infinity")
                writer.writerows(
                    (row_id + index, int(user), int(video), format(float(score), ".9g"))
                    for index, (user, video, score) in enumerate(
                        zip(users, videos, scores)
                    )
                )
                row_id += len(users)
    return {
        "rows": row_id,
        "video_metadata": metadata,
        "checkpoint_sha256": sha256(checkpoint_path),
        "source_basic_sha256": sha256(basic),
        "source_log_sha256": sha256(log_path),
        "candidate_sha256": sha256(output_path),
        "candidate_bytes": output_path.stat().st_size,
    }


def check_candidate(data_dir: Path, candidate_path: Path) -> dict:
    log_path = data_dir / "log_standard_4_22_to_5_08_1k.csv"
    expected = iter_test_chunks(log_path, 262144)
    expected_users = expected_videos = None
    expected_position = 0
    checked = 0
    with candidate_path.open(newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader, None)
        if header != HEADER:
            raise ValueError(f"candidate header mismatch: {header}")
        for record in reader:
            if expected_users is None or expected_position == len(expected_users):
                try:
                    expected_users, expected_videos, _, _ = next(expected)
                except StopIteration as error:
                    raise ValueError("candidate has more rows than the test input") from error
                expected_position = 0
            if len(record) != 4:
                raise ValueError(f"candidate row {checked + 2} has {len(record)} fields")
            row_id, user, video, score = record
            if int(row_id) != checked:
                raise ValueError(f"row_id mismatch at candidate line {checked + 2}")
            if int(user) != int(expected_users[expected_position]):
                raise ValueError(f"user mismatch at candidate line {checked + 2}")
            if int(video) != int(expected_videos[expected_position]):
                raise ValueError(f"video mismatch at candidate line {checked + 2}")
            value = float(score)
            if not math.isfinite(value):
                raise ValueError(f"non-finite score at candidate line {checked + 2}")
            checked += 1
            expected_position += 1
    if expected_users is not None and expected_position != len(expected_users):
        raise ValueError("candidate ended before the current source chunk")
    try:
        next(expected)
    except StopIteration:
        pass
    else:
        raise ValueError("candidate ended before the test input")
    return {
        "rows": checked,
        "candidate_sha256": sha256(candidate_path),
        "candidate_bytes": candidate_path.stat().st_size,
        "alignment_checked_without_outcome_columns": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--chunk-size", type=int, default=262144)
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    started = time.time()
    if args.check_only:
        result = check_candidate(args.data_dir, args.output)
    else:
        if args.checkpoint is None:
            raise ValueError("--checkpoint is required unless --check-only is used")
        result = write_candidate(
            args.data_dir, args.checkpoint, args.output, args.chunk_size
        )
        result["alignment"] = check_candidate(args.data_dir, args.output)
    result.update(
        {
            "benchmark": "KuaiRand-1K",
            "split": [TEST_START, TEST_END],
            "public_test_labels_accessed": False,
            "public_test_evaluated": False,
            "elapsed_seconds": time.time() - started,
            "max_rss_bytes": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
        }
    )
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
