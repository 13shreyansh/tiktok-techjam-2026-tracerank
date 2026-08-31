#!/usr/bin/env python3
"""Run one auditable Track 2 iteration and append its result to the ledger."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import resource
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "experiments" / "ledger.jsonl"
STATE = ROOT / "experiments" / "run_state.json"
OUTPUTS = ROOT / "outputs" / "experiments"
EVALUATOR = ROOT / "organizer" / "kuairand-starter-kit" / "evaluate.py"
OFFICIAL_START = dt.datetime(2026, 8, 29, 12, 0, tzinfo=dt.timezone(dt.timedelta(hours=8)))
MAX_ITERATIONS = 50
MAX_SECONDS = 6 * 60 * 60


def now():
    return dt.datetime.now().astimezone()


def load_state():
    if STATE.exists():
        return json.loads(STATE.read_text())
    return {"started_at": now().isoformat(), "iterations": 0}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--hypothesis", required=True)
    ap.add_argument("model_args", nargs=argparse.REMAINDER)
    args = ap.parse_args()
    current = now()
    if current < OFFICIAL_START:
        raise SystemExit("refusing judged experiment before official start")
    state = load_state()
    elapsed_total = (current - dt.datetime.fromisoformat(state["started_at"])).total_seconds()
    if state["iterations"] >= MAX_ITERATIONS:
        raise SystemExit("50-iteration limit reached")
    if elapsed_total >= MAX_SECONDS:
        raise SystemExit("six-hour wall-clock limit reached")

    OUTPUTS.mkdir(parents=True, exist_ok=True)
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    result_path = OUTPUTS / f"{args.id}.json"
    model_args = args.model_args[1:] if args.model_args[:1] == ["--"] else args.model_args
    command = [
        str(ROOT / ".venv" / "bin" / "python"),
        str(ROOT / "solution" / "ranker.py"),
        "--data-dir",
        str(ROOT / "data" / "KuaiRand-Pure" / "data"),
        "--json-out",
        str(result_path),
    ] + model_args
    t0 = time.time()
    env = os.environ.copy()
    local_libomp = ROOT / ".deps" / "libomp" / "22.1.8" / "lib"
    env["DYLD_LIBRARY_PATH"] = str(local_libomp)
    proc = subprocess.run(command, cwd=ROOT, env=env, text=True, capture_output=True)
    elapsed = time.time() - t0
    usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    state["iterations"] += 1
    STATE.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
    result = json.loads(result_path.read_text()) if proc.returncode == 0 and result_path.exists() else None
    previous = []
    if LEDGER.exists():
        previous = [json.loads(line) for line in LEDGER.read_text().splitlines() if line.strip()]
    best_before = max((x.get("valid_primary", float("-inf")) for x in previous if x["returncode"] == 0), default=None)
    primary = result["valid"]["primary"] if result else None
    record = {
        "iteration": state["iterations"],
        "id": args.id,
        "started_at": current.isoformat(),
        "elapsed_seconds": elapsed,
        "agent_elapsed_seconds_at_start": elapsed_total,
        "hypothesis": args.hypothesis,
        "command": command,
        "returncode": proc.returncode,
        "valid_primary": primary,
        "valid": result.get("valid") if result else None,
        "best_iteration": result.get("best_iteration") if result else None,
        "improved_over_previous_best": bool(primary is not None and (best_before is None or primary > best_before)),
        "max_rss_bytes": int(usage.ru_maxrss),
        "evaluator_sha256": hashlib.sha256(EVALUATOR.read_bytes()).hexdigest(),
        "stdout_tail": proc.stdout[-4000:],
        "stderr_tail": proc.stderr[-4000:],
    }
    with LEDGER.open("a") as fh:
        fh.write(json.dumps(record, sort_keys=True) + "\n")
    print(json.dumps(record, indent=2, sort_keys=True))
    raise SystemExit(proc.returncode)


if __name__ == "__main__":
    main()
