# Run 78 decision journal

## 2026-08-31 12:46 SGT — creator-and-tag history frozen

- Run77 tag-only attention regressed and is not tuned.
- Freeze one distinct information source: ordered positive creators aligned to
  the existing positive tags; no video or user identity enters the residual.
- Creator archive: zero timestamp inversions, 207,446,146 × 5 int32, SHA-256
  `d3c563e5d1f70fcde871e01c0d7185979141804d541a2391714f3a30bc140ec7`.
- All 84 tests pass; epoch-zero 4,096-row parent error is `0.0`.
- Begin one early attempt and preserve Run52.

## 2026-08-31 12:50 SGT — creator attention regresses; branch closed

- Epoch 1 primary was `0.6338891192837905`, or
  `-0.0012762197489246` versus exact Run52. GAUC changed
  `-0.0012844118567609`; nDCG@5 changed `-0.0012680276410882`.
- Patience stopped after the first failed epoch. Best epoch remained zero, and
  final validation, forward, and all established slices reproduce Run52.
- The final prediction archive is byte-identical to the parent with SHA-256
  `8d2392915731af585177bbb79287fc391629dea2fbce9f1faab0c965db911872`.
- Close creator-and-tag DIN without widths, history length, exact-video,
  auxiliary actions, optimization, or blend variants. Recent-history attention
  now has two consistent first-gate failures on 27K.
