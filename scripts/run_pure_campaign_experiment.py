#!/usr/bin/env python3
"""Run one counted KuaiRand-Pure experiment in a declared campaign."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import resource
import subprocess
import time
import types
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVALUATOR = ROOT / "organizer" / "kuairand-starter-kit" / "evaluate.py"
MODEL = ROOT / "solution" / "ranker.py"
MAX_ITERATIONS = 50
MAX_SECONDS = 6 * 60 * 60
MAX_ATTEMPT_SECONDS = 10 * 60
BENCHMARK = "KuaiRand-Pure official validation"


def now() -> dt.datetime:
    return dt.datetime.now().astimezone()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def result_metric_fields(result: dict | None) -> dict:
    """Project every evaluation surface into the immutable attempt record."""
    result = result or {}
    valid = result.get("valid")
    return {
        "valid": valid,
        "valid_primary": valid.get("primary") if valid else None,
        "forward_valid": result.get("forward_valid"),
        "random_validation": result.get("random_validation"),
        "robustness": result.get("robustness"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--campaign", required=True)
    parser.add_argument("--id", required=True)
    parser.add_argument("--family", required=True)
    parser.add_argument("--hypothesis", required=True)
    parser.add_argument("--parent", required=True)
    parser.add_argument("model_args", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if not re.fullmatch(r"run[0-9]+", args.campaign):
        raise SystemExit("--campaign must look like run82")

    run_dir = ROOT / "experiments" / args.campaign
    state_path = run_dir / "run_state.json"
    ledger = run_dir / "ledger.jsonl"
    if not state_path.is_file():
        raise SystemExit(f"missing declared run state: {state_path}")
    state = json.loads(state_path.read_text())
    if state.get("benchmark") != BENCHMARK:
        raise SystemExit("declared benchmark does not match KuaiRand-Pure")
    if state.get("search_closed", False):
        raise SystemExit(f"{args.campaign} search is closed")
    current = now()
    elapsed_total = (
        current - dt.datetime.fromisoformat(state["started_at"])
    ).total_seconds()
    if state["iterations"] >= MAX_ITERATIONS:
        raise SystemExit(f"{args.campaign} has reached its 50-iteration limit")
    if elapsed_total >= MAX_SECONDS:
        raise SystemExit(f"{args.campaign} has reached its six-hour wall-clock limit")
    if state["iterations"] and state["iterations"] % 8 == 0:
        review = run_dir / f"STRATEGIC_REVIEW_{state['iterations']:03d}.md"
        if not review.exists():
            raise SystemExit(f"fresh strategic review required: {review}")

    model_args = args.model_args[1:] if args.model_args[:1] == ["--"] else args.model_args
    if "--evaluate-test" in model_args:
        raise SystemExit("public date-based test labels are locked")
    outputs = ROOT / "outputs" / "experiments" / args.campaign
    outputs.mkdir(parents=True, exist_ok=True)
    result_path = outputs / f"{args.id}.json"
    if result_path.exists():
        raise SystemExit(f"refusing to overwrite existing result: {result_path}")
    command = [
        str(ROOT / ".venv" / "bin" / "python"),
        str(MODEL),
        "--data-dir",
        str(ROOT / "data" / "KuaiRand-Pure" / "data"),
        "--json-out",
        str(result_path),
    ] + model_args
    env = os.environ.copy()
    env["DYLD_LIBRARY_PATH"] = str(ROOT / ".deps" / "libomp" / "22.1.8" / "lib")
    timeout = max(1.0, min(MAX_ATTEMPT_SECONDS, MAX_SECONDS - elapsed_total))
    started = time.time()
    try:
        proc = subprocess.run(
            command,
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as error:
        stdout = (
            error.stdout.decode(errors="replace")
            if isinstance(error.stdout, bytes)
            else error.stdout or ""
        )
        stderr = (
            error.stderr.decode(errors="replace")
            if isinstance(error.stderr, bytes)
            else error.stderr or ""
        )
        proc = types.SimpleNamespace(
            returncode=124,
            stdout=stdout,
            stderr=stderr + f"\nterminated after {timeout:.1f}s by campaign guard",
        )
    elapsed = time.time() - started
    usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    state["iterations"] += 1
    state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
    result = (
        json.loads(result_path.read_text())
        if proc.returncode == 0 and result_path.exists()
        else None
    )
    if (
        proc.returncode == 0
        and state.get("label_boundary_required")
        and (result or {}).get("label_boundary", {}).get("official_test_outcomes_loaded") is not False
    ):
        proc.returncode = 65
        proc.stderr += "\nrequired official-test label-boundary attestation is absent"
    record = {
        "campaign": args.campaign,
        "benchmark": BENCHMARK,
        "iteration": state["iterations"],
        "id": args.id,
        "family": args.family,
        "parent": args.parent,
        "hypothesis": args.hypothesis,
        "started_at": current.isoformat(),
        "elapsed_seconds": elapsed,
        "campaign_elapsed_seconds_at_start": elapsed_total,
        "command": command,
        "returncode": proc.returncode,
        **result_metric_fields(result),
        "max_rss_bytes": int(usage.ru_maxrss),
        "evaluator_sha256": digest(EVALUATOR),
        "model_sha256": digest(MODEL),
        "public_test_evaluated": False,
        "label_boundary": result.get("label_boundary") if result else None,
        "official_test_outcomes_loaded": (
            result.get("label_boundary", {}).get("official_test_outcomes_loaded")
            if result
            else None
        ),
        "stdout_tail": proc.stdout[-8000:],
        "stderr_tail": proc.stderr[-8000:],
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    with ledger.open("a") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")
    print(json.dumps(record, indent=2, sort_keys=True))
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
