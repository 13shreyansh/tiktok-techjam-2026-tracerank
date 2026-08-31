# Run 64 decision journal

## 2026-08-31 08:34 SGT — two-to-one shrinkage frozen

- Give the rank-16 seed consensus one vote and exact Run52 two identical votes.
- Use no activity route and no alternate weight.
- Begin with early only. Preserve Run52.

## 2026-08-31 08:35 SGT — forward gate fails

- Attempt 1 completed successfully in `6.192740` seconds with
  `3,367,092,224`-byte peak RSS.
- Validation primary improved `+0.0003640851113182`, GAUC
  `+0.0002241039601183`, and nDCG@5 `+0.0005040662625182` versus Run52.
- Forward primary improved only `+0.0001777153613997`, below the frozen
  `+0.00025` gate.
- Cold/low improved `+0.0002979576967466`, medium `+0.0010190419894973`,
  early dates `+0.0003051952539144`, and late dates
  `+0.0002244227729128`; high activity regressed `-0.0005927376477256`,
  inside the `-0.001` slice guard.
- The ignored 4,771,077-byte prediction SHA-256 is
  `7c8a877fe7f0fca0144d1354928510efc75dc417a4a03ae2d8e99b042c9bef43`.
- Stop without middle, late, official, or alternate weight.
