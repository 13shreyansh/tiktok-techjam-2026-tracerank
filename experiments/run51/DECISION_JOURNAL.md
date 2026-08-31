# Run 51 decision journal

## 2026-08-31 04:11 SGT — six members and gates frozen before scoring

- Protected Run49 official primary is `0.6509565751074728`.
- All six members, member order, equal one-sixth within-user rank votes,
  temporal comparisons, and gates were fixed before Run51 read any consensus
  score.
- All member predictions already exist from successful prior commands. Run51
  trains no model and does not select members from Run50's official outcomes.
- Begin with the early chronological union only.

## 2026-08-31 04:12 SGT — early magnitude gate fails

- Attempt 1 completed successfully in `7.318592` seconds with
  `3,458,875,392`-byte peak RSS.
- Validation primary is `0.6344968654666717`, a gain of
  `+0.0001964301231455` over Run49; forward is `0.6367952442287790`, a gain
  of `+0.0003449724338651`.
- Validation misses the frozen `+0.00025` continuation gate. Every fixed
  primary slice is directionally positive, ranging from `+0.0001180160973089`
  for cold/low activity to `+0.0003262887108777` for medium activity, but the
  aggregate gate is authoritative.
- Prediction SHA-256 is
  `31053a45170d9f23231188680853e3ba8de083cb5d2375a0e568ace7d3f33df8`.
- Stop without middle, late, official, subset, weight, duplicate, or
  normalization variants. Run49 remains protected.
