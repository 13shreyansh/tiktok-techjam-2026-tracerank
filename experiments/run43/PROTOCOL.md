# Run 43 protocol: repeat-affinity seed consensus

Started: **2026-08-30 21:26 SGT**.

## Independent question

Can an equal within-user percentile-rank ensemble of three independently seeded
copies of the confirmed full-density repeat-affinity model reduce seed-specific
ordering error and beat the best protected single checkpoint without weakening
chronological transfer or robustness slices?

## Frozen candidate

- Architecture, full-training cache, causal repeat-affinity fields, rank 8,
  BCE objective, learning rate `0.001`, epochs/patience, batching, evaluator,
  and all split/slice definitions are exactly the confirmed Runs 38-39 design.
- Members are fixed to seeds 2027, 2028, and 2029 before any Run 43 ensemble
  score. Convert each member independently to deterministic within-user
  percentile ranks and average them 1/3 each.
- Do not search raw-score aggregation, weights, member subsets, extra seeds,
  or activity-specific routing.
- The official prediction archives already exist and have matching cache,
  split, length, and command provenance. They remain locked until the shadow
  gate passes.

## Shadow procedure and gates

1. Train missing seed-2028 and seed-2029 copies on `shadow_early`, preserving
   the existing seed-2027 Run 38 member. Then score exactly one fixed ensemble.
2. Continue only if ensemble validation and forward primary each improve
   `>= +0.0003` over the seed-2027 repeat-affinity parent and every fixed slice
   is `>= -0.0005`.
3. If early passes, repeat the same missing seeds and fixed ensemble on middle
   and late shadows. At least two of three shadows must pass; no aggregate may
   fall below `-0.0005` and no slice below `-0.001`.
4. Only then evaluate the fixed three existing official prediction archives.
   Promote only if primary improves `>= +0.0003` over the protected seed-2029
   checkpoint and every fixed official slice is `>= -0.0005`.
5. Stop at family failure, declared convergence, 50 counted attempts, or six
   hours. Closing Run 43 does not stop the overall 72-hour campaign.

All scores remain deterministic development-sample evidence, not full
benchmark, hidden test, leaderboard, or submission results. Public-test labels
and all external actions remain locked.
