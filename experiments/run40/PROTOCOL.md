# Run 40 protocol: causal user-creator explicit feedback affinity

## Hypothesis

The protected repeat-affinity FM knows whether a user repeatedly long-watches
the current creator, but it does not distinguish explicit positive actions
(like, follow, comment, or forward) from `is_hate` for that creator. Adding two
strictly causal user-author rate buckets can capture creator preference and
aversion beyond long viewing.

## Frozen change

- Keep the protected repeat-affinity rank-8 FM, BCE objective, learning rate
  `0.001`, optimizer, epochs/patience, batches, seeds, full-training cache,
  fixed evaluation rows, evaluator, and robustness definitions unchanged.
- Add exactly two categorical fields: prior user-author strong-feedback rate
  and prior user-author hate rate. Strong feedback is the fixed union of
  `is_like`, `is_follow`, `is_comment`, and `is_forward`.
- Use exposure count as the denominator, the existing fixed Beta(1,3) prior,
  and 21 rate buckets. The already-present user-author exposure count field is
  not duplicated.
- State uses only earlier timestamps through the split's training cutoff.
  Same-user/author/timestamp rows update together; validation and forward state
  is frozen. Missing authors retain the fixed prior.
- Exact-video behavior is excluded because Run 38 measured only 0.38% nonzero
  repeat coverage on early validation. No field, action union, prior, bucket,
  weight, or learning-rate sweep is allowed.

## Gates

1. Build and hash `shadow_early`, then compare once with the exact Run 38 early
   parent. Continue only for validation gain `>= +0.0005`, forward
   `>= -0.0005`, and every fixed slice `>= -0.001`.
2. If early passes, build and test middle and late unchanged. At least two of
   three shadows must pass with no material transfer failure.
3. Only then build official features and run seeds 2027-2029. Promote for
   paired mean gain `>= +0.0005`, no seed below `-0.0005`, and candidate score
   span `<= 0.002`.
4. Stop on family failure, convergence, 50 attempts, or six hours. Closing Run
   40 does not stop the overall hackathon campaign.

All metrics remain deterministic development-sample evidence, not full hidden
benchmark, submission, or leaderboard evidence. Public-test labels and all
external actions remain locked.

