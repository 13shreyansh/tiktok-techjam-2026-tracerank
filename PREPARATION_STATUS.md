# Preparation status

Last verified: **2026-08-31 19:49 SGT**

The preparation phase completed before the official start. Post-start judged
work is now recorded separately in `experiments/STATUS.md` and
`docs/SOLUTION_REPORT.md`.

## Ready

- [x] Preserved the untouched 15,848-byte organizer starter archive and its
  SHA-256 checksum.
- [x] Re-downloaded the official Track 2 attachment after public launch on
  2026-08-28; it is byte-for-byte identical to the preserved archive.
- [x] Safely inspected and extracted all eight organizer archive entries.
- [x] Preserved official URLs, sizes, checksums, source timestamps, and known
  licence information.
- [x] Validated an ignored Python 3.9.6 virtual environment with NumPy 2.0.2.
- [x] Downloaded KuaiRand-Pure through the exact no-registration Zenodo path in
  the organizer README; the 47,432,272-byte archive matched its official MD5.
- [x] Safely extracted the dataset under ignored `data/` and preserved its
  embedded licence as a small text artifact.
- [x] Reproduced the unmodified Factorization Machine baseline successfully.
- [x] Generated and validated the organizer's example test CSV; the generated
  4.6 MB file remains ignored and is not a submission.
- [x] Reconciled the launched statement: the benchmark, deliverables, judging
  formula, published scores, and starter all specify `long_view`, `GAUC`, and
  `nDCG@5`; one stale Limits-table row still says otherwise.
- [x] Recorded the launched resource limits: 50 iterations and a six-hour
  wall-clock ceiling per benchmark run.
- [x] Audited the 31 August official FAQ: the supplied test rows are the final
  judged rows; Pure training is restricted to the standard 8–21 April log; and
  convergence parameters may be predeclared per run.
- [x] Checked the public Information Document, Devpost Resources/Updates/Rules,
  and the official Telegram channel for additional Track 2 material.
- [x] Rechecked the live signed-in Lark statement and Devpost on 2026-08-29;
  confirmed the per-benchmark-run cap wording, public-repository requirement,
  and 2026-09-01 12:00 PM SGT deadline without performing an external action.
- [x] Preserved pinned, unmodified snapshots of Karpathy autoresearch, AIDE,
  and FML-Bench with exact commits, URLs, checksums, and licence evidence.
- [x] Preserved the pinned OpenAI MLE-bench README and MIT licence. Its full
  archive transfer was incomplete and was quarantined rather than accepted.
- [x] Acquired and safely extracted the organizer-authorized KuaiRand-1K bonus
  archive. Its official MD5 and locally computed SHA-256 pass; the 4.3 GB data,
  archive, caches, models, and predictions remain ignored.
- [x] Preserved KuaiRand-1K's embedded CC BY-SA 4.0 text and the conflicting
  Zenodo CC BY 4.0 metadata without silently resolving the discrepancy.
- [x] Built a label-safe, memory-bounded 1K development cache and verified a
  local sparse-FM benchmark under 3.36 GB peak RSS.

## Reproduction result

The documented FM command succeeded on Apple M5 Pro CPU hardware. It loaded
`1,141,112` train, `124,909` validation, and `170,588` test rows and reported:

| Split | GAUC | nDCG@5 | Primary |
|---|---:|---:|---:|
| validation | 0.6671 | 0.5358 | 0.6015 |
| test | 0.6621 | 0.5286 | 0.5953 |

Elapsed time was 22.86 s and maximum resident set size was 796,508,160 bytes.
No GPU or LLM call was used. Full commands and output are in
`docs/BASELINE_REPRODUCTION.md`.

## Unresolved blockers

- The public statement's Limits table still says `click` with `NDCG@10 /
  Recall@50`. This is now a lone stale contradiction: the benchmark table,
  deliverables, judging formula, published baseline, and unchanged starter all
  specify `long_view` with `GAUC / nDCG@5`.
- KuaiRand-1k and KuaiRand-27k are called bonus benchmarks, but no bonus formula
  or point value is published.
- The checksum-verified KuaiRand-1K archive contains 4,371,868 basic video rows
  and 32 ID holes, while the project page reports 4,369,953 items. Published and
  observed counts are preserved separately.
- Track 2 publishes weights of 35/20/20/15/10 including Presentation, while the
  Devpost Rules describe four equally weighted Stage Two criteria and omit
  Presentation. No precedence rule is stated.
- The starter ZIP contains no licence or notice file. Its redistribution terms
  therefore remain unknown.
- Zenodo metadata reports `cc-by-4.0` for KuaiRand, while the downloaded archive
  embeds the full CC BY-SA 4.0 licence. This conflict is preserved, not resolved.
- Karpathy autoresearch's included workload requires one NVIDIA GPU (tested on
  H100), whereas the prepared machine is an Apple M5 Pro. Only the unmodified
  reference is ready; a compatible Track 2 adaptation has not been made.
- The OpenAI MLE-bench full archive did not finish downloading before start;
  only its pinned README and licence are verified. The partial transfer and
  extraction remain quarantined under ignored artifacts.

## Post-start disposition

- [x] Agent-driven validation experiments and feature/model improvements began
  only after 12:00 SGT. Run2 packaged a validation-verified mixed candidate at
  `0.6054008850`; Run82 froze the fully causal six-member candidate at
  `0.6055212247`; and Run83 selected the latter after a fixed two-of-three
  chronological-window audit. The mixed artifact remains fallback. See
  `docs/SOLUTION_REPORT.md` and `docs/RUN83_REPORT.md`.
- [x] A local test-format candidate was generated and passed a label-blind
  alignment checker for all 170,588 rows. The official FAQ confirms these exact
  rows are final judged rows; no upload occurred.
- [x] Run82 is quarantined from final submission because its historical loader
  materialized test outcomes. Run84 rebuilt six fresh members through the
  feature-only boundary and selected the clean consensus at validation primary
  `0.6053745200`; all artifact, slice, and alignment gates passed.
- [x] Cumulative attempt, compute, AI-role, token-snapshot, and intervention
  caveats are consolidated in `docs/RESOURCE_REPORT.md`.
- [x] A clean, separately generated public-release tree was rebuilt after the
  submission freeze, sanitized all detected local-path occurrences, passed its
  privacy scan, and passed `scripts/release_audit.py` after initialization as a
  fresh local Git repository. Its manifest records the exact source commit and
  hashes. It remains ignored and unpublished; see
  `docs/PUBLIC_RELEASE_PROTOCOL.md`.
- [x] Run-cap interpretation is narrowed and documented: report Pure Run2 at
  37 / 50, candidate-freezing Run82 at 5 / 50, selection-audit Run83 at 24 / 50,
  Run16 as 18 executed / 16 convergence-eligible, Run84 as 8 / 50 including
  one disclosed duplicate, Run85 as 1 / 50, Run86 as 2 / 50 with one disclosed
  device-construction failure, Run87 as 1 / 50, Run88 as 2 / 50, Run89 as
  1 / 50, Run90 as 1 / 50, Run91 as 1 / 50, Run92 as 1 / 50, Run93 as
  8 / 50 with no completed consensus or candidate, and the full 344-execution
  research total, because run boundaries remain undefined even though the
  official cap is expressly per run.
- [x] Run85 tested a separately declared causal strict-skip history channel.
  Its first paired early-shadow attempt improved primary by only
  `0.0001149774`, below the frozen `0.0005` gate, and regressed the
  high-activity slice by `0.0008892577`. The family closed after one counted
  execution without tuning; Run84 remains the protected Pure candidate.
- [x] Run86 tested task-protected shared/private experts with training-only
  click auxiliary supervision. The exact retry improved early-shadow primary
  by only `0.0001055002`, below the fixed `0.0005` gate; the family closed after
  two counted executions, including one disclosed pre-model MPS-sandbox failure.
- [x] Run87 tested a chronological cross-fit LambdaMART residual. Its meta
  window improved `0.0042750588`, but the untouched target fell
  `0.0028399230`, the forward window fell `0.0019162860`, and every declared
  activity/date slice regressed. The family closed after one execution without
  tree, coefficient, feature, window, or seed tuning; Run84 remains protected.
- [x] Run88 tested majority-pairwise list aggregation without training or
  tunable weights. Early validation/forward changed `-0.0001498512` /
  `-0.0000245488`; middle changed `-0.0000461638` / `+0.0001318523`. Two
  failures made two-of-three impossible, so it stopped before late or official
  application. The initial future-rounded campaign timestamp is disclosed and
  its raw ledger offsets remain preserved.
- [x] Run89 tested one causal self-attention encoder over the ordered positive
  history. Validation and forward primary fell `0.1056606174` and
  `0.0789712071`; every fixed slice regressed. It closed after one attempt with
  no scaling, normalization, layer, head, width, seed, window, or blend rescue.
- [x] Run90 preserved the selected 20-event positive-history profile and added
  a separate last-five profile. Early validation improved `0.0005576015`, but
  forward primary slipped `0.0000094175` and high-activity primary fell
  `0.0012083505`, beyond the frozen slice floor. It closed after one attempt
  without length, capacity, seed, window, or blend tuning.
- [x] Run91 kept the selected long-view path and added a separately attended
  history of earlier likes, follows, comments, and forwards. Forward primary
  improved `0.0004534721`, but validation primary fell `0.0002588034` and
  high-activity primary fell `0.0012313562`. It closed after one attempt
  without changing event membership, history length, seed, window, or blend.
- [x] Run92 preserved the soft positive-history profile and added the single
  candidate-best-matching history vector. Validation primary fell
  `0.0006055236`, forward primary fell `0.0001223087`, and medium/high activity
  plus late dates failed their floors. It closed after one attempt without
  top-k, temperature, seed, window, or blend tuning.
- [x] Run93 began a predeclared causal seed-saturation audit. One automatic-
  device construction failed before model execution and seven exact MPS
  subprocesses succeeded. The user then froze model search for submission
  before any declared consensus was complete, so the run closed without a
  score, candidate, official build, or change to Run84.
- [x] Run 16 completed a separate KuaiRand-1K bonus campaign. Its current
  validation candidate is the shadow-qualified content FM at `0.6537467530`;
  no public-test or hidden-test label was evaluated. A 4,132,081-row
  test-format CSV passed a label-blind alignment check, but no 1K-specific
  organizer checker or submission route is published. See `docs/RUN16_REPORT.md`.
- [x] A literal convergence audit found that Run 16 should have stopped at
  attempt 16. Attempts 17-18 are disclosed, excluded post-convergence, and
  cannot change the selected attempt-13 candidate; the campaign is hard-locked.
- [x] A live 20:11 SGT source re-read confirmed the literal per-run wording.
  Run 17 therefore predeclared a separate DeepFM architecture family while
  retaining cumulative accounting. Its first shadow attempt regressed by
  0.009546 validation and 0.010591 forward, so the family closed without tuning.
- [x] The judge-facing README, release audit, and three-minute demo storyboard
  are prepared locally. A public Devpost refresh at 18:35 SGT exposed no new
  Track 2 attachment or announcement.
- [x] A separate sanitized public repository was created and its audited
  release was authorized for publication on 2026-08-31. The private canonical
  repository was not made public.
- [ ] No Devpost final submission, organizer contact, registration change, or
  final-test output upload has been performed.
