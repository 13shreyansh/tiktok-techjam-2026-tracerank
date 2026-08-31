# Run 68 protocol: fixed half-pass checkpoint

Started: **2026-08-31 09:10:00 SGT**.

## Independent question

Does the protected rank-32 repeat-affinity FM reach a better transferable
checkpoint halfway through its first deterministic shuffled training pass?

## Frozen candidate and gates

- Exact Run52 `history_item_repeat` rank-32 sparse FM.
- Exactly one epoch with `epoch_fraction=0.5`: the first
  `ceil(training_rows * 0.5)` positions of the seeded permutation.
- Exact Run52 initialization, learning rate 0.001, BCE objective, batching,
  threads, inference, evaluator, splits, slices, and seeds 2027–2029.
- No alternate fraction, extra epoch, learning rate, optimizer, regularizer,
  feature, loss, batch, rank, or checkpoint interpolation.
- Early seed 2027 must improve validation and forward primary each
  `>= +0.00025`, with no component below `-0.0005`, no fixed slice below
  `-0.001`, and peak RSS below 60,000,000,000 bytes versus exact Run52.
- A pass repeats unchanged on middle and late; at least two of three windows
  must meet the same gain and safety guards.
- Only then train official seeds 2027–2029. Require paired mean gain
  `>= +0.00025`, no seed below `-0.0005`, span `<= 0.002`, and every official
  slice `>= -0.001`.
- Score one equal within-user rank consensus only after seed stability; promote
  over Run52 at `>= +0.0003` with every slice `>= -0.0005`.
- Stop at any gate, memory, or artifact failure, convergence, 50 attempts, or
  six hours. Closing Run68 does not stop the 72-hour campaign.

All scores remain deterministic 1/32 development-sample evidence, not the full
benchmark, hidden test, submission, or leaderboard. Public-test labels and
external actions remain locked.
