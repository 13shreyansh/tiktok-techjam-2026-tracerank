#!/usr/bin/env python3
"""Validate Pure submission alignment without loading or scoring outcomes."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solution.pure_submission import check_submission, expected_rows  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=ROOT / "data" / "KuaiRand-Pure" / "data",
    )
    parser.add_argument("--split", choices=("valid", "test"), default="test")
    args = parser.parse_args()

    count = check_submission(args.candidate, expected_rows(args.data_dir, args.split))
    print(
        f"PASS label-blind Pure alignment: {count:,} rows "
        f"(split={args.split}); outcomes not loaded or scored"
    )


if __name__ == "__main__":
    main()
