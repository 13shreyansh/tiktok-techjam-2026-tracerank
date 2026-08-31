# Judge quickstart

This guide separates checks that work in a clean public clone from checks that
require the ignored datasets, checkpoints, and predictions on the development
machine. It is intentionally explicit about what each command does and does not
prove.

## 1. Audit a clean clone — no dataset or environment required

From the repository root, run:

```bash
python3 scripts/release_audit.py
```

Expected final field:

```json
"status": "pass"
```

This standard-library check confirms that required reports and manifests are
tracked, all committed JSON and JSONL parse, all eight starter-kit checksums
match, no dataset/output/cache path or file over 10 MiB is tracked, and no
common credential format is detected. It does **not** recompute model scores or
prove that ignored checkpoints exist.

## 2. Inspect the decision evidence — about five minutes

1. Start with [`SOLUTION_REPORT.md`](SOLUTION_REPORT.md) for the selected Pure
   model, exact scores, and caveats.
2. Open [`RUN2_REPORT.md`](RUN2_REPORT.md) for the candidate-producing campaign,
   reconstruction command, convergence evidence, and resource use.
3. Inspect [`../experiments/run2/ledger.jsonl`](../experiments/run2/ledger.jsonl)
   for immutable commands, return codes, metrics, time, memory, and source
   hashes for all 37 counted attempts.
4. Open [`RUN16_REPORT.md`](RUN16_REPORT.md) and
   [`../experiments/run16/ledger.jsonl`](../experiments/run16/ledger.jsonl) for
   the separate KuaiRand-1K bonus campaign, including the two disclosed and
   excluded post-convergence executions.
5. Compare the clean protected hashes in
   [`../manifests/run84-candidate-artifacts.json`](../manifests/run84-candidate-artifacts.json)
   and
   [`../manifests/kuairand-1k-candidate-artifacts.json`](../manifests/kuairand-1k-candidate-artifacts.json).

The diagrams in [`figures/tracerank-system.svg`](figures/tracerank-system.svg)
and [`figures/results-summary.svg`](figures/results-summary.svg) summarize the
same evidence without replacing it.

## 3. Reproduce the untouched organizer baseline

Python 3.9 was used for the verified development run. The acquisition script
downloads the organizer-authorized KuaiRand-Pure archive and checks its hash
before extraction.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
./scripts/acquire_kuairand_pure.sh
cd organizer/kuairand-starter-kit
/usr/bin/time -l ../../.venv/bin/python baseline.py \
  --model fm \
  --data_dir ../../data/KuaiRand-Pure/data
```

The expected organizer validation primary is `0.6016`. Hardware-dependent
runtime and memory may differ. A run is reproduced only if this command
succeeds and its observed score is recorded; the committed report is not a
substitute for executing it.

## 4. Verify protected artifacts when they are available

Large models, predictions, datasets, and CSVs are deliberately not committed.
On the development machine—or after those files are supplied through the
organizer's eventual artifact route—run:

```bash
.venv/bin/python scripts/verify_run84_candidate.py
.venv/bin/python scripts/verify_kuairand_1k_artifacts.py
.venv/bin/python scripts/final_readiness.py
```

The final command additionally runs the label-blind Pure and 1K alignment
passes, experiment-accounting totals, and
convergence locks. It must finish with:

```json
"status": "local_ready_external_actions_pending"
```

The selected Pure CSV has 170,588 data rows. The 1K candidate CSV has 4,132,081
rows, but its schema remains locally derived because no 1K-specific organizer
checker or delivery route has been published.

## 5. Claims deliberately not made

- The reported numbers are validation results, not final-test scores.
- The selected clean Pure candidate has not read or evaluated final-test
  outcomes and has not been submitted externally.
- The 1K result is not compared with an organizer baseline because none is
  published.
- Successful release auditing does not prove model reproduction; it proves the
  integrity and safety of the committed evidence package.
- No public repository, Devpost project, video, upload, or final submission is
  created by any command in this guide.
