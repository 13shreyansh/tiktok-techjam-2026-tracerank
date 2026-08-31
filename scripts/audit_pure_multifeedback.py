#!/usr/bin/env python3
"""Audit Pure feedback overlap using only the authorized training log."""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter
from pathlib import Path


SIGNALS = (
    "click",
    "like",
    "follow",
    "comment",
    "forward",
    "hate",
    "deep_engagement",
    "positive_action",
)


def binary_phi(n: int, a: int, b: int, both: int) -> float | None:
    """Return the phi coefficient for two binary variables."""
    denominator = math.sqrt(a * (n - a) * b * (n - b))
    if denominator == 0:
        return None
    return (n * both - a * b) / denominator


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, required=True)
    args = parser.parse_args()

    source = args.data_dir / "log_standard_4_08_to_4_21_pure.csv"
    counts: Counter[str] = Counter()
    joint_with_long_view: Counter[str] = Counter()
    rows = 0
    with source.open(newline="") as handle:
        for row in csv.DictReader(handle):
            rows += 1
            long_view = int(row["long_view"])
            values = {
                "click": int(row["is_click"]),
                "like": int(row["is_like"]),
                "follow": int(row["is_follow"]),
                "comment": int(row["is_comment"]),
                "forward": int(row["is_forward"]),
                "hate": int(row["is_hate"]),
            }
            values["deep_engagement"] = int(
                any(values[name] for name in ("like", "follow", "comment", "forward"))
            )
            values["positive_action"] = int(
                any(values[name] for name in ("click", "like", "follow", "comment", "forward"))
            )
            counts["long_view"] += long_view
            for name in SIGNALS:
                counts[name] += values[name]
                joint_with_long_view[name] += values[name] * long_view

    long_views = counts["long_view"]
    result = {
        "source": str(source),
        "scope": "training rows only; no validation, random, or test file read",
        "rows": rows,
        "long_view": {
            "positives": long_views,
            "rate": long_views / rows,
        },
        "signals": {},
    }
    for name in SIGNALS:
        positives = counts[name]
        joint = joint_with_long_view[name]
        result["signals"][name] = {
            "positives": positives,
            "rate": positives / rows,
            "joint_with_long_view": joint,
            "p_long_view_given_signal": joint / positives if positives else None,
            "p_signal_given_long_view": joint / long_views if long_views else None,
            "phi_with_long_view": binary_phi(rows, long_views, positives, joint),
        }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
