# Run 59 decision journal

## 2026-08-31 08:00 SGT — normalized rank-64 hypothesis frozen

- Hold initial FM dot-product variance equal to protected rank 32 by using
  `latent_init_std=0.008408964152537145` at rank 64.
- Begin with seed-2027 early only. Preserve Run52 and compare to both Run52 and
  the unnormalized Run53 rank-64 result.
- All 58 tests passed before opening the run.

## 2026-08-31 08:14 SGT — normalized rank-64 gate fails

- Attempt 1 completed successfully in `805.203233` seconds with
  `45,375,324,160`-byte peak RSS.
- Normalization improved early primary only `+0.0000618384191967` over
  unnormalized Run53, while remaining `-0.0006031548353358` below exact
  Run52. Forward primary was `-0.0001996377400483` below Run52 and
  `-0.0000842095639938` below Run53.
- Versus Run52, GAUC regressed `-0.0005659334909706`, nDCG@5
  `-0.0006403761797010`; cold/low regressed `-0.0005597440964928`, medium
  `-0.0009787780337972`, high `-0.0002196434571122`, early dates
  `-0.0003050073594436`, and late dates `-0.0008172450709120`.
- The ignored 7,431,533,965-byte checkpoint SHA-256 is
  `0b9aa1ff1e85ce2d69bb571eb4e1d0b967edef53f9b04bc8e4400ce7f5624629`;
  the ignored 6,614,981-byte prediction SHA-256 is
  `f2e24e3951e3838bc822e5f1b9f5343f721aea376c021dfcf495a01b6a7d28ab`.
- Stop rank-64 capacity after this corrected comparison. No middle, late,
  official, alternative initialization, other rank, or consensus follows.
