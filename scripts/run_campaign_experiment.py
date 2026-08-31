#!/usr/bin/env python3
"""Run one isolated iteration for a numbered Track 2 campaign."""
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
EXPERIMENT_TIMEOUT_SECONDS = 10 * 60


def now() -> dt.datetime:
    return dt.datetime.now().astimezone()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--campaign", required=True)
    parser.add_argument("--id", required=True)
    parser.add_argument("--family", required=True)
    parser.add_argument("--hypothesis", required=True)
    parser.add_argument("--parent", required=True)
    parser.add_argument("model_args", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if not re.fullmatch(r"run[0-9]+", args.campaign):
        raise SystemExit("--campaign must look like run6")

    run_dir = ROOT / "experiments" / args.campaign
    ledger = run_dir / "ledger.jsonl"
    state_path = run_dir / "run_state.json"
    outputs = ROOT / "outputs" / "experiments" / args.campaign

    current = now()
    state = json.loads(state_path.read_text())
    elapsed_total = (current - dt.datetime.fromisoformat(state["started_at"])).total_seconds()
    if state["iterations"] >= MAX_ITERATIONS:
        raise SystemExit(f"{args.campaign} has reached its 50-iteration limit")
    if elapsed_total >= MAX_SECONDS:
        raise SystemExit(f"{args.campaign} has reached its six-hour wall-clock limit")
    if state["iterations"] and state["iterations"] % 8 == 0:
        review = run_dir / f"STRATEGIC_REVIEW_{state['iterations']:03d}.md"
        if not review.exists():
            raise SystemExit(f"fresh strategic review required before another attempt: {review}")

    model_args = args.model_args[1:] if args.model_args[:1] == ["--"] else args.model_args
    if "--evaluate-test" in model_args:
        raise SystemExit(f"{args.campaign} public-test labels are locked")

    outputs.mkdir(parents=True, exist_ok=True)
    result_path = outputs / f"{args.id}.json"
    command = [
        str(ROOT / ".venv" / "bin" / "python"),
        str(MODEL),
        "--data-dir",
        str(ROOT / "data" / "KuaiRand-Pure" / "data"),
        "--json-out",
        str(result_path),
    ] + model_args

    started = time.time()
    env = os.environ.copy()
    env["DYLD_LIBRARY_PATH"] = str(ROOT / ".deps" / "libomp" / "22.1.8" / "lib")
    try:
        proc = subprocess.run(
            command,
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            timeout=EXPERIMENT_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as error:
        stdout = error.stdout.decode(errors="replace") if isinstance(error.stdout, bytes) else error.stdout or ""
        stderr = error.stderr.decode(errors="replace") if isinstance(error.stderr, bytes) else error.stderr or ""
        proc = types.SimpleNamespace(
            returncode=124,
            stdout=stdout,
            stderr=stderr + f"\nterminated by {args.campaign} ten-minute timeout",
        )
    elapsed = time.time() - started
    usage = resource.getrusage(resource.RUSAGE_CHILDREN)

    state["iterations"] += 1
    state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
    result = json.loads(result_path.read_text()) if proc.returncode == 0 and result_path.exists() else None
    split_mode = next(
        (model_args[i + 1] for i, value in enumerate(model_args[:-1]) if value == "--split-mode"),
        "official",
    )
    record = {
        "campaign": args.campaign,
        "iteration": state["iterations"],
        "id": args.id,
        "family": args.family,
        "parent": args.parent,
        "hypothesis": args.hypothesis,
        "split_mode": split_mode,
        "started_at": current.isoformat(),
        "elapsed_seconds": elapsed,
        "campaign_elapsed_seconds_at_start": elapsed_total,
        "command": command,
        "returncode": proc.returncode,
        "valid": result.get("valid") if result else None,
        "valid_primary": result.get("valid", {}).get("primary") if result else None,
        "forward_valid": result.get("forward_valid") if result else None,
        "random_validation": result.get("random_validation") if result else None,
        "robustness": result.get("robustness") if result else None,
        "max_rss_bytes": int(usage.ru_maxrss),
        "evaluator_sha256": hashlib.sha256(EVALUATOR.read_bytes()).hexdigest(),
        "model_sha256": hashlib.sha256(MODEL.read_bytes()).hexdigest(),
        "public_test_evaluated": False,
        "stdout_tail": proc.stdout[-5000:],
        "stderr_tail": proc.stderr[-5000:],
    }
    with ledger.open("a") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")
    print(json.dumps(record, indent=2, sort_keys=True))
    raise SystemExit(proc.returncode)


if __name__ == "__main__":
    main()
