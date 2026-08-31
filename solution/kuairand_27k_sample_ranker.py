#!/usr/bin/env python3
"""Run the protected sparse ranker on a declared KuaiRand-27K sample cache."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DELEGATE = ROOT / "solution" / "kuairand_1k_ranker.py"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def argument_value(arguments: list[str], name: str) -> str:
    try:
        position = arguments.index(name)
    except ValueError as error:
        raise ValueError(f"{name} is required") from error
    if position + 1 >= len(arguments):
        raise ValueError(f"{name} has no value")
    return arguments[position + 1]


def relabel_result(
    result: dict[str, object],
    benchmark: str = "KuaiRand-27K deterministic development sample",
) -> dict[str, object]:
    updated = dict(result)
    updated["benchmark"] = benchmark
    updated["score_scope_warning"] = (
        "Metrics describe the declared deterministic development sample, not "
        "the full KuaiRand-27K benchmark or organizer hidden test."
    )
    updated["delegated_ranker"] = {
        "path": str(DELEGATE.relative_to(ROOT)),
        "sha256": sha256(DELEGATE),
    }
    return updated


def main() -> int:
    arguments = sys.argv[1:]
    json_path = Path(argument_value(arguments, "--json-out"))
    if not json_path.is_absolute():
        json_path = ROOT / json_path
    cache_path = Path(argument_value(arguments, "--cache-dir"))
    if not cache_path.is_absolute():
        cache_path = ROOT / cache_path
    benchmark = json.loads((cache_path / "manifest.json").read_text())["benchmark"]
    command = [str(ROOT / ".venv" / "bin" / "python"), str(DELEGATE)] + arguments
    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    for line in completed.stdout.splitlines():
        if not line.startswith("RESULT_JSON="):
            print(line, flush=True)
    if completed.stderr:
        print(completed.stderr, file=sys.stderr, end="")
    if completed.returncode != 0:
        return completed.returncode
    if not json_path.is_file():
        raise FileNotFoundError(f"delegate did not create {json_path}")
    result = relabel_result(json.loads(json_path.read_text()), benchmark)
    json_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("RESULT_JSON=" + json.dumps(result, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
