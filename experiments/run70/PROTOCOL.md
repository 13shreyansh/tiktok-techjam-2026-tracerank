# Run 70 protocol: recurring time context on protected Run52

Started: **2026-08-31 09:36:00 SGT**.

## Independent question

Do recurring hour-of-day and weekday interactions improve the protected 27K
rank-32 repeat-affinity FM with chronological transfer?

## Frozen candidate and gates

- Exact Run52 `history_item_repeat` rank-32 sparse FM.
- Append exactly Asia/Shanghai hour (`0..23`) and weekday (`0..6`) categorical
  fields derived from already cached timestamps/dates.
- Exact Run52 initialization, BCE, learning rate 0.001, 20 epochs, patience 4,
  batching, threads, inference, evaluator, splits, slices, and seeds 2027–2029.
- No raw date, alternative timezone, bin, cyclic encoding, time gap, decay,
  field subset, rank, learning rate, optimizer, regularizer, batch, or blend.
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
  six hours. Closing Run70 does not stop the 72-hour campaign.

Source SHA-256 before scoring:
`a760d64b1e0d861f4d8e08e3e6e0873f4f03be818740d432ad7fc4d2e4ccb280`.
All 67 tests and bytecode compilation passed. All scores remain deterministic
1/32 development-sample evidence, not the full benchmark, hidden test,
submission, or leaderboard. Public-test labels and external actions remain
locked.
