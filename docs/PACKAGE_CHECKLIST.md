# Local package checklist

## Ready and verified

- [x] Protected validation result and complete six-member reconstruction.
- [x] Six model checkpoints and six prediction archives with SHA-256 hashes.
- [x] Final ensemble prediction archive and 170,588-row CSV with hashes.
- [x] Organizer format/alignment checker passed again on 2026-08-31 for all
  170,588 final-test rows.
- [x] Official dataset, category, caption, and starter provenance preserved.
- [x] Exact commands, failures, metrics, code/evaluator hashes, time, and memory
  retained across all campaign ledgers.
- [x] No tracked dataset, checkpoint, prediction archive, CSV, cache, or secret.
- [x] Current solution, resource report, caveats, and narrative draft prepared.
- [x] Live 2026-08-29 rules audit confirmed the 50-iteration and six-hour limits
  are phrased per benchmark run; reporting policy preserves both Run 2 and
  cumulative totals.
- [x] Devpost deadline confirmed as 2026-09-01 12:00 PM SGT; public repository
  and working-project access requirements rechecked.
- [x] KuaiRand-1K seed-2028 checkpoint reconstructed 2,524,980 saved validation
  predictions bit-for-bit and generated a 4,132,081-row label-blind test-format
  CSV with recorded hashes and receipt.
- [x] KuaiRand-1K candidate inputs reconstructed from the exact candidate code;
  all ten stable cache arrays matched byte-for-byte and have per-file hashes.
- [x] Fail-closed local readiness command checks the tracked release, both
  protected artifact families, both CSV alignments, accounting totals,
  convergence locks, and unresolved external-action placeholders.
- [x] Public-ready README and time-coded three-minute demo storyboard prepared
  locally without recording, publishing, or changing repository visibility.
- [x] Source-controlled system and measured-results SVGs prepared for the demo;
  both clearly separate validation evidence from unread final-test outcomes.
- [x] Judge quickstart separates clean-clone integrity checks from full
  data/artifact reproduction and states what each command cannot prove.
- [x] Deterministic public-export builder preserves canonical ledgers privately,
  sanitizes machine-specific paths in a separate ignored tree, records per-file
  hashes, retains only provenance-essential upstream reference files, and
  performs a release privacy scan without publishing anything.
- [x] Devpost-ready title, tagline, description, result table, technical stack,
  resource disclosure, limitations, final-link placeholders, and action gates
  prepared locally in `docs/DEVPOST_PACKET.md`.
- [x] Tracked release audit passes: 1,057 files, 200 JSON files, 117 JSONL files,
  all eight starter checksums, no tracked data/output/cache path, no file over
  10 MiB, and no detected common credential format.

Verify ignored artifacts locally:

```text
.venv/bin/python scripts/verify_candidate_artifacts.py
.venv/bin/python scripts/verify_kuairand_1k_artifacts.py
```

Run the complete fail-closed local readiness gate:

```text
.venv/bin/python scripts/final_readiness.py
```

Verify the tracked release independently of ignored artifacts:

```text
.venv/bin/python scripts/release_audit.py
```

Verify the CSV using the organizer code:

```text
.venv/bin/python organizer/kuairand-starter-kit/submit.py \
  outputs/submissions/run84-clean-six-causal-user-rank-test.csv \
  --data_dir data/KuaiRand-Pure/data --split test --check
```

## Blocked or requires explicit user action

- [ ] At submission, report Pure Run2 as 37 / 50 attempts and 3,172.35 seconds,
  Run82 as 5 / 50, Run83 as 24 / 50, Run84 as 8 / 50, Run85 as 1 / 50,
  Run86 as 2 / 50, Run87 as 1 / 50, Run88 as 2 / 50, Run89 as 1 / 50, Run90
  as 1 / 50, Run91 as 1 / 50, Run92 as 1 / 50, Run93 as 8 / 50 with no
  completed consensus or candidate, Run16 as 18 executed / 16
  convergence-eligible, and 344
  cumulative research executions. Preserve every per-campaign ledger and do
  not omit failed or post-convergence attempts.
- [x] Confirmed from the signed-in Track 2 deliverables that the required token
  figure is the combined `input + output` total; a separate split is not asked
  for, so the exposed combined goal counter is the truthful value to report.
- [x] Paginate the Codex task history through `hasMore=false` at 20:43 SGT:
  52 turns contain 26 user-authored messages; separately report six unique
  logged campaign-control events. Refresh again if another user message arrives.
- [x] Confirmed from the public FAQ that the supplied dated test rows are the
  final judged rows and there is no separate hidden dataset. Their outcomes
  remain unread and prohibited from development.
- [ ] Obtain the organizer's KuaiRand-1K-specific format checker or confirm its
  submission schema; the local package currently derives the Pure schema from
  the statement that both benchmarks use the same task.
- [ ] Decide how to handle the official metric/limits and judging-weight
  contradictions without claiming organizer clarification.
- [ ] Provide a public three-minute video unless Devpost is changed: Track 2
  calls it optional/recommended, but the Devpost overview calls it required.
- [x] Created a separate public sanitized repository after explicit user
  authorization; the private canonical repository remains private.
- [x] Received explicit action-time authorization to publish the audited
  sanitized release to the public repository.
- [ ] Any Devpost upload, final submission, organizer contact, or registration
  change requires explicit user authorization at that stage.
