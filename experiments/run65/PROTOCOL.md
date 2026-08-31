# Run 65 protocol: midpoint high-activity shrinkage

Started: **2026-08-31 08:37:00 SGT**.

## Independent question

Can a fixed midpoint blend only for high-activity users preserve Run61's
forward diversity while keeping its unstable cohort inside the safety floor?

## Frozen candidate and gates

- Use `high_activity_equal_blend` with exactly two inputs: Run61 capacity-group
  consensus first and matching protected Run52 rank-32 prediction second.
- Users at or below the existing training-activity upper tertile use Run61
  alone. Users above it use the equal within-user-rank midpoint of Run61 and
  Run52.
- Early input SHA-256 values are
  `c621cddf7c46af11e5bc1f3841a018c15167d4a0dd9a56d878bd44bf281980e4`
  and `8d2392915731af585177bbb79287fc391629dea2fbce9f1faab0c965db911872`.
- No alternate blend, threshold, route, member, subset, calibration, raw-logit,
  rank, seed, or aggregation variation.
- Early must improve validation and forward primary each `>= +0.00025`, with
  no component below `-0.0005` and no fixed slice below `-0.001` versus exact
  Run52.
- A pass constructs the exact Run61 capacity-group base for middle and late,
  then applies the same midpoint route. At least two of three routed windows
  must meet the same gain and safety guards.
- Only then create the frozen three-seed rank-16 official consensus, give it
  one equal group vote with protected Run52, and apply the same midpoint blend
  above the official training-activity upper tertile.
- Promote only at official primary `>= +0.0003` and every official slice
  `>= -0.0005` versus Run52.
- Stop at any gate or artifact failure, convergence, 50 attempts, or six hours.
  Closing Run65 does not stop the 72-hour campaign.

All scores remain deterministic 1/32 development-sample evidence, not the full
benchmark, hidden test, submission, or leaderboard. Public-test labels and
external actions remain locked.
