# Run 67 protocol: data-derived positive class balance

Started: **2026-08-31 08:55:00 SGT**.

## Independent question

Does training-split class-balanced BCE improve within-user positive ordering
for the protected rank-32 repeat-affinity FM?

## Frozen candidate and gates

- Exact Run52 `history_item_repeat` rank-32 sparse FM.
- Positive BCE multiplier is exactly `training negatives / training positives`
  for each declared split; negative multiplier remains 1.
- Exact Run52 initialization, learning rate 0.001, 20 epochs, patience 4,
  batching, threads, seeds 2027–2029, inference, evaluator, splits, and slices.
- No multiplier, clipping, focal loss, user weighting, auxiliary label, rank,
  learning rate, regularizer, optimizer, feature, objective, batch, seed,
  epoch, or ensemble-weight variation.
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
  six hours. Closing Run67 does not stop the 72-hour campaign.

All scores remain deterministic 1/32 development-sample evidence, not the full
benchmark, hidden test, submission, or leaderboard. Public-test labels and
external actions remain locked.
