#!/usr/bin/env python3
"""Run one counted KuaiRand-27K sample experiment under organizer limits."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import resource
import subprocess
import time
import types
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = "kuairand_27k_sample_ranker.py"
ALLOWED_MODELS = {
    DEFAULT_MODEL,
    "kuairand_27k_author_tag_din_residual.py",
    "kuairand_27k_crossfit_lambdamart_residual.py",
    "kuairand_27k_deepfm_residual.py",
    "kuairand_27k_din_residual.py",
    "kuairand_27k_lambdaloss_finetune.py",
}
DELEGATE = ROOT / "solution" / "kuairand_1k_ranker.py"
EVALUATOR = ROOT / "organizer" / "kuairand-starter-kit" / "evaluate.py"
DEFAULT_CACHE = ROOT / "outputs" / "kuairand-27k-sample-cache"
MAX_ITERATIONS = 50
MAX_SECONDS = 6 * 60 * 60
MAX_ATTEMPT_SECONDS = 90 * 60
ALLOWED_BENCHMARKS = {
    "KuaiRand-27K deterministic development sample",
    "KuaiRand-27K expanded-training deterministic development sample",
    "KuaiRand-27K quarter-training deterministic development sample",
    "KuaiRand-27K half-training deterministic development sample",
    "KuaiRand-27K full-training deterministic development sample",
}


def now() -> dt.datetime:
    return dt.datetime.now().astimezone()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--campaign", required=True)
    parser.add_argument("--id", required=True)
    parser.add_argument("--family", required=True)
    parser.add_argument("--hypothesis", required=True)
    parser.add_argument("--parent", required=True)
    parser.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE)
    parser.add_argument(
        "--model-script", choices=tuple(sorted(ALLOWED_MODELS)), default=DEFAULT_MODEL
    )
    parser.add_argument("model_args", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    model = ROOT / "solution" / args.model_script
    if not re.fullmatch(r"run[0-9]+", args.campaign):
        raise SystemExit("--campaign must look like run24")
    cache_dir = args.cache_dir.resolve()
    if not cache_dir.is_relative_to((ROOT / "outputs").resolve()):
        raise SystemExit("27K cache must remain under this repository's outputs directory")
    cache_manifest_path = cache_dir / "manifest.json"
    if not cache_manifest_path.is_file():
        raise SystemExit("KuaiRand-27K sampled development cache is not prepared")
    cache_manifest = json.loads(cache_manifest_path.read_text())
    if cache_manifest.get("benchmark") not in ALLOWED_BENCHMARKS:
        raise SystemExit("unexpected KuaiRand-27K cache scope")
    benchmark = cache_manifest["benchmark"]

    run_dir = ROOT / "experiments" / args.campaign
    ledger = run_dir / "ledger.jsonl"
    state_path = run_dir / "run_state.json"
    if not state_path.is_file():
        raise SystemExit(f"missing declared run state: {state_path}")
    state = json.loads(state_path.read_text())
    if state.get("benchmark") != benchmark:
        raise SystemExit("declared run benchmark does not match the selected cache")
    if state.get("search_closed", False):
        raise SystemExit(
            f"{args.campaign} search is closed at convergence iteration "
            f"{state.get('converged_at_iteration')}"
        )
    current = now()
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
    forbidden = {"--evaluate-test", "--predict-test", "--test"}
    if forbidden.intersection(model_args):
        raise SystemExit(f"{args.campaign} public-test labels are locked")
    split_mode = next(
        (model_args[i + 1] for i, value in enumerate(model_args[:-1]) if value == "--split-mode"),
        "official",
    )
    if split_mode == "official" and not state.get("shadow_gate_passed", False):
        raise SystemExit("official validation is locked until the declared shadow gate passes")

    outputs = ROOT / "outputs" / "experiments" / args.campaign
    outputs.mkdir(parents=True, exist_ok=True)
    result_path = outputs / f"{args.id}.json"
    if result_path.exists():
        raise SystemExit(f"refusing to overwrite an existing result: {result_path}")
    command = [
        str(ROOT / ".venv" / "bin" / "python"),
        str(model),
        "--cache-dir",
        str(cache_dir),
        "--json-out",
        str(result_path),
    ] + model_args
    remaining = MAX_SECONDS - elapsed_total
    timeout = max(1.0, min(MAX_ATTEMPT_SECONDS, remaining))
    started = time.time()
    try:
        proc = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as error:
        stdout = error.stdout.decode(errors="replace") if isinstance(error.stdout, bytes) else error.stdout or ""
        stderr = error.stderr.decode(errors="replace") if isinstance(error.stderr, bytes) else error.stderr or ""
        proc = types.SimpleNamespace(
            returncode=124,
            stdout=stdout,
            stderr=stderr + f"\nterminated after {timeout:.1f}s by the campaign wall-time guard",
        )
    elapsed = time.time() - started
    usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    state["iterations"] += 1
    state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
    result = json.loads(result_path.read_text()) if proc.returncode == 0 and result_path.exists() else None
    record = {
        "campaign": args.campaign,
        "benchmark": benchmark,
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
        "robustness": result.get("robustness") if result else None,
        "best_iteration": result.get("best_epoch") if result else None,
        "max_rss_bytes": int(usage.ru_maxrss),
        "evaluator_sha256": digest(EVALUATOR),
        "model_sha256": digest(model),
        "delegated_ranker_sha256": digest(DELEGATE),
        "cache_manifest_sha256": digest(cache_manifest_path),
        "score_scope_warning": cache_manifest["score_scope_warning"],
        "public_test_evaluated": False,
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
