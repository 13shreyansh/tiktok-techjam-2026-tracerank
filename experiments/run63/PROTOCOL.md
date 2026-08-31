# Run 63 protocol: tested exact high-activity fallback

Started: **2026-08-31 08:33:00 SGT**.

## Independent question

Can an exact protected fallback preserve Run61's capacity-diversity gain while
eliminating its high-activity reversal?

## Frozen candidate and gates

- Use `high_activity_last_member_only` with exactly two inputs: the equal
  rank-16/rank-32 capacity-group consensus first and matching protected Run52
  rank-32 prediction last.
- Only users strictly above the existing training-activity upper tertile use
  the final Run52 member; everyone else uses the first member alone.
- Early input SHA-256 values are
  `c621cddf7c46af11e5bc1f3841a018c15167d4a0dd9a56d878bd44bf281980e4`
  and `8d2392915731af585177bbb79287fc391629dea2fbce9f1faab0c965db911872`.
- No alternate threshold, route direction, member, subset, weight, duplication,
  calibration, raw-logit, rank, seed, or aggregation variation.
- Early must improve validation and forward primary each `>= +0.00025`, with
  no component below `-0.0005` and every fixed slice `>= -0.0005` versus exact
  Run52.
- A pass constructs the exact predeclared capacity-group base for middle and
  late, then applies the same route. At least two of three routed windows must
  meet the same gain and safety guards.
- Only then create the frozen three-seed rank-16 official consensus, give it
  one equal capacity-group vote with protected Run52, and apply the same exact
  fallback to protected Run52.
- Promote only at official primary `>= +0.0003` and every official slice
  `>= -0.0005` versus Run52.
- Stop at any gate or artifact failure, convergence, 50 attempts, or six hours.
  Closing Run63 does not stop the 72-hour campaign.

All scores remain deterministic 1/32 development-sample evidence, not the full
benchmark, hidden test, submission, or leaderboard. Public-test labels and
external actions remain locked.
