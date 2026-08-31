# Run88 decision journal

## 2026-08-31 18:26 SGT — family frozen

- Reject rescue tuning of Run87 after its independent temporal reversal.
- Freeze one parameter-free majority-pairwise aggregation rule on the existing
  causal seed predictions.
- Require `+0.0002` on both validation and forward in two of three chronological
  windows, with component and subgroup floors, before official application.
- No alternative vote rule, tie handling, threshold, weight, subset, member,
  seed, or calibration may be tried after scores are observed.
- Run84 remains protected and final-test outcomes remain locked.

## 2026-08-31 18:26 SGT — implementation verification passed

- Ten targeted tests and the complete 102-test suite passed; both edited Python
  files compiled and `git diff --check` passed.
- Tests cover majority suppression of one reversed outlier, isolation between
  users, singleton lists, and fail-closed row alignment.
- The first CLI-help check omitted the repository's local `libomp` runtime and
  failed while importing LightGBM; it produced no score or output. The corrected
  environment check exposed the frozen `user_copeland_rank` mode.
- Commit the exact implementation and protocol before the first counted score.

## 2026-08-31 18:28 SGT — two failures close the family

- Attempt 1, early window: validation primary changed `-0.0001498512` and
  forward primary `-0.0000245488`. Both components declined on validation;
  every slice except medium activity declined. This is a gate failure.
- Attempt 2, middle window: validation primary changed `-0.0000461638`; forward
  improved only `+0.0001318523`, below the fixed `+0.0002` gate. High activity
  regressed `-0.0004477315`. This is a second gate failure.
- Two passing windows out of three are now impossible. Stop without the late
  window, official validation, alternative vote rule, tie-break change, or any
  tuning. Run84 remains protected.
- Both executions succeeded, loaded no official-test outcomes, and totaled
  `23.851929` subprocess seconds; maximum peak RSS was `2,199,683,072` bytes.

## Timestamp incident

- The initial state and draft protocol used a manually rounded future start of
  `18:30`, while authoritative commit time was `18:26:25` and launches began at
  `18:26:45`. The wrapper therefore recorded negative campaign offsets.
- Preserve both raw ledger records unchanged. Correct the state/protocol to the
  commit time and disclose the incident; it does not affect scores, attempt
  counts, subprocess durations, label boundaries, or the close decision.
