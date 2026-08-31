# Run89 decision journal

## 2026-08-31 18:32 SGT — family frozen

- Run88 closed; do not search another aggregation rule.
- Freeze one small causal self-attention encoder before the existing
  candidate-conditioned history attention.
- Opening gate is paired seed 2027 on the early chronological window. Require
  `+0.0005` validation and nonnegative forward transfer with hard floors.
- A failed opening gate closes the architecture with no head/layer/width,
  position, history, seed, loss, optimizer, or blend rescue.
- Run84 remains protected and official final-test outcomes remain locked.

## 2026-08-31 18:35 SGT — implementation verification passed

- Eleven targeted tests and the complete 103-test suite passed; Python
  compilation, CLI discovery, and `git diff --check` passed.
- The new component test exercises causal masking, left padding, an entirely
  empty history row, finite outputs, and finite backward gradients.
- No model or benchmark score was produced. Commit exact code and protocol
  before the first counted seed-2027 execution.

## 2026-08-31 18:37 SGT — opening gate closes the family

- The only counted attempt succeeded on MPS in `84.690969` seconds with peak
  RSS `7,821,934,592` bytes and no official-test outcomes loaded.
- Validation primary changed from `0.6169077754` to `0.5112471581`, or
  `-0.1056606174`; GAUC changed `-0.1285452247` and nDCG@5
  `-0.0827760398`.
- Forward primary changed `-0.0789712071`. Every activity/date slice regressed;
  medium activity was worst at `-0.1328274981`.
- This is a catastrophic representation failure, plausibly because normalized
  Transformer outputs destroyed the small candidate/history embedding geometry.
  The explanation is an inference, not a separately verified causal diagnosis.
- Close without residual scaling, normalization changes, heads/layers/widths,
  positions, history length, optimizer, loss, seed, window, or blending. Do not
  use the model in the official candidate. Run84 remains protected.
