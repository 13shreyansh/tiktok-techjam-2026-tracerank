# Run 45 protocol: causal user-topic affinity

Started: **2026-08-30 23:21 SGT**.

## Independent question

Do prior-only user/current-primary-tag exposure count and long-view rate add a
generalizable topic-interest signal beyond exact video/creator repeat affinity?

## Frozen candidate

- Parent architecture and data are the full-density Run 38/39 repeat-affinity
  sparse FM: rank 8, BCE, learning rate `0.001`, epochs/patience, batching,
  evaluator, splits, and slices unchanged.
- Add exactly two categorical buckets: prior user/current-primary-tag count
  (`floor(log2(count+1))`, capped at 15) and beta-smoothed long-view rate in the
  existing 21-bucket scheme.
- State includes only earlier timestamps through each training cutoff;
  same-timestamp rows share the same prior and validation/forward state is
  frozen. Use only the primary tag. No feature, prior, bucket, capacity,
  objective, or optimizer variation is allowed inside Run 45.

## Procedure and gates

1. Build and hash the early feature archive, then evaluate seed 2027 against
   the exact Run 38 early parent. Continue only if validation and forward each
   gain `>= +0.0005` and every slice is `>= -0.001`.
2. If early passes, repeat unchanged on middle and late. At least two of three
   windows must pass the same aggregate gate; no aggregate may fall below
   `-0.0005` and no slice below `-0.001`.
3. Only then build official state and evaluate fixed seeds 2027, 2028, 2029.
   Require paired mean gain `>= +0.0005`, every seed gain `>= +0.0003`, and
   every official slice `>= -0.0005` versus its exact repeat parent.
4. If the seed gate passes, compute exactly one equal within-user percentile-
   rank consensus of the three tag-affinity seeds. Promote only if it gains
   `>= +0.0003` over protected Run 43 and every fixed slice is `>= -0.0005`.
5. Stop at family failure, declared convergence, 50 counted model attempts, or
   six hours including preparation. Closing Run 45 does not stop the overall
   72-hour campaign.

All scores remain deterministic development-sample evidence, not a full
benchmark, hidden-test, submission, or leaderboard result. Public-test labels
and all external actions remain locked.
