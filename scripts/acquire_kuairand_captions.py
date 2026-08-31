#!/usr/bin/env python3
"""Acquire the exact official KuaiRand-Pure caption subset reproducibly."""

from __future__ import annotations

import csv
import hashlib
import subprocess
import tempfile
from pathlib import Path


URL = "https://zenodo.org/records/18159199/files/kuairand_video_captions.csv"
PREFIX_BYTES = 4_194_304
PURE_ROWS = 7_583
EXPECTED_PREFIX_SHA256 = "d8db383fb1a92477c837c1cf3e9f5f26adbd41e89212ee245198e06a6b39318f"
EXPECTED_SUBSET_SHA256 = "7593a7e1497951a16ca29126605b751869cf66df5a2f845f7690b2f6c1f4ba2c"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    output_dir = Path("data/kuairand-supplemental")
    with tempfile.TemporaryDirectory(prefix="kuairand-captions-") as temporary:
        temporary_dir = Path(temporary)
        prefix = temporary_dir / "captions.prefix.csv"
        subset = temporary_dir / "captions.pure.csv"
        subprocess.run(
            [
                "curl",
                "--fail",
                "--location",
                "--range",
                f"0-{PREFIX_BYTES - 1}",
                "--output",
                str(prefix),
                URL,
            ],
            check=True,
        )
        if prefix.stat().st_size != PREFIX_BYTES:
            raise RuntimeError(f"unexpected prefix size: {prefix.stat().st_size}")
        prefix_sha256 = sha256(prefix)
        if prefix_sha256 != EXPECTED_PREFIX_SHA256:
            raise RuntimeError(f"unexpected prefix SHA-256: {prefix_sha256}")

        with prefix.open(newline="") as source, subset.open("w", newline="") as destination:
            reader = csv.DictReader(source)
            if reader.fieldnames != ["final_video_id", "caption", "show_cover_text", "duration"]:
                raise RuntimeError(f"unexpected columns: {reader.fieldnames}")
            writer = csv.DictWriter(destination, fieldnames=reader.fieldnames, lineterminator="\n")
            writer.writeheader()
            for expected_id in range(PURE_ROWS):
                row = next(reader)
                if row["final_video_id"] != str(expected_id):
                    raise RuntimeError(
                        f"unexpected video ID at row {expected_id}: {row['final_video_id']}"
                    )
                writer.writerow(row)

        subset_sha256 = sha256(subset)
        if subset_sha256 != EXPECTED_SUBSET_SHA256:
            raise RuntimeError(f"unexpected subset SHA-256: {subset_sha256}")
        output_dir.mkdir(parents=True, exist_ok=True)
        prefix.replace(output_dir / "kuairand_video_captions.prefix.csv")
        subset.replace(output_dir / "kuairand_video_captions_pure.csv")
    print(
        f"verified rows={PURE_ROWS} ids=0..{PURE_ROWS - 1} "
        f"sha256={EXPECTED_SUBSET_SHA256}"
    )


if __name__ == "__main__":
    main()
