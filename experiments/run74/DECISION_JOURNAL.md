# Run 74 decision journal

## 2026-08-31 11:57 SGT — chronological order frozen

- Run52 universally peaks after one complete pass; added representation and
  loss complexity has not improved transfer.
- Change only the one-pass traversal from seed shuffle to stable global
  timestamp order. Preserve exact Run52 initialization and all other settings.
- Begin with seed-2027 early only. Preserve Run52.
- All 73 tests and isolated-cache bytecode compilation passed before opening
  the run.

## 2026-08-31 12:09 SGT — first gate failed; branch closed

- The command completed successfully in `677.178521` seconds and peaked at
  `27,782,021,120` bytes RSS.
- Validation primary was `0.6319153908834496`, or
  `-0.0032499481492655` versus exact Run52. Forward primary was
  `0.6335973787010323`, or `-0.0031845616159048`.
- Validation GAUC changed `-0.0025960065812070`; validation nDCG@5 changed
  `-0.0039038897173241`. Forward GAUC changed `-0.0027324294563834`;
  forward nDCG@5 changed `-0.0036366937754263`.
- Every fixed slice regressed. Primary deltas were cold/low
  `-0.0030870332540780`, medium `-0.0034972288173032`, high
  `-0.0033359818949272`, early date `-0.0022259141974909`, and late date
  `-0.0028829041425308`.
- The frozen first gate therefore fails decisively. Do not run later windows,
  official seeds, reverse order, order mixtures, or a blend. Protect Run52 and
  close only this hypothesis; the 72-hour campaign continues.
