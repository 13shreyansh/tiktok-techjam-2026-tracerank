# Track 2 current solution report

Last verified: **2026-08-31 19:49 SGT**

## Outcome

The selected clean candidate is a six-member fully causal within-user rank
ensemble with saved-artifact validation **GAUC 0.6725210738**, **nDCG@5
0.5382279662**, and primary **0.6053745200**. The organizer's published FM
validation primary is 0.6016, so the measured validation gain is
`+0.0037745200`. It is not a final-test score and does not guarantee leaderboard
rank. Run84 rebuilt every member from scratch through a feature-only final-test
boundary after the 31 August FAQ clarification.

Each member is a neural factorization machine that scores an impression using
user, video, author, tags, tab, and duration, plus attention over the user's
last 20 positive long-view videos and their tags. Six independently seeded
causal-history members are converted to
percentile ranks within each user; the six ranks are averaged. The ensemble
therefore uses the workshop's central clue—recent viewing history affects the
next candidate—while aligning aggregation to user-grouped ranking metrics.

## Why this candidate is selected

- All six members are independent seeds, and rank aggregation reduced variance.
- Chronological history construction was audited after discovering 23,938
  within-user time reversals and 24,729 users split across file blocks.
- Candidate changes were screened on chronological shadow windows and
  low/medium/high-activity plus early/late-date slices.
- Run83 compared source-order and chronological histories at three fixed seeds
  across three chronological validation/forward windows. Causal history passed
  early and late, failed middle, crossed no catastrophic component or slice
  floor, and therefore met the frozen two-of-three selection rule.
- The label-blind organizer-format checker passed on 2026-08-31 for all
  170,588 rows.
- All six Run84 members and the consensus explicitly attest that official test
  outcomes were not loaded. The clean artifact passed its metric and robustness
  gates; the historical Run82 artifact remains quarantined.

## What was tested and learned

The organizer-prioritized families were all investigated: BPR, sampled
listwise and Lambda-style ranking losses; DIN and GRU sequence variants;
multi-action and auxiliary targets; censored watch time; causal aggregates;
Deep & Cross interactions; time drift; random-exposure validation; official
hierarchical categories; official captions; robust median-rank consensus; and
strictly causal repeated user-video memory.

The durable evidence is that simple positive long-view video/tag history and
multi-seed mean-rank consensus transfer better than extra capacity or auxiliary
signals. Several ideas improved one window while hurting the next or a user
segment. They were rejected rather than merged. Detailed evidence is in
`docs/RUN2_REPORT.md` through `docs/RUN15_REPORT.md`.

## Exact protected artifacts

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `outputs/predictions/run84-clean-six-causal-user-rank-final.npz` | 493,222 | `eb645924bcefc857283cbc5e819dc39b3caa041eeb12412023ba810db7764480` |
| `outputs/submissions/run84-clean-six-causal-user-rank-test.csv` | 4,646,704 | `35f5fcbd718c7cdc0be10db031dd12e06909b16fd3aa2a53b070b8f006118539` |

The CSV has one header plus 170,588 data rows. The feature-only checker
reported:

```text
PASS label-blind Pure alignment: 170,588 rows (split=test); outcomes not loaded or scored
```

No upload or submission has been performed. Large generated artifacts remain
ignored. Exact checkpoint/member hashes and reconstruction evidence are in
`manifests/run84-candidate-artifacts.json` and `docs/RUN84_REPORT.md`.

## Material caveats

- A single public-test audit was performed in original Run 1 on an earlier,
  already frozen model (0.597922 versus published 0.5946). It was not used to
  select later models, but it is now treated as a compliance incident rather
  than a harmless audit.
- Historical Pure loaders materialized test outcomes even when only predictions
  were requested. Run82 is therefore a validation reference only; Run84 is the
  clean selected candidate.
- The fallback mixed ensemble contains three members that predate the
  causal-history fix. They contain no validation-label leakage, but their
  training histories could include a later training event. Run82's fixed
  six-causal replacement reached primary `0.6055212247`, passed
  every declared activity/date slice guard, and improved GAUC while slightly
  reducing nDCG@5. Its primary gain over the fallback is only `+0.0001203396`.
  Run83 supplied independent chronological evidence for selecting it without
  reopening weights, seeds, members, or official scoring.
- Apple MPS can show small run-to-run numerical variation. Exact saved member
  predictions, not assumed reruns, define the protected artifact.
- Through closed Run93, all immutable ledgers contain 344 executions: 333
  succeeded and 11 failed. The ledger-derived subprocess total is `77,615.202`
  seconds.
  Run84 used eight executions, including one disclosed duplicate seed-2026
  execution caused by an orchestration polling race.
  Run85 used one successful attempt and closed at its first chronological gate.
  Run86 used one failed construction and one successful scored attempt, then
  closed below its first materiality gate.
  Run87 used one successful residual-ranking attempt and closed when a strong
  meta-window gain reversed on both independent target and forward windows.
  Run88 used two successful majority-pairwise aggregation attempts and stopped
  after two chronological transfer failures.
  Run89 used one successful self-attentive history attempt and closed after a
  catastrophic opening transfer failure.
  Run90 used one successful dual-timescale-history attempt and closed when its
  small early gain failed forward transfer and the high-activity slice floor.
  Run91 used one successful separate-engagement-history attempt and closed
  when its forward gain failed validation and the high-activity slice floor.
  Run92 used one successful hard target-match attempt and closed after
  validation, forward, and three slice floors failed.
  Run93 used seven successful seed-saturation subprocesses and one failed
  pre-model automatic-device execution. The user froze search for submission
  before the declared consensus was complete, so it produced no candidate.
  The largest prior measured peak RSS was
  `45,375,324,160` bytes.
  Every individual
  campaign remained below 50 attempts and six hours. Pure Run2 used 37 / 50
  attempts, Run82 used 5 / 50, Run83 used 24 / 50, Run84 used 8 / 50, and
  Run85 used 1 / 50, Run86 used 2 / 50, Run87 used 1 / 50, Run88 used 2 / 50,
  Run89 used 1 / 50, Run90 used 1 / 50, Run91 used 1 / 50, Run92 used
  1 / 50, and Run93 used 8 / 50; Run16's 18 executions
  include two disclosed,
  convergence-ineligible post-stop attempts. Restarted-run boundaries remain
  undefined, so candidate-producing counts and the cumulative total must both
  be disclosed. `docs/RESOURCE_REPORT.md` contains current ledger-derived
  totals and still requires live token/message refresh before submission.
- The official metric contradiction, judging-weight discrepancy, and starter
  licence gap remain unresolved in
  `PREPARATION_STATUS.md`.
