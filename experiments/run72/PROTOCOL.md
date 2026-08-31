# Run 72 protocol: corrected post-pass raw-identity freeze refinement

Started: **2026-08-31 11:24:30 SGT**.

## Independent question

After explicitly reproducing protected Run52's legacy random unknown-row
initialization, can freezing raw user, video, and author rows after epoch 1
allow context and causal-history rows to refine without identity overfit?

## Construction and scoring gates

- Exact Run52 `history_item_repeat` rank-32 sparse FM and explicit
  `legacy_random_unknown_init` through epoch 1.
- Epoch-1 validation GAUC, nDCG@5, primary, and loss must exactly reproduce
  Run52 seed-2027 early before any hypothesis score is accepted. A mismatch is
  a construction failure, not a negative model result.
- From epoch 2 onward, remove only raw user, video, and author rows from sparse
  latent and linear optimizer updates. All other rows continue unchanged.
- Exact Run52 BCE, learning rate 0.001, epoch order, maximum 20 epochs,
  patience 4, batching, threads, inference, evaluator, splits, slices, and
  seeds 2027–2029.
- No freeze-point, frozen-field, initialization, learning-rate, regularization,
  epoch-count, optimizer, rank, feature, loss, batch, calibration, or blend
  search.
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
- Stop at any construction, score, memory, or artifact failure, convergence,
  50 attempts, or six hours. Closing Run72 does not stop the 72-hour campaign.

Source SHA-256 before scoring:
`ed21133dede975a3b109be84777141db5afe02996fb298b0560e146fac6c4c58`.
All 71 tests and isolated-cache bytecode compilation passed. All scores remain
deterministic 1/32 development-sample evidence, not the full benchmark, hidden
test, submission, or leaderboard. Public-test labels and external actions
remain locked.
