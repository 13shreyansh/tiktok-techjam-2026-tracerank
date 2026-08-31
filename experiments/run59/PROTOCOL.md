# Run 59 protocol: variance-normalized rank-64 repeat affinity

Started: **2026-08-31 08:00:00 SGT**.

## Independent question

Does rank 64 improve the protected repeat-affinity FM when its initial
dot-product variance is held equal to rank 32?

## Frozen candidate and gates

- Exact Run53 `history_item_repeat` rank-64 configuration, except
  `latent_init_std=0.008408964152537145` instead of `0.01`.
- Exact Run52 BCE, learning rate 0.001, 20 epochs, patience 4, batching,
  threads, seeds 2027–2029, evaluator, splits, and slices.
- No other rank, initialization, learning rate, regularizer, optimizer,
  feature, objective, batch, seed, epoch, or ensemble-weight variation.
- Early seed 2027 must improve validation primary `>= +0.00025` versus exact
  Run52 and improve over Run53 rank 64, with forward primary `>= -0.0005`, no
  component metric below `-0.0005`, no fixed slice below `-0.001`, and peak
  RSS below 60,000,000,000 bytes.
- A pass repeats unchanged on middle and late; at least two of three windows
  must meet the same validation gain and safety guards.
- Only then train official seeds 2027–2029. Require paired mean gain
  `>= +0.00025`, no seed below `-0.0005`, span `<= 0.002`, every official
  slice `>= -0.001`, and peak RSS below 60,000,000,000 bytes.
- Score one equal within-user rank consensus only after seed stability; promote
  over Run52 at `>= +0.0003` with every slice `>= -0.0005`.
- Stop at gate or memory failure, convergence, 50 attempts, or six hours.
  Closing Run59 does not stop the 72-hour campaign.

All scores remain deterministic 1/32 development-sample evidence, not the full
benchmark, hidden test, submission, or leaderboard. Public-test labels and
external actions remain locked.
