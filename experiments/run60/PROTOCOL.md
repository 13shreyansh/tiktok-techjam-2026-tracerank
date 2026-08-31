# Run 60 protocol: deterministic unknown initialization

Started: **2026-08-31 08:16:00 SGT**.

## Independent question

Does correctly neutralizing random initial values for trainable unknown/missing
embedding rows improve the protected rank-32 repeat-affinity FM?

## Frozen candidate and gates

- Exact Run52 `history_item_repeat` rank-32 sparse FM with default
  `latent_init_std=0.01`; only unknown-row initialization is corrected from the
  ineffective advanced-index operation to in-place zero initialization.
- Unknown rows remain trainable after initialization.
- Exact Run52 BCE, learning rate 0.001, 20 epochs, patience 4, batching,
  threads, seeds 2027–2029, evaluator, splits, and slices.
- No rank, initialization scale, masking, freezing, learning rate, regularizer,
  optimizer, feature, objective, batch, seed, epoch, or ensemble-weight search.
- Early seed 2027 must improve validation and forward primary each
  `>= +0.00025`, with no component metric below `-0.0005` and no fixed slice
  below `-0.001` versus exact Run52.
- A pass repeats unchanged on middle and late; at least two of three windows
  must meet the same gain and safety guards.
- Only then train official seeds 2027–2029. Require paired mean gain
  `>= +0.00025`, no seed below `-0.0005`, span `<= 0.002`, and every official
  slice `>= -0.001`.
- Score one equal within-user rank consensus only after seed stability; promote
  over Run52 at `>= +0.0003` with every slice `>= -0.0005`.
- Stop at gate or construction failure, convergence, 50 attempts, or six
  hours. Closing Run60 does not stop the 72-hour campaign.

All scores remain deterministic 1/32 development-sample evidence, not the full
benchmark, hidden test, submission, or leaderboard. Public-test labels and
external actions remain locked.
