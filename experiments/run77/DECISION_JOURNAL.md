# Run 77 decision journal

## 2026-08-31 12:37 SGT — target-aware residual frozen

- Run76 closed below its frozen validation materiality gate; its exact tree and
  consensus are not being tuned.
- Run4 already audited random exposure, so exposure debiasing is not reopened.
- Freeze one candidate-aware 27K mechanism: candidate primary tag attends over
  five causal positive-history tags, then predicts a correction to exact
  Run52. No raw identities enter the residual.
- Epoch-zero output is exact Run52. A 4,096-row smoke comparison had maximum
  absolute error `0.0`; 80 tests and bytecode compilation pass.
- Begin one early-window attempt. Preserve Run52 regardless of outcome.

## 2026-08-31 12:42 SGT — epoch one regresses; exact rollback retained

- Epoch zero reproduced all preserved Run52 validation predictions with maximum
  absolute error `0.0`.
- Epoch 1 primary was `0.6336730452542434`, a
  `-0.0014922937784717` regression from exact Run52. GAUC changed
  `-0.0012904440931404` and nDCG@5 `-0.0016941434638031`.
- Patience one stopped training. Best epoch remained zero, so saved validation
  and forward predictions are byte-for-byte the exact parent archive; their
  SHA-256 is
  `8d2392915731af585177bbb79287fc391629dea2fbce9f1faab0c965db911872`.
- The initial result JSON defined activity tertiles from all training rows,
  unlike the established evaluation-sampled reference. That reporting-only
  mismatch produced cutpoints 1,577/3,374. A read-only rescore of the saved
  exact-parent prediction with the established 1,282,407-row reference
  reproduced cutpoints 49/106 and every exact Run52 slice. The implementation
  was corrected for future use; no model metric or branch decision changed.
- Close this coarse-tag DIN residual without width, history length, action,
  context, learning-rate, blend, or epoch variants. Continue the overall
  campaign after a fresh audit.
