# Run 44 protocol: fixed raw-logit seed consensus

Started: **2026-08-30 23:16 SGT**.

## Independent question

Does equal averaging of the raw logits from the same three confirmed
repeat-affinity seeds outperform Run 43's within-user rank averaging by
preserving cross-seed margin agreement without weakening chronological
transfer or robustness slices?

## Frozen candidate

- Members and order are exactly seeds 2027, 2028, and 2029 from Runs 38-39.
- Compute one equal arithmetic mean of their raw stored logits. Do not search
  weights, member subsets, clipping, calibration, logit scaling, ranks, or any
  other normalization.
- Model architecture, training outputs, cache, evaluator, splits, slices, and
  labels are unchanged. Run 43's rank consensus is the exact parent.

## Procedure and gates

1. Evaluate raw-logit consensus on early, middle, and late shadows in that
   order, using only the already preserved predictions.
2. Continue after a shadow only if validation and forward primary are each at
   least `-0.0003` versus the exact Run 43 rank-consensus parent and no slice
   is below `-0.0005`. At least two shadows must improve both aggregates by
   `>= +0.0002`; otherwise close without official evaluation.
3. Only after the shadow gate passes, evaluate the fixed official archives.
   Promote only if primary improves `>= +0.0003` over Run 43 and every fixed
   official slice is `>= -0.0005`.
4. Stop at family failure, declared convergence, 50 counted attempts, or six
   hours. Closing Run 44 does not stop the overall 72-hour campaign.

All metrics remain deterministic development-sample evidence, not full
benchmark, hidden-test, submission, or leaderboard results. Public-test labels
and all external actions remain locked.
