#!/usr/bin/env python3
"""Build a sanitized, non-publishing copy of the tracked repository.

The canonical experiment ledgers retain exact local commands. This builder
copies tracked files into a new ignored directory and replaces only local
machine paths in UTF-8 text files. It never pushes, publishes, or changes the
source repository.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SAFE_OUTPUT_PARENT = ROOT / "artifacts"
TEXT_SUFFIXES = {
    ".cfg",
    ".csv",
    ".ini",
    ".json",
    ".jsonl",
    ".md",
    ".py",
    ".sh",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}
PRIVATE_PATTERNS = {
    "absolute macOS user path": re.compile(rb"/Users/[A-Za-z0-9._-]+/"),
    "authenticated Lark URL": re.compile(rb"https?://[^\s\"']*(?:larksuite\.com|feishu\.cn)"),
    "personal repository URL": re.compile(rb"github\.com/13shreyansh", re.I),
    "OpenAI-style key": re.compile(rb"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "GitHub token": re.compile(rb"\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}\b"),
    "Google API key": re.compile(rb"\bAIza[0-9A-Za-z_-]{30,}\b"),
    "AWS access key": re.compile(rb"\bAKIA[0-9A-Z]{16}\b"),
}
PUBLIC_REPOSITORY_URL = (
    b"https://github.com/13shreyansh/tiktok-techjam-2026-tracerank"
)
PUBLIC_VENDOR_ALLOWLIST = {
    "vendor/karpathy-autoresearch/README.md",
    "vendor/karpathy-autoresearch/program.md",
    "vendor/openai-mle-bench-reference/LICENSE",
    "vendor/openai-mle-bench-reference/README.md",
    "vendor/qrzou-fml-bench/LICENSE",
    "vendor/qrzou-fml-bench/README.md",
    "vendor/wecoai-aideml/LICENSE",
    "vendor/wecoai-aideml/README.md",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_output(*args: str) -> bytes:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True
    ).stdout


def tracked_files() -> list[str]:
    return [
        item.decode()
        for item in git_output("ls-files", "-z").split(b"\0")
        if item
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="New directory below artifacts/; it must not already exist.",
    )
    parser.add_argument(
        "--allow-dirty",
        action="store_true",
        help="Permit a test build from a dirty worktree; recorded in manifest.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output = args.output_dir.expanduser().resolve()
    safe_parent = SAFE_OUTPUT_PARENT.resolve()
    if output.parent != safe_parent:
        raise SystemExit(f"output must be a direct child of {safe_parent}")
    if output.exists():
        raise SystemExit(f"refusing to overwrite existing output: {output}")

    dirty = bool(git_output("status", "--porcelain"))
    if dirty and not args.allow_dirty:
        raise SystemExit("worktree is dirty; commit and retry or use --allow-dirty")

    source_commit = git_output("rev-parse", "HEAD").decode().strip()
    source_root = str(ROOT)
    user_home = str(ROOT.parents[4])
    replacements = (
        (source_root, "${REPO_ROOT}"),
        (user_home, "${USER_HOME}"),
    )

    all_tracked = tracked_files()
    selected = [
        path
        for path in all_tracked
        if not path.startswith("vendor/") or path in PUBLIC_VENDOR_ALLOWLIST
    ]
    excluded_vendor = sorted(set(all_tracked) - set(selected))

    output.mkdir(parents=True)
    files: list[dict[str, object]] = []
    replacement_total = 0
    for relative in selected:
        source = ROOT / relative
        target = output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.is_symlink():
            target.symlink_to(source.readlink())
            files.append(
                {
                    "path": relative,
                    "kind": "symlink",
                    "target": str(source.readlink()),
                    "replacements": 0,
                }
            )
            continue

        original_hash = sha256(source)
        replacement_count = 0
        if source.suffix.lower() in TEXT_SUFFIXES:
            text = source.read_text(encoding="utf-8")
            for old, new in replacements:
                occurrences = text.count(old)
                replacement_count += occurrences
                text = text.replace(old, new)
            target.write_text(text, encoding="utf-8")
            shutil.copymode(source, target)
        else:
            shutil.copy2(source, target)
        replacement_total += replacement_count
        files.append(
            {
                "path": relative,
                "kind": "file",
                "source_sha256": original_hash,
                "public_sha256": sha256(target),
                "replacements": replacement_count,
            }
        )

    findings: list[str] = []
    for entry in files:
        if entry["kind"] != "file":
            continue
        path = output / str(entry["path"])
        if path.stat().st_size > 10 * 1024 * 1024:
            findings.append(f"oversized file: {entry['path']}")
            continue
        data = path.read_bytes().replace(
            PUBLIC_REPOSITORY_URL, b"${PUBLIC_REPOSITORY_URL}"
        )
        for label, pattern in PRIVATE_PATTERNS.items():
            if pattern.search(data):
                findings.append(f"possible {label}: {entry['path']}")

    manifest = {
        "schema_version": 1,
        "source_commit": source_commit,
        "source_worktree_dirty": dirty,
        "source_tracked_files": len(all_tracked),
        "tracked_files_copied": len(files),
        "excluded_vendor_files": excluded_vendor,
        "path_replacements": replacement_total,
        "status": "pass" if not findings else "fail",
        "findings": findings,
        "files": files,
    }
    manifest_path = output / "PUBLIC_RELEASE_MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    summary = {
        key: value
        for key, value in manifest.items()
        if key not in {"files", "excluded_vendor_files"}
    }
    summary["excluded_vendor_files"] = len(excluded_vendor)
    summary["manifest_sha256"] = sha256(manifest_path)
    print(json.dumps(summary, indent=2, sort_keys=True))
    raise SystemExit(1 if findings else 0)


if __name__ == "__main__":
    main()
