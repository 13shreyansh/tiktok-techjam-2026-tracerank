# Run 64 protocol: two-to-one protected capacity shrinkage

Started: **2026-08-31 08:34:00 SGT**.

## Independent question

Does a fixed one-third rank-16 diversity contribution improve protected rank 32
without the high-activity instability of equal group weighting?

## Frozen candidate and gates

- Aggregate exactly three equal within-user percentile-rank votes: the fixed
  three-seed rank-16 consensus once and the matching protected rank-32
  prediction twice.
- The repeated rank-32 input is an explicit `2:1` capacity weight, not an
  additional trained model.
- Shadow input hashes are exactly those recorded in Run61's protocol.
- No other ratio, duplicate count, member, route, threshold, subset,
  calibration, raw-logit, rank, seed, or aggregation variation.
- Early must improve validation and forward primary each `>= +0.00025`, with
  no component below `-0.0005` and no fixed slice below `-0.001` versus exact
  Run52.
- A pass scores middle and late unchanged; at least two of three windows must
  meet the same gain and safety guards.
- Only then create one official three-seed rank-16 consensus from the fixed
  previously trained members and aggregate it once with two identical votes of
  the protected Run52 three-seed rank-32 consensus.
- Promote only at official primary `>= +0.0003` and every official slice
  `>= -0.0005` versus Run52.
- Stop at any gate or artifact failure, convergence, 50 attempts, or six hours.
  Closing Run64 does not stop the 72-hour campaign.

All scores remain deterministic 1/32 development-sample evidence, not the full
benchmark, hidden test, submission, or leaderboard. Public-test labels and
external actions remain locked.
