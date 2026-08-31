#!/usr/bin/env python3
"""Audit the tracked repository without datasets, caches, or model outputs."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_PREFIXES = ("data/", "datasets/", "outputs/", "checkpoints/", ".venv/")
REQUIRED_FILES = (
    "README.md",
    "PREPARATION_STATUS.md",
    "requirements.txt",
    "docs/SOLUTION_REPORT.md",
    "docs/JUDGE_QUICKSTART.md",
    "docs/RUN2_REPORT.md",
    "docs/RUN84_REPORT.md",
    "docs/RUN16_REPORT.md",
    "docs/RESOURCE_REPORT.md",
    "docs/DEMO_STORYBOARD.md",
    "docs/DEVPOST_PACKET.md",
    "docs/DISCLOSURE_SNAPSHOT.md",
    "docs/PUBLIC_RELEASE_PROTOCOL.md",
    "docs/OFFICIAL_FAQ_AUDIT_2026-08-31.md",
    "docs/TEST_LABEL_COMPLIANCE_AUDIT_2026-08-31.md",
    "docs/licenses/KuaiRand-Pure-LICENSE.txt",
    "docs/figures/results-summary.svg",
    "docs/figures/tracerank-system.svg",
    "manifests/candidate-artifacts.json",
    "manifests/run84-candidate-artifacts.json",
    "manifests/kuairand-1k-candidate-artifacts.json",
    "manifests/kuairand-1k-content-cache-inputs.json",
    "manifests/official-resources.json",
    "manifests/starter-kit.sha256",
    "organizer/kuairand-starter-kit/evaluate.py",
    "scripts/release_audit.py",
    "scripts/build_public_release.py",
    "scripts/final_readiness.py",
    "scripts/verify_run84_candidate.py",
    "scripts/check_pure_submission.py",
    "scripts/verify_kuairand_1k_artifacts.py",
)
SECRET_PATTERNS = {
    "OpenAI-style key": re.compile(rb"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "GitHub token": re.compile(rb"\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}\b"),
    "Google API key": re.compile(rb"\bAIza[0-9A-Za-z_-]{30,}\b"),
    "AWS access key": re.compile(rb"\bAKIA[0-9A-Z]{16}\b"),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tracked_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z"], cwd=ROOT, check=True, capture_output=True
    )
    return [item.decode() for item in result.stdout.split(b"\0") if item]


def main() -> None:
    errors: list[str] = []
    tracked = tracked_files()
    tracked_set = set(tracked)

    for required in REQUIRED_FILES:
        if required not in tracked_set:
            errors.append(f"required tracked file missing: {required}")

    forbidden = [path for path in tracked if path.startswith(FORBIDDEN_PREFIXES)]
    if forbidden:
        errors.extend(
            f"forbidden large-artifact path is tracked: {path}" for path in forbidden
        )

    oversized = [
        (path, (ROOT / path).stat().st_size)
        for path in tracked
        if (ROOT / path).is_file() and (ROOT / path).stat().st_size > 10 * 1024 * 1024
    ]
    errors.extend(
        f"tracked file exceeds 10 MiB: {path} ({size} bytes)"
        for path, size in oversized
    )

    json_files = [path for path in tracked if path.endswith(".json")]
    jsonl_files = [path for path in tracked if path.endswith(".jsonl")]
    for path in json_files:
        try:
            json.loads((ROOT / path).read_text())
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            errors.append(f"invalid JSON: {path}: {error}")
    for path in jsonl_files:
        line_number = 0
        try:
            lines = (ROOT / path).read_text().splitlines()
            for line_number, line in enumerate(lines, 1):
                if line.strip():
                    json.loads(line)
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            errors.append(f"invalid JSONL: {path}:{line_number}: {error}")

    checksum_file = ROOT / "manifests" / "starter-kit.sha256"
    checksum_lines = checksum_file.read_text().splitlines()
    for line in checksum_lines:
        expected, relative = line.split(maxsplit=1)
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"checksummed starter file missing: {relative}")
        elif sha256(path) != expected:
            errors.append(f"starter checksum mismatch: {relative}")

    scanned_bytes = 0
    for relative in tracked:
        path = ROOT / relative
        if not path.is_file() or path.stat().st_size > 5 * 1024 * 1024:
            continue
        data = path.read_bytes()
        scanned_bytes += len(data)
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(data):
                errors.append(f"possible {label} in tracked file: {relative}")

    result = {
        "status": "pass" if not errors else "fail",
        "tracked_files": len(tracked),
        "tracked_bytes": sum(
            (ROOT / path).stat().st_size
            for path in tracked
            if (ROOT / path).is_file()
        ),
        "json_files_checked": len(json_files),
        "jsonl_files_checked": len(jsonl_files),
        "secret_scan_bytes": scanned_bytes,
        "starter_checksums_checked": len(checksum_lines),
        "errors": errors,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
