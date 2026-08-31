"""Label-blind KuaiRand-Pure submission I/O.

Only date, user_id, and video_id are projected from the interaction logs. No
outcome column is named, returned, scored, or used for candidate selection.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path


HEADER = ["row_id", "user_id", "video_id", "score"]
SPLIT_DATES = {
    "valid": (20220422, 20220428),
    "test": (20220429, 20220508),
}
LOG_FILES = (
    "log_standard_4_08_to_4_21_pure.csv",
    "log_standard_4_22_to_5_08_pure.csv",
)


def expected_rows(data_dir: Path, split: str):
    """Yield feature-only alignment keys in organizer file order."""
    if split not in SPLIT_DATES:
        raise ValueError(f"unsupported split: {split}")
    lower, upper = SPLIT_DATES[split]
    for filename in LOG_FILES:
        with (Path(data_dir) / filename).open(newline="") as handle:
            reader = csv.reader(handle)
            header = next(reader)
            indices = {name: header.index(name) for name in ("date", "user_id", "video_id")}
            for record in reader:
                date = int(record[indices["date"]])
                if lower <= date <= upper:
                    yield record[indices["user_id"]], record[indices["video_id"]]


def write_submission(path: Path, rows, scores) -> int:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(HEADER)
        for count, ((user, video), score) in enumerate(zip(rows, scores), start=1):
            value = float(score)
            if not math.isfinite(value):
                raise ValueError(f"prediction {count - 1} is not finite")
            # Nine significant digits round-trip a float32 score. The organizer
            # accepts arbitrary finite reals; extra precision avoids creating
            # new within-user ties during CSV packaging.
            writer.writerow([count - 1, user, video, f"{value:.9g}"])
    return count


def check_submission(path: Path, rows) -> int:
    expected = iter(rows)
    checked = 0
    with Path(path).open(newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader, None)
        if header != HEADER:
            raise ValueError(f"header must be {','.join(HEADER)}; got {header}")
        for line_number, record in enumerate(reader, start=2):
            if len(record) != 4:
                raise ValueError(f"line {line_number} has {len(record)} fields; expected 4")
            row_id, user, video, score = record
            if int(row_id) != checked:
                raise ValueError(f"line {line_number} row_id={row_id}; expected {checked}")
            try:
                expected_user, expected_video = next(expected)
            except StopIteration as error:
                raise ValueError("candidate has more rows than the requested split") from error
            if (user, video) != (expected_user, expected_video):
                raise ValueError(
                    f"line {line_number} alignment mismatch: {(user, video)} != "
                    f"{(expected_user, expected_video)}"
                )
            try:
                value = float(score)
            except ValueError as error:
                raise ValueError(f"line {line_number} score is not numeric: {score!r}") from error
            if not math.isfinite(value):
                raise ValueError(f"line {line_number} score is not finite")
            checked += 1
    try:
        next(expected)
    except StopIteration:
        return checked
    raise ValueError("candidate has fewer rows than the requested split")
