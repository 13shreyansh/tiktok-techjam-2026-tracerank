# Public release protocol

The canonical private research branch intentionally preserves exact commands,
including the local machine path used by the experiment wrappers. Publishing
that branch directly would expose a personal username in historical ledgers.
Rewriting those append-only ledgers would weaken their provenance.

Build a separate, sanitized release tree instead:

```bash
.venv/bin/python scripts/build_public_release.py \
  --output-dir artifacts/public-release-YYYYMMDD-HHMM
```

The builder has no network or Git-push operation. It refuses to overwrite an
existing directory, accepts output only as a direct child of the ignored
`artifacts/` directory, and normally refuses a dirty source worktree. It copies
every project file, changes only local machine paths in UTF-8 text files, keeps
binary files unchanged, and writes `PUBLIC_RELEASE_MANIFEST.json` with the
source commit and source/public SHA-256 hashes. To keep the public repository
focused, complete upstream reference snapshots under `vendor/` are excluded;
only their pinned READMEs, licence evidence, and Karpathy's process brief are
retained. The manifest lists every excluded vendor path, while the canonical
private history and archive checksums preserve the acquisition evidence.

The generated tree fails its privacy gate if it contains an absolute macOS user
path, authenticated Lark/Feishu URL, personal repository URL, common credential
format, or file over 10 MiB. The manifest itself is part of the generated tree
and remains ignored locally.

Before any user-authorized public release:

1. Run `scripts/release_audit.py` on the canonical clean source.
2. Build a new sanitized tree without `--allow-dirty`.
3. Confirm the builder reports `status: pass` and `source_worktree_dirty: false`.
4. Review the generated README, disclosure, licences, and manifest manually.
5. Create a fresh public Git history from the sanitized tree; do not publish the
   canonical private history containing local absolute paths.
6. Perform the push, visibility change, and Devpost submission only after the
   user explicitly authorizes those external actions.

This protocol prepares a release but does not authorize or perform one.
