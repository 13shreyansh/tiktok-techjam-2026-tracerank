#!/usr/bin/env python3
"""Read-only, memory-bounded inspection of a verified KuaiRand-27K extract."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


EXPECTED_FILES = (
    "log_random_4_22_to_5_08_27k.csv",
    "log_standard_4_08_to_4_21_27k_part1.csv",
    "log_standard_4_08_to_4_21_27k_part2.csv",
    "log_standard_4_22_to_5_08_27k_part1.csv",
    "log_standard_4_22_to_5_08_27k_part2.csv",
    "user_features_27k.csv",
    "video_features_basic_27k.csv",
    "video_features_statistic_27k_part1.csv",
    "video_features_statistic_27k_part2.csv",
    "video_features_statistic_27k_part3.csv",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def last_nonempty_line(path: Path, chunk_size: int = 65536) -> str:
    """Return the last non-empty UTF-8 line without loading the full file."""

    with path.open("rb") as handle:
        handle.seek(0, 2)
        position = handle.tell()
        buffer = b""
        while position > 0:
            take = min(chunk_size, position)
            position -= take
            handle.seek(position)
            buffer = handle.read(take) + buffer
            lines = buffer.splitlines()
            if position == 0 or len(lines) > 1:
                for line in reversed(lines):
                    if line.strip():
                        return line.decode("utf-8")
        raise ValueError(f"no non-empty line in {path}")


def inspect_csv(path: Path) -> dict[str, object]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        first = next(reader, None)
        header = reader.fieldnames or []

    last_values = next(csv.reader([last_nonempty_line(path)]))
    last = dict(zip(header, last_values))
    sampled = {}
    for field in ("date", "time_ms", "user_id", "video_id"):
        if field in header:
            sampled[field] = {
                "first_record": first.get(field) if first else None,
                "last_record": last.get(field),
            }
    return {
        "bytes": path.stat().st_size,
        "columns": header,
        "sampled_endpoints_only": sampled,
    }


def locate_extract(root: Path) -> tuple[Path, Path]:
    candidates = (root, root / "data")
    for data_dir in candidates:
        if all((data_dir / name).is_file() for name in EXPECTED_FILES):
            return root, data_dir
    raise FileNotFoundError(
        "expected KuaiRand-27K files were not all found under "
        f"{root} or {root / 'data'}"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("data/KuaiRand-27K"),
        help="extracted KuaiRand-27K directory",
    )
    parser.add_argument(
        "--json-out",
        type=Path,
        help="optional ignored JSON receipt path",
    )
    args = parser.parse_args()

    extract_root, data_dir = locate_extract(args.root.resolve())
    files = {name: inspect_csv(data_dir / name) for name in EXPECTED_FILES}

    loaders = sorted(extract_root.rglob("load_data_27k.py"))
    licences = sorted(
        path
        for path in extract_root.rglob("*")
        if path.is_file() and path.name.lower().startswith(("license", "licence"))
    )
    report = {
        "extract_root": str(extract_root),
        "data_dir": str(data_dir),
        "expected_file_count": len(EXPECTED_FILES),
        "files": files,
        "loaders": [
            {"path": str(path), "bytes": path.stat().st_size, "sha256": sha256(path)}
            for path in loaders
        ],
        "licences": [
            {"path": str(path), "bytes": path.stat().st_size, "sha256": sha256(path)}
            for path in licences
        ],
        "warning": (
            "sampled_endpoints_only records first and last physical rows; it does "
            "not prove sorting or complete date ranges"
        ),
    }
    serialized = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(serialized)
    print(serialized, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
