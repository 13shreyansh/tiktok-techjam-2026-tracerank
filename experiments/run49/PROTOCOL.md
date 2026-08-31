# Run 49 protocol: rank-diverse repeat consensus

Started: **2026-08-31 00:39 SGT**.

## Independent question

Does the independently positive rank-16 repeat-affinity ordering add robust
diversity to the protected three-seed rank-8 consensus?

## Frozen candidate

- Equal within-user percentile-rank mean of exactly four members in this order:
  repeat-affinity rank-8 seeds 2027, 2028, and 2029, then repeat-affinity
  rank-16 seed 2027.
- Each member receives exactly `1/4`. No raw/logit averaging, weight, subset,
  duplicate, alternate rank, seed substitution, calibration, route, or feature
  variation is allowed.
- The exact Run 43 three-member rank consensus is the parent.

## Procedure and gates

1. Score the four existing early archives once. Continue only if validation
   and forward primary each improve `>= +0.0003` over Run 43 and every fixed
   slice is `>= -0.0005`.
2. If early passes, train only the missing unchanged rank-16 seed-2027 member
   for middle and late, then score the same four-member consensus. At least two
   of three windows must pass; no aggregate may fall below `-0.0005` and no
   slice below `-0.001`.
3. Only then train the unchanged rank-16 seed-2027 official member and evaluate
   exactly one fixed four-member official consensus. Promote over Run 43 only
   if primary gains `>= +0.0003` and every official slice is `>= -0.0005`.
4. Stop at gate failure, convergence, 50 counted attempts, or six elapsed
   hours. Closing Run 49 does not stop the 72-hour campaign.

All metrics are fixed development-sample evidence, not full-benchmark,
hidden-test, submission, or leaderboard results. Public-test labels and all
external actions remain locked.
