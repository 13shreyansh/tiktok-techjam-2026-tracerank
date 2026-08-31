# Run 55 protocol: protected-parent meta-consensus

Started: **2026-08-31 07:17:37 SGT**.

## Independent question

Does a fixed equal within-user rank consensus of protected Run49 and Run52
reduce architecture-specific ordering error beyond Run52 alone?

## Frozen candidate and gates

- Exactly two parent votes, ordered Run49 then Run52, each re-ranked within
  user and averaged 50/50. No raw averaging, weight, subset, duplication,
  routing, calibration, training, or member-level recombination.
- Shadows use Run49's four-member consensus and the matching Run52 rank-32
  seed-2027 prediction. Official uses the protected Run49 and Run52 consensus
  archives.
- Score early first. Continue only if validation and forward primary each gain
  `>= +0.00025` over the exact Run52 shadow parent, no component metric falls
  below `-0.0005`, and no fixed slice falls below `-0.001`.
- A pass scores middle then late. At least two of three windows must meet the
  same validation-and-forward gain; no aggregate below `-0.0005` and no slice
  below `-0.001`.
- Only then score exactly one official meta-consensus. Promote over Run52 only
  if primary gains `>= +0.0003` and every official slice is `>= -0.0005`.
- Stop at gate failure, convergence, 50 attempts, or six hours. Closing Run55
  does not stop the 72-hour campaign.

All scores are deterministic 1/32 development-sample evidence, not the full
benchmark, hidden test, submission, or leaderboard. Public-test labels and
external actions remain locked.
