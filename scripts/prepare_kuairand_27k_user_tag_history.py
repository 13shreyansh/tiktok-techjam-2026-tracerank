#!/usr/bin/env python3
"""Build causal per-user primary-tag affinity features for KuaiRand-27K."""
from __future__ import annotations

import argparse
import hashlib
import json
import resource
import time
from pathlib import Path

import numpy as np

try:
    from scripts.prepare_kuairand_1k_history import SPLITS, sha256
    from scripts.prepare_kuairand_27k_user_entity_history import (
        causal_entity_features,
        source_segments,
        user_indices,
    )
except ModuleNotFoundError:  # Direct ``python scripts/...`` execution.
    from prepare_kuairand_1k_history import SPLITS, sha256
    from prepare_kuairand_27k_user_entity_history import (
        causal_entity_features,
        source_segments,
        user_indices,
    )


FEATURE_NAMES = (
    "prior_user_primary_tag_count_log2",
    "prior_user_primary_tag_long_view_rate_21",
)


def build_split(cache_dir: Path, split: str, cutoff: int) -> dict[str, object]:
    users = np.load(cache_dir / "user.npy", mmap_mode="r")
    tags = np.load(cache_dir / "tag.npy", mmap_mode="r")
    times = np.load(cache_dir / "time_ms.npy", mmap_mode="r")
    dates = np.load(cache_dir / "date.npy", mmap_mode="r")
    labels = np.load(cache_dir / "label.npy", mmap_mode="r")
    manifest = json.loads((cache_dir / "manifest.json").read_text())
    row_count = int(manifest["rows"])
    if any(len(array) != row_count for array in (users, tags, times, dates, labels)):
        raise ValueError("user-tag history input lengths do not match manifest")
    segments = source_segments(users)
    output_path = cache_dir / f"user_tag_history_{split}.npy"
    output = np.lib.format.open_memmap(
        output_path, mode="w+", dtype="int16", shape=(row_count, len(FEATURE_NAMES))
    )
    written = 0
    for user in range(int(manifest["user_count"])):
        indices = user_indices(users, segments, user)
        if not len(indices):
            continue
        output[indices] = causal_entity_features(
            tags[indices],
            np.asarray(times[indices], dtype=np.int64),
            np.asarray(dates[indices], dtype=np.int32),
            np.asarray(labels[indices], dtype=np.uint8),
            cutoff,
        )
        written += len(indices)
    if written != row_count:
        raise RuntimeError(f"user-tag feature rows mismatch: {written} != {row_count}")
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
        raise ValueError("user-tag history requires the verified full-training cache")
    record_path = cache_dir / "user_tag_history_manifest.json"
    previous = json.loads(record_path.read_text()) if record_path.is_file() else {}
    splits = dict(previous.get("splits", {}))
    if args.split in splits:
        raise FileExistsError(f"user-tag history already exists for {args.split}")
    result = build_split(cache_dir, args.split, SPLITS[args.split][1])
    splits[args.split] = result
    record = {
        "format_version": 1,
        "feature_names": FEATURE_NAMES,
        "causal_contract": (
            "Per-user primary-tag fields use only earlier timestamps through the "
            "training cutoff; same-timestamp rows update after the whole batch and "
            "validation/forward state is frozen."
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
