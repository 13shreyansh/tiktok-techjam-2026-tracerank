# Run 46 protocol: topic-diverse seed consensus

Started: **2026-08-30 23:54 SGT**.

## Independent question

Does one causal topic-affinity member add complementary ordering information to
the protected three-seed repeat-affinity rank consensus?

## Frozen candidate

- Equal within-user percentile-rank mean of exactly four members in this order:
  repeat seeds 2027, 2028, 2029, then topic-affinity seed 2027.
- Each member receives one equal `1/4` vote. No raw averaging, weights, subsets,
  member duplication, calibration, capacity change, or feature variation.
- Run 43's exact three-repeat-member rank consensus is the parent.

## Procedure and gates

1. Evaluate the four fixed early archives. Continue only if validation and
   forward primary each improve `>= +0.0003` over Run 43 and every fixed slice
   is `>= -0.0005`.
2. If early passes, prepare/train the unchanged topic member for middle and
   late and evaluate the same four-member consensus. At least two of three
   windows must pass; no aggregate may fall below `-0.0005` and no slice below
   `-0.001`.
3. Only then prepare official topic state and train fixed topic seeds 2027,
   2028, and 2029 to check that the topic effect is not seed-specific. Require
   no topic seed below `-0.0005` versus its repeat parent and score span
   `<= 0.002`.
4. Evaluate one official four-member consensus using the fixed topic seed 2027
   member declared above. Promote only if primary gains `>= +0.0003` over Run
   43 and every official slice is `>= -0.0005`. The other topic seeds are
   confirmation only and cannot be substituted after scores are known.
5. Stop at failure, convergence, 50 counted attempts, or six elapsed hours
   including preparation. Closing Run 46 does not stop the 72-hour campaign.

All metrics remain fixed development-sample evidence, not full-benchmark,
hidden-test, submission, or leaderboard results. Public-test labels and all
external actions remain locked.
