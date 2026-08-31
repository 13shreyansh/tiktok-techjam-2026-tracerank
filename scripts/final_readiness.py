#!/usr/bin/env python3
"""Fail-closed local release readiness audit; performs no external action."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str], label: str) -> str:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(
            f"{label} failed ({result.returncode})\n"
            f"stdout:\n{result.stdout[-4000:]}\n"
            f"stderr:\n{result.stderr[-4000:]}"
        )
    print(f"PASS {label}")
    return result.stdout


def ledger_summary() -> dict[str, int]:
    paths = [ROOT / "experiments" / "ledger.jsonl"]
    paths.extend(sorted((ROOT / "experiments").glob("run*/ledger.jsonl")))
    records = []
    for path in paths:
        for line_number, line in enumerate(path.read_text().splitlines(), 1):
            if not line.strip():
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as error:
                raise RuntimeError(f"invalid ledger {path}:{line_number}: {error}")
    summary = {
        "executed": len(records),
        "successful": sum(record.get("returncode") == 0 for record in records),
        "failed_or_timed_out": sum(record.get("returncode") != 0 for record in records),
    }
    expected = {"executed": 344, "successful": 333, "failed_or_timed_out": 11}
    if summary != expected:
        raise RuntimeError(f"experiment accounting drift: {summary} != {expected}")

    run2 = json.loads((ROOT / "experiments/run2/run_state.json").read_text())
    run16 = json.loads((ROOT / "experiments/run16/run_state.json").read_text())
    run17 = json.loads((ROOT / "experiments/run17/run_state.json").read_text())
    run18 = json.loads((ROOT / "experiments/run18/run_state.json").read_text())
    run19 = json.loads((ROOT / "experiments/run19/run_state.json").read_text())
    run20 = json.loads((ROOT / "experiments/run20/run_state.json").read_text())
    run21 = json.loads((ROOT / "experiments/run21/run_state.json").read_text())
    run22 = json.loads((ROOT / "experiments/run22/run_state.json").read_text())
    run23 = json.loads((ROOT / "experiments/run23/run_state.json").read_text())
    run83 = json.loads((ROOT / "experiments/run83/run_state.json").read_text())
    run84 = json.loads((ROOT / "experiments/run84/run_state.json").read_text())
    run85 = json.loads((ROOT / "experiments/run85/run_state.json").read_text())
    run86 = json.loads((ROOT / "experiments/run86/run_state.json").read_text())
    run87 = json.loads((ROOT / "experiments/run87/run_state.json").read_text())
    run88 = json.loads((ROOT / "experiments/run88/run_state.json").read_text())
    run89 = json.loads((ROOT / "experiments/run89/run_state.json").read_text())
    run90 = json.loads((ROOT / "experiments/run90/run_state.json").read_text())
    run91 = json.loads((ROOT / "experiments/run91/run_state.json").read_text())
    run92 = json.loads((ROOT / "experiments/run92/run_state.json").read_text())
    run93 = json.loads((ROOT / "experiments/run93/run_state.json").read_text())
    if run2.get("iterations") != 37 or run2.get("public_test_locked") is not True:
        raise RuntimeError("Run 2 state no longer matches selected-run disclosure")
    if (
        run16.get("iterations") != 18
        or run16.get("eligible_iterations") != 16
        or run16.get("post_convergence_excluded_iterations") != [17, 18]
        or run16.get("search_closed") is not True
        or run16.get("public_test_locked") is not True
    ):
        raise RuntimeError("Run 16 state no longer matches convergence disclosure")
    if (
        run17.get("iterations") != 1
        or run17.get("search_closed") is not True
        or run17.get("public_test_locked") is not True
        or run17.get("shadow_gate_passed") is not False
    ):
        raise RuntimeError("Run 17 state no longer matches failed-gate disclosure")
    if (
        run18.get("iterations") != 1
        or run18.get("search_closed") is not True
        or run18.get("public_test_locked") is not True
        or run18.get("shadow_gate_passed") is not False
    ):
        raise RuntimeError("Run 18 state no longer matches failed-gate disclosure")
    if (
        run19.get("iterations") != 1
        or run19.get("search_closed") is not True
        or run19.get("public_test_locked") is not True
        or run19.get("shadow_gate_passed") is not False
    ):
        raise RuntimeError("Run 19 state no longer matches failed-gate disclosure")
    if (
        run20.get("iterations") != 2
        or run20.get("search_closed") is not True
        or run20.get("public_test_locked") is not True
        or run20.get("shadow_gate_passed") is not False
    ):
        raise RuntimeError("Run 20 state no longer matches failed-gate disclosure")
    if (
        run21.get("iterations") != 1
        or run21.get("search_closed") is not True
        or run21.get("public_test_locked") is not True
        or run21.get("shadow_gate_passed") is not False
    ):
        raise RuntimeError("Run 21 state no longer matches failed-gate disclosure")
    if (
        run22.get("iterations") != 1
        or run22.get("search_closed") is not True
        or run22.get("public_test_locked") is not True
        or run22.get("shadow_gate_passed") is not False
    ):
        raise RuntimeError("Run 22 state no longer matches failed-gate disclosure")
    if (
        run23.get("iterations") != 1
        or run23.get("search_closed") is not True
        or run23.get("public_test_locked") is not True
        or run23.get("shadow_gate_passed") is not False
    ):
        raise RuntimeError("Run 23 state no longer matches failed-gate disclosure")
    if (
        run83.get("iterations") != 24
        or run83.get("search_closed") is not True
        or run83.get("public_test_locked") is not True
        or run83.get("decision")
        != "selected_frozen_run82_all_causal_after_two_of_three_windows"
    ):
        raise RuntimeError("Run 83 state no longer matches final Pure selection")
    if (
        run84.get("iterations") != 8
        or run84.get("duplicate_executions") != 1
        or run84.get("search_closed") is not True
        or run84.get("public_test_locked") is not True
        or run84.get("decision")
        != "selected_clean_six_seed_consensus_after_all_gates"
    ):
        raise RuntimeError("Run 84 state no longer matches clean-candidate disclosure")
    if (
        run85.get("iterations") != 1
        or run85.get("search_closed") is not True
        or run85.get("public_test_locked") is not True
        or run85.get("label_boundary_required") is not True
        or run85.get("decision")
        != "closed_first_shadow_gate_below_materiality_threshold"
    ):
        raise RuntimeError("Run 85 state no longer matches failed-gate disclosure")
    if (
        run86.get("iterations") != 2
        or run86.get("search_closed") is not True
        or run86.get("public_test_locked") is not True
        or run86.get("label_boundary_required") is not True
        or run86.get("decision")
        != "closed_first_scored_shadow_gate_below_materiality_threshold"
    ):
        raise RuntimeError("Run 86 state no longer matches failed-gate disclosure")
    if (
        run87.get("iterations") != 1
        or run87.get("search_closed") is not True
        or run87.get("public_test_locked") is not True
        or run87.get("label_boundary_required") is not True
        or run87.get("decision")
        != "closed_independent_target_and_forward_transfer_gate_failed"
    ):
        raise RuntimeError("Run 87 state no longer matches failed-gate disclosure")
    if (
        run88.get("iterations") != 2
        or run88.get("search_closed") is not True
        or run88.get("public_test_locked") is not True
        or run88.get("label_boundary_required") is not True
        or run88.get("decision")
        != "closed_after_two_chronological_window_failures"
        or "raw_ledger_offsets_preserved" not in run88.get("timestamp_incident", "")
    ):
        raise RuntimeError("Run 88 state no longer matches failed-gate disclosure")
    if (
        run89.get("iterations") != 1
        or run89.get("search_closed") is not True
        or run89.get("public_test_locked") is not True
        or run89.get("label_boundary_required") is not True
        or run89.get("decision") != "closed_catastrophic_opening_transfer_failure"
    ):
        raise RuntimeError("Run 89 state no longer matches failed-gate disclosure")
    if (
        run90.get("iterations") != 1
        or run90.get("search_closed") is not True
        or run90.get("public_test_locked") is not True
        or run90.get("label_boundary_required") is not True
        or run90.get("decision")
        != "closed_opening_forward_and_high_activity_gates_failed"
    ):
        raise RuntimeError("Run 90 state no longer matches failed-gate disclosure")
    if (
        run91.get("iterations") != 1
        or run91.get("search_closed") is not True
        or run91.get("public_test_locked") is not True
        or run91.get("label_boundary_required") is not True
        or run91.get("decision")
        != "closed_opening_validation_and_high_activity_gates_failed"
    ):
        raise RuntimeError("Run 91 state no longer matches failed-gate disclosure")
    if (
        run92.get("iterations") != 1
        or run92.get("search_closed") is not True
        or run92.get("public_test_locked") is not True
        or run92.get("label_boundary_required") is not True
        or run92.get("decision")
        != "closed_opening_validation_forward_and_slice_gates_failed"
    ):
        raise RuntimeError("Run 92 state no longer matches failed-gate disclosure")
    if (
        run93.get("iterations") != 8
        or run93.get("search_closed") is not True
        or run93.get("public_test_locked") is not True
        or run93.get("label_boundary_required") is not True
        or run93.get("decision")
        != "closed_by_user_submission_freeze_before_any_consensus"
    ):
        raise RuntimeError("Run 93 state no longer matches submission-freeze disclosure")
    print("PASS experiment accounting and convergence locks")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--allow-dirty",
        action="store_true",
        help="Permit development testing; final closeout must run clean.",
    )
    parser.add_argument(
        "--skip-1k-alignment",
        action="store_true",
        help="Skip the slow label-blind 1K row-alignment pass; not valid for closeout.",
    )
    args = parser.parse_args()

    dirty = run(["git", "status", "--porcelain"], "Git status").strip()
    if dirty and not args.allow_dirty:
        raise RuntimeError("canonical worktree is dirty")
    if dirty:
        print("WARNING dirty worktree allowed for development test")

    release = json.loads(
        run([sys.executable, "scripts/release_audit.py"], "tracked release audit")
    )
    run([sys.executable, "scripts/verify_run84_candidate.py"], "clean Pure artifacts")
    run(
        [sys.executable, "scripts/verify_kuairand_1k_artifacts.py"],
        "KuaiRand-1K inputs and artifacts",
    )
    run(
        [
            sys.executable,
            "scripts/check_pure_submission.py",
            "outputs/submissions/run84-clean-six-causal-user-rank-test.csv",
            "--data-dir",
            "data/KuaiRand-Pure/data",
            "--split",
            "test",
        ],
        "label-blind Pure CSV alignment",
    )
    if not args.skip_1k_alignment:
        run(
            [
                sys.executable,
                "scripts/predict_kuairand_1k.py",
                "--data-dir",
                "data/KuaiRand-1K/data",
                "--output",
                "outputs/submissions/run16-content-fm-seed2028-kuairand-1k-test.csv",
                "--check-only",
            ],
            "label-blind KuaiRand-1K CSV alignment",
        )
    accounting = ledger_summary()

    placeholders = [
        line.strip()
        for line in (ROOT / "docs/DEVPOST_PACKET.md").read_text().splitlines()
        if "[ADD " in line
    ]
    if len(placeholders) != 4:
        raise RuntimeError(f"unexpected final-link placeholder count: {len(placeholders)}")

    judge_facing = [
        ROOT / "README.md",
        ROOT / "docs/DEVPOST_PACKET.md",
        ROOT / "docs/SUBMISSION_DRAFT.md",
        ROOT / "docs/DEMO_STORYBOARD.md",
        ROOT / "docs/figures/tracerank-system.svg",
        ROOT / "docs/figures/results-summary.svg",
    ]
    stale_selected_values = (
        "candidate reaches 0.605521",
        "scores GAUC 0.672758",
        'card-title">0.605521',
    )
    stale_hits = {
        str(path.relative_to(ROOT)): [
            value for value in stale_selected_values if value in path.read_text()
        ]
        for path in judge_facing
    }
    stale_hits = {path: values for path, values in stale_hits.items() if values}
    if stale_hits:
        raise RuntimeError(
            f"judge-facing files contain quarantined candidate values: {stale_hits}"
        )
    expected_clean_values = {
        "README.md": "0.605375",
        "docs/DEVPOST_PACKET.md": "0.605375",
        "docs/SUBMISSION_DRAFT.md": "scores GAUC 0.672521",
        "docs/DEMO_STORYBOARD.md": "candidate reaches 0.605375",
        "docs/figures/tracerank-system.svg": 'card-title">0.605375',
        "docs/figures/results-summary.svg": "0.605375",
    }
    missing_clean = [
        relative
        for relative, expected in expected_clean_values.items()
        if expected not in (ROOT / relative).read_text()
    ]
    if missing_clean:
        raise RuntimeError(
            f"judge-facing files omit clean selected candidate values: {missing_clean}"
        )
    print("PASS clean candidate narrative consistency")

    result = {
        "status": "local_ready_external_actions_pending",
        "git_clean": not bool(dirty),
        "one_k_alignment_executed": not args.skip_1k_alignment,
        "release_audit": release,
        "experiment_accounting": accounting,
        "external_blockers": [
            "refresh action-time usage counters if work continues before submission",
            "insert verified public repository, YouTube demo, and working-project URLs",
            "obtain the KuaiRand-1K delivery route",
            "receive explicit user authorization for push, visibility, upload, and submission",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
