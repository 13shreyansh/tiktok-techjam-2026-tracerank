# Run 47 protocol: causal high-activity topic specialist

Started: **2026-08-30 23:56 SGT**.

## Independent question

Can a fixed training-activity route capture topic-affinity gains for users with
enough history while leaving the protected consensus unchanged for others?

## Frozen candidate

- Activity is each user's row count in the same fixed evaluation-sampled
  training reference used by robustness slices. The cutoff is its upper
  tertile (`quantile 2/3`) among positive counts.
- Users strictly above the cutoff receive the equal four-member rank consensus
  from Run 46. Every other user receives the exact Run 43 three-member rank
  consensus. The same training cutoff routes validation and forward rows.
- No threshold, quantile, soft gate, weight, member, aggregation, feature,
  model, or seed variation is allowed.

## Procedure and gates

1. Evaluate the fixed early route using existing archives. Continue only if
   validation and forward primary each improve `>= +0.0003` over Run 43, no
   fixed slice falls below `-0.0003`, and non-routed cold/medium slices are
   prediction-identical to their parent scores.
2. If early passes, prepare/train the unchanged topic seed-2027 member for
   middle and late, then test the identical route. At least two of three
   windows must pass; no aggregate may fall below `-0.0005` and no slice below
   `-0.001`.
3. Only then prepare official topic state and confirm topic seeds 2027-2029 as
   declared in Run 46. Evaluate the fixed official route with topic seed 2027.
   Promote only if primary gains `>= +0.0003` over Run 43 and every official
   slice is `>= -0.0005`.
4. Stop at failure, convergence, 50 counted attempts, or six elapsed hours
   including preparation. Closing Run 47 does not stop the 72-hour campaign.

All metrics are fixed development-sample evidence, not full-benchmark,
hidden-test, submission, or leaderboard results. Public-test labels and all
external actions remain locked.
