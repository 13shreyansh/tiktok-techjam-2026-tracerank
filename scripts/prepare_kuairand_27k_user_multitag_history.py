#!/usr/bin/env python3
"""Build causal user/primary-tag affinity using all historical tag positions."""
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
        causal_entity_features,
        source_segments,
        user_indices,
    )
except ModuleNotFoundError:  # Direct ``python scripts/...`` execution.
    from prepare_kuairand_1k_history import SPLITS, rate_bucket, sha256
    from prepare_kuairand_27k_user_entity_history import (
        causal_entity_features,
        source_segments,
        user_indices,
    )


FEATURE_NAMES = (
    "prior_user_primary_tag_any_position_count_log2",
    "prior_user_primary_tag_any_position_long_view_rate_21",
)


def causal_primary_from_multitag_features(
    tags: np.ndarray,
    times: np.ndarray,
    dates: np.ndarray,
    labels: np.ndarray,
    cutoff: int,
) -> np.ndarray:
    """Score each row's primary tag from prior occurrences in any tag slot."""
    tags = np.asarray(tags, dtype=np.int64)
    if tags.ndim != 2 or tags.shape[1] != 3:
        raise ValueError("multitag history expects exactly three tag columns")
    row_count = len(tags)
    output = np.empty((row_count, 2), dtype=np.int16)
    output[:, 0] = 0
    output[:, 1] = int(rate_bucket(0, 0))

    rows = np.repeat(np.arange(row_count, dtype=np.int64), 3)
    slots = np.tile(np.arange(3, dtype=np.int8), row_count)
    flattened = tags.reshape(-1)
    valid = flattened >= 0
    # One video's duplicate tag should update its history only once.
    valid[1::3] &= tags[:, 1] != tags[:, 0]
    valid[2::3] &= (tags[:, 2] != tags[:, 0]) & (tags[:, 2] != tags[:, 1])
    selected = np.flatnonzero(valid)
    if not len(selected):
        return output
    selected_rows = rows[selected]
    exploded = causal_entity_features(
        flattened[selected],
        np.asarray(times, dtype=np.int64)[selected_rows],
        np.asarray(dates, dtype=np.int32)[selected_rows],
        np.asarray(labels, dtype=np.uint8)[selected_rows],
        cutoff,
    )
    primary = slots[selected] == 0
    output[selected_rows[primary]] = exploded[primary]
    return output


def build_split(cache_dir: Path, split: str, cutoff: int) -> dict[str, object]:
    users = np.load(cache_dir / "user.npy", mmap_mode="r")
    tag1 = np.load(cache_dir / "tag.npy", mmap_mode="r")
    tag2 = np.load(cache_dir / "tag2.npy", mmap_mode="r")
    tag3 = np.load(cache_dir / "tag3.npy", mmap_mode="r")
    times = np.load(cache_dir / "time_ms.npy", mmap_mode="r")
    dates = np.load(cache_dir / "date.npy", mmap_mode="r")
    labels = np.load(cache_dir / "label.npy", mmap_mode="r")
    manifest = json.loads((cache_dir / "manifest.json").read_text())
    row_count = int(manifest["rows"])
    inputs = (users, tag1, tag2, tag3, times, dates, labels)
    if any(len(array) != row_count for array in inputs):
        raise ValueError("user-multitag history input lengths do not match manifest")
    segments = source_segments(users)
    output_path = cache_dir / f"user_multitag_history_{split}.npy"
    output = np.lib.format.open_memmap(
        output_path, mode="w+", dtype="int16", shape=(row_count, len(FEATURE_NAMES))
    )
    written = 0
    for user in range(int(manifest["user_count"])):
        indices = user_indices(users, segments, user)
        if not len(indices):
            continue
        local_tags = np.column_stack((tag1[indices], tag2[indices], tag3[indices]))
        output[indices] = causal_primary_from_multitag_features(
            local_tags,
            np.asarray(times[indices], dtype=np.int64),
            np.asarray(dates[indices], dtype=np.int32),
            np.asarray(labels[indices], dtype=np.uint8),
            cutoff,
        )
        written += len(indices)
    if written != row_count:
        raise RuntimeError(f"user-multitag rows mismatch: {written} != {row_count}")
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
        raise ValueError("user-multitag history requires the verified full-training cache")
    record_path = cache_dir / "user_multitag_history_manifest.json"
    previous = json.loads(record_path.read_text()) if record_path.is_file() else {}
    splits = dict(previous.get("splits", {}))
    if args.split in splits:
        raise FileExistsError(f"user-multitag history already exists for {args.split}")
    result = build_split(cache_dir, args.split, SPLITS[args.split][1])
    splits[args.split] = result
    record = {
        "format_version": 1,
        "feature_names": FEATURE_NAMES,
        "causal_contract": (
            "Current primary-tag affinity counts prior rows where that tag appeared "
            "in any unique tag position; same-timestamp rows share prior state, "
            "updates stop at the training cutoff, and scoring state is frozen."
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
