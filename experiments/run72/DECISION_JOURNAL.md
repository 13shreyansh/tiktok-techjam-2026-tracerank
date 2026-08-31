# Run 72 decision journal

## 2026-08-31 11:24 SGT — corrected identity-freeze test frozen

- Run71 exactly reproduced rejected Run60 rather than declared Run52 because
  neutral unknown-row initialization remained the default.
- Use the newly explicit legacy random unknown-row compatibility mode and
  require exact epoch-1 Run52 reproduction before interpreting refinement.
- Begin with seed-2027 early only. Preserve Run52.
- All 71 tests and isolated-cache bytecode compilation passed before opening
  the run.

## 2026-08-31 11:37 SGT — exact parent reproduced; refinement rejected

- Attempt 1 completed successfully in `692.105190` seconds with
  `26,780,942,336`-byte peak RSS.
- Epoch 1 exactly reproduced Run52: loss, validation GAUC, nDCG@5, primary,
  forward metrics, every fixed slice, and both prediction arrays have zero
  difference.
- No frozen-identity epoch beat the parent. The best later primary was epoch 4
  at `0.6337686895740273`, or `-0.001396649458687782` versus Run52.
- The ignored 3,786,952,845-byte checkpoint SHA-256 is
  `42d7cd91ef42acdad003669ace6020787428ff83b02bafa432df9ace8a928bba`;
  the ignored 6,607,883-byte prediction archive SHA-256 is
  `8d2392915731af585177bbb79287fc391629dea2fbce9f1faab0c965db911872`.
- Stop the post-pass identity-freeze family. The universal one-pass peak is not
  rescued by continuing only lower-cardinality context/history rows.
