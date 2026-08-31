# Run 69 protocol: entire-space click-to-long-view funnel

Started: **2026-08-31 09:19:00 SGT**.

## Independent question

Does explicit entire-space modeling of the impression-to-click-to-long-view
funnel improve the protected rank-32 repeat-affinity FM?

## Frozen candidate and gates

- Exact Run52 `history_item_repeat` fields and rank-32 shared sparse latent
  interaction representation.
- Two sparse linear heads: click and conditional long view.
- Joint score is
  `P(click) * P(long_view | click)`; train with equal click BCE plus
  all-impression joint-long-view BCE. Rank by its log probability.
- Exact Run52 initialization, learning rate 0.001, 20 epochs, patience 4,
  batching, threads, inference grouping, evaluator, splits, slices, and seeds
  2027–2029.
- No task weight, action union, head depth, separate latent tower, fraction,
  learning rate, optimizer, regularizer, feature, batch, rank, or loss variant.
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
  six hours. Closing Run69 does not stop the 72-hour campaign.

Source SHA-256 before scoring:
`ee2949b4e0b476d44112abab4366296150855dd0e53ad0f1e920eef4edbc8a8f`.
All 65 tests passed. All scores remain deterministic 1/32 development-sample
evidence, not the full benchmark, hidden test, submission, or leaderboard.
Public-test labels and external actions remain locked.
