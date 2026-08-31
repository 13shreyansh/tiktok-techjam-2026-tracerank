#!/usr/bin/env python3
"""Verify the selected KuaiRand-1K inputs, artifacts, and label-use receipt."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
INPUT_MANIFEST = ROOT / "manifests" / "kuairand-1k-content-cache-inputs.json"
CANDIDATE_MANIFEST = ROOT / "manifests" / "kuairand-1k-candidate-artifacts.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_file(path: Path, record: dict, label: str) -> None:
    if not path.is_file():
        raise FileNotFoundError(path)
    expected_bytes = record.get("bytes")
    if expected_bytes is not None and path.stat().st_size != expected_bytes:
        raise RuntimeError(f"{label} size mismatch: {path}")
    observed = sha256(path)
    if observed != record["sha256"]:
        raise RuntimeError(f"{label} SHA-256 mismatch: {path}")
    print(f"verified {label}: {path.relative_to(ROOT)} sha256={observed}")


def main() -> None:
    inputs = json.loads(INPUT_MANIFEST.read_text())
    candidate = json.loads(CANDIDATE_MANIFEST.read_text())
    rows = int(inputs["rows"])

    candidate_inputs = candidate["inputs"]
    if candidate_inputs.get("stable_cache_input_manifest") != str(
        INPUT_MANIFEST.relative_to(ROOT)
    ):
        raise RuntimeError("candidate points to the wrong stable input manifest")
    if sha256(INPUT_MANIFEST) != candidate_inputs.get(
        "stable_cache_input_manifest_sha256"
    ):
        raise RuntimeError("stable input-manifest SHA-256 mismatch")
    if candidate_inputs.get("historical_volatile_cache_manifest_sha256") != inputs[
        "historical_manifest"
    ]["sha256_at_candidate_training"]:
        raise RuntimeError("historical cache-manifest identity mismatch")

    for record in inputs["source_files"]:
        verify_file(ROOT / record["path"], record, "1K source")

    cache_dir = ROOT / inputs["cache_directory"]
    for record in inputs["arrays"]:
        path = cache_dir / record["path"]
        verify_file(path, record, "1K stable cache array")
        array = np.load(path, mmap_mode="r", allow_pickle=False)
        if len(array) != rows:
            raise RuntimeError(f"cache row-count mismatch: {path}")

    artifacts = candidate["ignored_artifacts"]
    for name in (
        "checkpoint",
        "validation_predictions",
        "test_format_candidate",
        "inference_receipt",
    ):
        record = artifacts[name]
        verify_file(ROOT / record["path"], record, f"1K {name}")

    predictions = np.load(
        ROOT / artifacts["validation_predictions"]["path"], allow_pickle=False
    )
    if predictions.files != ["valid"] or predictions["valid"].shape != (2524980,):
        raise RuntimeError("1K validation prediction schema mismatch")
    if not np.all(np.isfinite(predictions["valid"])):
        raise RuntimeError("1K validation predictions contain NaN or infinity")

    receipt = json.loads((ROOT / artifacts["inference_receipt"]["path"]).read_text())
    if receipt.get("public_test_labels_accessed") is not False:
        raise RuntimeError("1K receipt does not prove label-blind packaging")
    if receipt.get("public_test_evaluated") is not False:
        raise RuntimeError("1K receipt indicates public-test evaluation")
    if receipt.get("rows") != artifacts["test_format_candidate"]["rows"]:
        raise RuntimeError("1K receipt row count disagrees with manifest")
    if receipt.get("candidate_sha256") != artifacts["test_format_candidate"]["sha256"]:
        raise RuntimeError("1K receipt candidate hash disagrees with manifest")

    print(
        "verified KuaiRand-1K stable inputs and candidate: "
        f"{len(inputs['arrays'])} cache arrays, {rows} rows, label-blind receipt"
    )


if __name__ == "__main__":
    main()
