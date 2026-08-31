# Run 51 protocol: six-member seed-and-capacity consensus

Started: **2026-08-31 04:11 SGT**.

## Independent question

Can equal within-user rank aggregation of the fixed union of three confirmed
rank-8 seeds and three confirmed rank-16 seeds reduce both seed and capacity
variance beyond the protected Run49 four-member consensus?

## Frozen candidate

- Rank-8 repeat-affinity seeds 2027, 2028, and 2029 from Runs 38/39/43.
- Rank-16 repeat-affinity seeds 2027, 2028, and 2029 from Runs 42/49/50.
- Convert each member independently to deterministic within-user percentile
  ranks and average exactly `1/6` in the fixed order above.
- No subset, duplicate, raw/logit aggregation, family weight, member weight,
  calibration, route, feature, model, seed, or parameter variation is allowed.

## Procedure and gates

1. Score the fixed early six-member consensus. Continue only if validation and
   forward primary each improve `>= +0.00025` over Run49 and every fixed slice
   is `>= -0.0005`.
2. If early passes, score the same middle and late unions. At least two of
   three windows must improve validation and forward by `>= +0.00025`; no
   aggregate may be below `-0.0003` and no slice below `-0.0008`.
3. Only then score exactly one official six-member consensus. Promote over
   Run49 only if primary improves `>= +0.0003` and every fixed official slice
   is `>= -0.0005`.
4. Stop at gate failure, convergence, 50 counted attempts, or six elapsed
   hours. Closing Run 51 does not stop the 72-hour campaign.

All scores are fixed development-sample evidence, not full-benchmark,
hidden-test, submission, or leaderboard results. Public-test labels and all
external actions remain locked.
