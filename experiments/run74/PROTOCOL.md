# Run 74 protocol: exact chronological one-pass ordering

Started: **2026-08-31 11:57:00 SGT**.

## Independent question

Does stable global chronological training order improve the protected Run52
rank-32 repeat-affinity FM on later validation and forward periods?

## Frozen candidate and gates

- Exact Run52 `history_item_repeat` rank-32 sparse FM with explicit legacy
  random unknown-row initialization.
- Traverse every eligible training row in stable ascending `time_ms` order;
  preserve verified cache order inside equal timestamps.
- Exact Run52 BCE, learning rate 0.001, 20 epochs, patience 4, batching,
  threads, inference, evaluator, splits, slices, and seed 2027.
- No reverse order, day shuffle, recency weight, rolling window, order mixture,
  alternative tie order, learning-rate, regularizer, rank, feature, loss,
  batch, calibration, or blend.
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
  six hours. Closing Run74 does not stop the 72-hour campaign.

Source SHA-256 before scoring:
`56dd167bf9df426154dac062cd10883dc03593d6b03f25e95121cf1eb32182b8`.
All 73 tests and isolated-cache bytecode compilation passed. All scores remain
deterministic 1/32 development-sample evidence, not the full benchmark, hidden
test, submission, or leaderboard. Public-test labels and external actions
remain locked.
