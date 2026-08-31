# Run 66 protocol: bipartite history-to-candidate FM

Started: **2026-08-31 08:42:00 SGT**.

## Independent question

Does restricting rank-32 latent interactions to person/history-to-candidate
pairs improve ranking by removing irrelevant same-side FM interactions?

## Frozen candidate and gates

- Exact Run52 `history_item_repeat` features and rank 32.
- Left fields: indices `(0, 3, 8–15, 20–23)` representing user, context tab,
  user histories, and candidate-aware user-entity histories.
- Right fields: indices `(1, 2, 4–7, 16–19)` representing video, author,
  content attributes, and item histories.
- Latent score includes only left-right dot products. Sparse linear effects for
  all 24 fields remain unchanged.
- Exact Run52 initialization scale, BCE, learning rate 0.001, 20 epochs,
  patience 4, batching, threads, seeds 2027–2029, evaluator, splits, and slices.
- No grouping, residual, rank, learning-rate, regularizer, optimizer, feature,
  objective, batch, seed, epoch, or ensemble-weight variation.
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
  six hours. Closing Run66 does not stop the 72-hour campaign.

All scores remain deterministic 1/32 development-sample evidence, not the full
benchmark, hidden test, submission, or leaderboard. Public-test labels and
external actions remain locked.
