# Run 41 protocol: causal user-creator recency

## Hypothesis

The protected repeat-affinity FM summarizes cumulative user-author exposure and
long-view rate, but cannot distinguish a creator watched recently from the same
history accumulated long ago. Adding strictly causal time-since-last-exposure
and time-since-last-long-view buckets can capture preference freshness without
changing the target or objective.

## Frozen change

- Keep the protected repeat-affinity rank-8 FM, BCE objective, learning rate
  `0.001`, optimizer, epochs/patience, batches, seeds, full-training cache,
  fixed evaluation rows, evaluator, and robustness definitions unchanged.
- Add exactly two categorical fields for the current user-author pair: elapsed
  hours since the last eligible exposure and since the last eligible long view.
- Bucket each as `floor(log2(elapsed_hours + 1))`, cap at 15, and use 16 as a
  separate never-seen value. No edge, cap, time unit, or missing-value sweep is
  allowed.
- State uses only earlier timestamps through the split training cutoff.
  Same-user/author/timestamp rows update together. Validation and forward rows
  measure time from frozen training state; their outcomes never update it.
- Exact-video recency is excluded for the same sparse-coverage reason recorded
  in Run 40.

## Gates

1. Build and hash `shadow_early`, then compare once with the exact Run 38 early
   repeat-affinity parent. Continue only for validation gain `>= +0.0005`,
   forward `>= -0.0005`, and every fixed slice `>= -0.001`.
2. If early passes, build and test middle and late unchanged. At least two of
   three shadows must pass with no material transfer failure.
3. Only then build official features and run seeds 2027-2029. Promote for
   paired mean gain `>= +0.0005`, no seed below `-0.0005`, and score span
   `<= 0.002`.
4. Stop on family failure, convergence, 50 attempts, or six hours. Closing Run
   41 does not stop the overall hackathon campaign.

All metrics remain deterministic development-sample evidence, not hidden test,
submission, or leaderboard evidence. Public-test labels and external actions
remain locked.

