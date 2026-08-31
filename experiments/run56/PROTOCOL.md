# Run 56 protocol: rank-32 hard within-user fine-tune

Started: **2026-08-31 07:19:29 SGT**.

## Independent question

Can conservative training-only hard-pair BPR fine-tuning improve the protected
rank-32 repeat-affinity ordering without sacrificing pointwise or temporal
performance?

## Frozen implementation

- Load the exact Run52 rank-32 seed-2027 checkpoint for each shadow; do not
  repeat BCE training.
- Use existing deterministic within-user hard pairs: up to five lowest-scored
  positives against five highest-scored negatives per training user.
- BPR/softplus, sparse Adam learning rate `0.00005`, batch 32,768, maximum
  three epochs, patience 2, validation-gated rollback to epoch zero.
- Keep cache, feature set, rank, fields, split, seed, evaluator, prediction
  batches, and slices unchanged. No pair sampler, loss, learning-rate, pair-
  count, epoch, or blend variant is allowed.

## Gates

1. Early must improve validation `>= +0.00025`, keep forward `>= -0.0005`,
   no component metric below `-0.0005`, and no slice below `-0.001` versus
   exact Run52. Otherwise stop.
2. A pass repeats unchanged on middle and late. At least two of three windows
   must meet the validation gain with the same transfer/slice guards.
3. Only then fine-tune official seeds 2027–2029. Require paired mean gain
   `>= +0.00025`, no seed below `-0.0005`, span `<= 0.002`, and every official
   slice `>= -0.001`.
4. Only a passing seed set forms one equal within-user rank consensus; promote
   over Run52 at `>= +0.0003` with all slices `>= -0.0005`.
5. Stop at failure, rollback, convergence, 50 attempts, or six hours. Closing
   Run56 does not stop the 72-hour campaign.

All results remain deterministic 1/32 development-sample evidence, not the
full benchmark, hidden test, submission, or leaderboard. Public-test labels
and external actions remain locked.
