# Run 58 protocol: additive recent-sequence tail

Started: **2026-08-31 07:44:43 SGT**.

## Independent question

Can the fixed recent-sequence fields add stable linear evidence when excluded
from the protected rank-32 FM interaction path?

## Frozen candidate and gates

- Exact Run52 24-field rank-32 interaction base; append all eleven verified
  Run57 sequence fields as additive-only sparse linear fields.
- Exact Run52 BCE, learning rate 0.001, 20 epochs, patience 4, batching,
  threads, seeds 2027–2029, evaluator, splits, and slices.
- No field subset, tail weight, rank, loss, regularizer, initialization,
  optimizer, learning rate, seed, or ensemble-weight variation.
- Early seed 2027 must improve validation and forward primary each
  `>= +0.00025`, with no component metric below `-0.0005` and no fixed slice
  below `-0.001` versus exact Run52.
- A pass builds/trains middle and late unchanged; at least two of three windows
  must meet the same gain and safety guards.
- Only then build official state and train seeds 2027–2029. Require paired mean
  gain `>= +0.00025`, no seed below `-0.0005`, span `<= 0.002`, and every
  official slice `>= -0.001`.
- Score one equal within-user rank consensus only after seed stability; promote
  over Run52 at `>= +0.0003` with every slice `>= -0.0005`.
- Stop at gate/construction failure, convergence, 50 attempts, or six hours.
  Closing Run58 does not stop the 72-hour campaign.

All scores remain deterministic 1/32 development-sample evidence, not the full
benchmark, hidden test, submission, or leaderboard. Public-test labels and
external actions remain locked.
