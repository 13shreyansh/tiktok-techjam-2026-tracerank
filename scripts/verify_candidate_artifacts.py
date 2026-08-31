#!/usr/bin/env python3
"""Verify every selected and fallback artifact declared by the candidate manifest."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests" / "candidate-artifacts.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    manifest = json.loads(MANIFEST.read_text())
    groups = (
        "model_checkpoints",
        "member_predictions",
        "protected_artifacts",
        "fallback_artifacts",
    )
    count = 0
    for group in groups:
        for record in manifest[group]:
            path = ROOT / record["path"]
            if not path.is_file():
                raise FileNotFoundError(path)
            if path.stat().st_size != record["bytes"]:
                raise RuntimeError(f"size mismatch: {record['path']}")
            observed = sha256(path)
            if observed != record["sha256"]:
                raise RuntimeError(f"SHA-256 mismatch: {record['path']}")
            if "rows" in record:
                with path.open(newline="") as handle:
                    rows = sum(1 for _ in csv.reader(handle)) - 1
                if rows != record["rows"]:
                    raise RuntimeError(f"row-count mismatch: {record['path']}")
            print(f"verified {record['path']} sha256={observed}")
            count += 1
    print(f"verified {count} selected and fallback candidate artifacts")


if __name__ == "__main__":
    main()
