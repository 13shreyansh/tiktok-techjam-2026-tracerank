# Run 62 protocol: high-activity safety route

Started: **2026-08-31 08:29:00 SGT**.

## Independent question

Can a training-activity-only fallback preserve Run61's capacity-diversity gain
without harming the high-activity users for whom it reversed?

## Frozen candidate and gates

- Use `high_activity_last_member` with exactly two inputs: the equal
  rank-16/rank-32 capacity-group consensus first and matching protected Run52
  rank-32 prediction last.
- The upper-tertile cutoff uses the existing training-activity definition;
  only users strictly above it receive the final Run52 member.
- Early input SHA-256 values are
  `c621cddf7c46af11e5bc1f3841a018c15167d4a0dd9a56d878bd44bf281980e4`
  and `8d2392915731af585177bbb79287fc391629dea2fbce9f1faab0c965db911872`.
- No alternate threshold, comparison, route direction, member, subset, weight,
  duplication, calibration, raw-logit, rank, seed, or aggregation variation.
- Early must improve validation and forward primary each `>= +0.00025`, with
  no component below `-0.0005` and every fixed slice `>= -0.0005` versus exact
  Run52.
- A pass constructs the exact predeclared capacity-group base for middle and
  late, then applies the same route. At least two of three routed windows must
  meet the same gain and safety guards.
- Only then create one official three-seed rank-16 consensus from fixed members
  with SHA-256 `c3507f1faa5eb0d8eaf068768eda478db76c3603b2f592cbd74ccce195207c66`,
  `b1e11232f1646d92a74692805c070e2136290906d27d852204bd2ebf91ce86f4`,
  and `42f5f5bd8f793c9d0d04d03b520283629e674126ce5864c4130c93d5af3af364`.
- Give that rank-16 consensus one equal group vote with the protected rank-32
  consensus SHA-256
  `12e4652ef8b3636936b6bc310b500d3ad11714cfa25e3a0775c1c8e5e9696b96`,
  then apply the same high-activity fallback to protected Run52.
- Promote only at official primary `>= +0.0003` and every official slice
  `>= -0.0005` versus Run52.
- Stop at any gate or artifact failure, convergence, 50 attempts, or six hours.
  Closing Run62 does not stop the 72-hour campaign.

All scores remain deterministic 1/32 development-sample evidence, not the full
benchmark, hidden test, submission, or leaderboard. Public-test labels and
external actions remain locked.
