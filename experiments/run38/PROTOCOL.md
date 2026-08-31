# Run 38 protocol: causal user-creator/video repeat affinity

## Hypothesis

Run 34 knows global video/author history and broad user/tag history, but not
whether a particular user repeatedly watches the current creator or exact
video. Adding strictly causal user×author and user×video count/long-view-rate
buckets can capture persistent creator affinity and repeat viewing that the
workshop explicitly identifies as ranking-stage behavioral context.

## Frozen change

- Keep Run 34 full-density rank-8 `history_item` FM, BCE, learning rate
  `0.001`, optimizer, epochs/patience, batches, seeds, cache, evaluation rows,
  evaluator, and robustness definitions unchanged.
- Add exactly four categorical fields: prior user-author count log2, smoothed
  long-view rate; prior user-video count log2, smoothed long-view rate.
- Build state from training rows only. Rows sharing a user/entity/timestamp see
  the same prior state, then update together. Validation and forward rows use
  state frozen at the split cutoff. Missing authors retain zero-count prior.
- Count cap 15 and the existing fixed Beta(1,3), 21-bin rate encoding are fixed
  by the already-audited user/item history representation. No field ablation,
  prior, cap, or bucket sweep is allowed.

## Gates

1. Prepare and hash `shadow_early` features, then run the unchanged candidate.
   Continue only for validation gain `>= +0.0005`, forward `>= -0.0005`, and
   every fixed slice `>= -0.001` versus Run 34.
2. If early passes, build and test middle and late unchanged. At least two of
   three must pass with no material transfer failure.
3. Only then build official features and run seeds 2027–2029. Promote for
   paired mean gain `>= +0.0005`, no seed below `-0.0005`, and span `<= 0.002`.
4. Stop on family failure, convergence, 50 attempts, or six hours. Closing this
   bounded hypothesis does not stop the 72-hour campaign.

All results remain deterministic development-sample evidence, not hidden-test,
full-benchmark, submission, or leaderboard evidence. Public-test outcomes and
all external actions remain locked.
