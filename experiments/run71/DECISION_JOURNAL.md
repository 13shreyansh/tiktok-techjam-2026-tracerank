# Run 71 decision journal

## 2026-08-31 11:10 SGT — identity-freeze refinement frozen

- All three Run52 shadows and all three official seeds select epoch 1; every
  epoch-2 score is materially worse.
- Reproduce epoch 1 exactly, then freeze only raw user/video/author embedding
  and linear rows. Continue lower-cardinality context and causal-history rows.
- Begin with seed-2027 early only. Preserve Run52.
- All 70 tests and isolated-cache bytecode compilation passed before opening
  the run.

## 2026-08-31 11:23 SGT — declared-parent reproduction defect

- Attempt 1 completed successfully in `684.152659` seconds with
  `26,781,106,176`-byte peak RSS, but epoch 1 was `0.6347827300641647`
  instead of exact Run52 `0.6351653390327151`.
- The epoch-1 validation, forward, and prediction archive are bit-for-bit the
  rejected Run60 neutral-unknown result; prediction SHA-256 is
  `91976e932b79719f0d51344740868d9016b0fed0945205defbf820455cbd5d8c`.
- Root cause: Run60's corrected zero initialization of unknown rows remained
  the default after that candidate was rejected. Run71 therefore tested the
  identity freeze on the wrong parent.
- Later frozen-identity epochs deteriorated more slowly than Run60 but never
  exceeded epoch 1. That is not evidence about exact Run52.
- Close Run71 as a counted construction-invalid attempt. A corrected explicit
  legacy-Run52 initialization requires a fresh bounded run before this
  hypothesis can be evaluated.
