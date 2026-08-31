# Run 63 decision journal

## 2026-08-31 08:33 SGT — tested exact fallback frozen

- Reuse the exact Run62 inputs and training-activity cutoff definition.
- Use new tested exact-fallback mode; do not blend base into routed users.
- Begin with early only. Preserve Run52.
- All 59 tests passed before opening the run.

## 2026-08-31 08:33 SGT — forward gain narrowly misses gate

- Attempt 1 completed successfully in `6.468082` seconds with
  `3,361,636,352`-byte peak RSS.
- Validation primary improved `+0.0002591555143150`, GAUC
  `+0.0001451720717213`, and nDCG@5 `+0.0003731389569087` versus Run52.
- Forward primary improved `+0.0002031095226152`, missing the frozen
  `+0.00025` threshold by `0.0000468904773848`.
- High activity improved `+0.0000301122157590`; cold/low improved
  `+0.0000949539624020`, medium `+0.0008699618058720`, early dates regressed
  `-0.0003017721603780`, and late dates `-0.0001556953321807`, all within
  slice guards.
- The ignored 4,161,718-byte prediction SHA-256 is
  `d1186b6eb351fb88874eff45dc37f391407438f16c15d953e70e22345c921e61`.
- Stop without middle, late, official, cutoff, or route variation.
