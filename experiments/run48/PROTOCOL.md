# Run 48 protocol: causal multi-tag-supported primary affinity

Started: **2026-08-31 00:03 SGT**.

## Independent question

Does counting a user's prior occurrences of the candidate's primary tag across
all three historical tag positions produce a robust gain over the exact
repeat-affinity parent?

## Frozen candidate

- Parent is the exact Run 38/39 repeat-affinity sparse FM configuration.
- Add exactly two bounded categorical fields: prior user/current-primary-tag
  count and smoothed long-view rate. Historical matches may occur in any of the
  three source tag positions; duplicate tags within one row update once.
- Current candidate tag 2/tag 3, model capacity, rank (`8`), sampler, loss,
  optimizer, regularization, epochs, learning rate, batch size, stopping rule,
  and seed are unchanged. No bucket, prior, current-tag, weight, route,
  objective, or capacity variation is allowed.

## Procedure and gates

1. Build the causal early artifact, then train seed 2027 once. Continue only if
   validation and independent forward primary each improve `>= +0.0005` over
   the paired repeat parent and every fixed slice is `>= -0.001`.
2. If early passes, build and evaluate the identical seed-2027 candidate on
   middle and late shadows. At least two of three windows must pass the
   `+0.0005` gate; no aggregate may be below `-0.0005` and no slice below
   `-0.001`.
3. Only then build official state and train fixed seeds 2027, 2028, and 2029,
   each paired with its repeat-affinity parent. Require paired mean gain
   `>= +0.0005`, minimum seed gain `>= +0.0003`, every slice `>= -0.0005`, and
   candidate primary span `<= 0.002`.
4. If the seed gate passes, form exactly one equal within-user rank consensus
   of those three candidates. Promote over Run 43 only if primary gains
   `>= +0.0003` and every official slice is `>= -0.0005`.
5. Stop at gate failure, convergence, 50 counted attempts, or six elapsed
   hours including preprocessing. Closing Run 48 does not stop the 72-hour
   campaign.

All metrics are fixed development-sample evidence, not full-benchmark,
hidden-test, submission, or leaderboard results. Public-test labels and all
external actions remain locked.
