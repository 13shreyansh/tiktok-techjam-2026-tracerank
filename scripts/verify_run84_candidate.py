#!/usr/bin/env python3
"""Verify the clean Pure candidate without reading any final-test outcome."""
from __future__ import annotations

import collections
import csv
import hashlib
import json
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
STARTER = ROOT / "organizer" / "kuairand-starter-kit"
sys.path.insert(0, str(STARTER))
from evaluate import evaluate  # noqa: E402


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def development_rows(data_dir: Path):
    """Project only user/date/long_view, and never include dates after 28 April."""
    splits = {"train": [], "valid": []}
    for filename in (
        "log_standard_4_08_to_4_21_pure.csv",
        "log_standard_4_22_to_5_08_pure.csv",
    ):
        with (data_dir / filename).open(newline="") as handle:
            for raw in csv.DictReader(handle):
                date = int(raw["date"])
                if 20220408 <= date <= 20220421:
                    split = "train"
                elif 20220422 <= date <= 20220428:
                    split = "valid"
                else:
                    continue
                splits[split].append(
                    {"user": raw["user_id"], "date": date, "label": int(raw["long_view"] != "0")}
                )
    return splits


def robustness(train, valid, scores):
    activity = collections.Counter(row["user"] for row in train)
    counts = np.asarray([activity[row["user"]] for row in valid])
    positive = counts[counts > 0]
    cut1, cut2 = np.quantile(positive, [1 / 3, 2 / 3])
    dates = sorted({row["date"] for row in valid})
    midpoint = len(dates) // 2
    masks = {
        "early_dates": np.asarray([row["date"] in set(dates[:midpoint]) for row in valid]),
        "late_dates": np.asarray([row["date"] in set(dates[midpoint:]) for row in valid]),
        "cold_or_low_activity": counts <= cut1,
        "medium_activity": (counts > cut1) & (counts <= cut2),
        "high_activity": counts > cut2,
    }
    result = {}
    for name, mask in masks.items():
        indices = np.flatnonzero(mask)
        result[name] = evaluate(
            [valid[index]["user"] for index in indices],
            [valid[index]["label"] for index in indices],
            np.asarray(scores)[indices],
        )
    return result


def main() -> None:
    manifest = json.loads((ROOT / "manifests/run84-candidate-artifacts.json").read_text())
    for record in manifest["artifacts"]:
        path = ROOT / record["path"]
        if path.stat().st_size != record["bytes"] or sha256(path) != record["sha256"]:
            raise RuntimeError(f"artifact verification failed: {record['path']}")

    ledger = [json.loads(line) for line in (ROOT / "experiments/run84/ledger.jsonl").read_text().splitlines()]
    expected_ids = {
        "001-clean-seed2026-official": 2,
        "002-clean-seed2027-official": 1,
        "003-clean-seed2028-official": 1,
        "004-clean-seed2029-official": 1,
        "005-clean-seed2030-official": 1,
        "006-clean-seed2031-official": 1,
        "007-clean-six-causal-user-rank-official": 1,
    }
    observed_ids = collections.Counter(record["id"] for record in ledger)
    if len(ledger) != 8 or observed_ids != expected_ids or any(record["returncode"] != 0 for record in ledger):
        raise RuntimeError("Run84 execution accounting does not match the disclosed duplicate")
    if any(record.get("official_test_outcomes_loaded") is not False for record in ledger):
        raise RuntimeError("Run84 label-boundary attestation failed")

    data = development_rows(ROOT / "data/KuaiRand-Pure/data")
    candidate_path = ROOT / "outputs/predictions/run84-clean-six-causal-user-rank-final.npz"
    reference_path = ROOT / "outputs/predictions/run82-six-causal-user-rank-final.npz"
    with np.load(candidate_path) as archive:
        valid_scores = np.asarray(archive["valid"], dtype=np.float64)
        test_scores = np.asarray(archive["test"], dtype=np.float64)
    if len(valid_scores) != 124909 or len(test_scores) != 170588:
        raise RuntimeError("candidate prediction shape mismatch")
    if not np.isfinite(valid_scores).all() or not np.isfinite(test_scores).all():
        raise RuntimeError("candidate contains non-finite predictions")
    observed = evaluate(
        [row["user"] for row in data["valid"]],
        [row["label"] for row in data["valid"]],
        valid_scores,
    )
    for metric in ("GAUC", "nDCG@5", "primary"):
        if abs(observed[metric] - manifest["validation"][metric]) > 1e-12:
            raise RuntimeError(f"manifest validation drift for {metric}")
    for metric, threshold in (("GAUC", 0.6723), ("nDCG@5", 0.5380), ("primary", 0.6053)):
        if observed[metric] < threshold:
            raise RuntimeError(f"Run84 {metric} gate failed: {observed[metric]} < {threshold}")

    with np.load(reference_path) as archive:
        reference_scores = np.asarray(archive["valid"], dtype=np.float64)
    candidate_slices = robustness(data["train"], data["valid"], valid_scores)
    reference_slices = robustness(data["train"], data["valid"], reference_scores)
    slice_deltas = {
        name: candidate_slices[name]["primary"] - reference_slices[name]["primary"]
        for name in candidate_slices
    }
    if min(slice_deltas.values()) < -0.001:
        raise RuntimeError(f"Run84 robustness gate failed: {slice_deltas}")

    print(
        json.dumps(
            {
                "status": "pass",
                "attempts": len(ledger),
                "official_test_outcomes_loaded": False,
                "validation": observed,
                "minimum_slice_delta_vs_run82": min(slice_deltas.values()),
                "artifact_count": len(manifest["artifacts"]),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
