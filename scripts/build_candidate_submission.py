#!/usr/bin/env python3
"""Build a local organizer-format CSV from saved prediction scores.

This utility only writes a file. It does not score or upload a submission.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solution.pure_submission import expected_rows, write_submission  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("prediction_file", type=Path)
    parser.add_argument("output_csv", type=Path)
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data" / "KuaiRand-Pure" / "data")
    parser.add_argument("--split", choices=("valid", "test"), default="test")
    args = parser.parse_args()

    with np.load(args.prediction_file) as archive:
        if args.split not in archive.files:
            raise ValueError(f"{args.prediction_file} has no {args.split!r} predictions")
        scores = np.asarray(archive[args.split], dtype=np.float64)

    rows = list(expected_rows(args.data_dir, args.split))
    if len(scores) != len(rows):
        raise ValueError(
            f"prediction count {len(scores)} does not match {args.split} rows {len(rows)}"
        )

    count = write_submission(args.output_csv, rows, scores)
    print(
        f"wrote {args.output_csv}: {count:,} rows (split={args.split}); "
        "outcomes not loaded or scored; no upload performed"
    )


if __name__ == "__main__":
    main()
