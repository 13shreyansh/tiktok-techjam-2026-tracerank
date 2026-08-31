# Run 80 decision journal

## 2026-08-31 14:49 SGT — frozen DeepFM tower selected

- Run79 closes tree residual correction after clean meta improvement failed to
  transfer forward or to high-activity users.
- The standard shallow MLP described in the workshop has not been isolated on
  the protected 27K representation. Prior 1K DeepFM relearned all embeddings;
  it does not answer whether higher-order functions of frozen Run52 embeddings
  add signal safely.
- Freeze parent, architecture, defaults, gate, and exact rollback before score.
  Begin with seed-2027 early only and preserve Run52.

## 2026-08-31 14:53 SGT — pre-score metadata mismatch corrected

- The first 4,096-row smoke command stopped before prediction because the old
  Run52 checkpoint predates serialization of `legacy_random_unknown_init` and
  stores no such key. No model, score, ledger entry, or artifact was produced.
- Narrow the loader to accept only missing/`None` or explicit `True`; explicit
  neutral mode remains rejected. Exact tensor shapes, field dimensions, offsets,
  split, feature set, model type, seed, full checkpoint hash, and stored
  prediction reproduction remain mandatory. This compatibility correction does
  not change the residual, parameters, data, hypothesis, or gates.
- The corrected 4,096-row smoke test reproduced the stored parent with maximum
  absolute error `0.0`; every output was finite. The two focused tests and all
  88 repository tests pass, bytecode compilation and diff checks pass, and no
  benchmark score has occurred.

## 2026-08-31 14:54 SGT — attempt 1 rejected and exact parent restored

- The first trained epoch scored validation GAUC `0.6995229674369844`, nDCG@5
  `0.5642114570814302`, and primary `0.6318672122592073`. Relative to the exact
  parent this is `-0.0033757609508163`, `-0.0032204925961994`, and
  `-0.0032981267735078`, respectively, so it failed the frozen primary and both
  component gates.
- Patience-one rollback selected epoch zero. Final validation and forward scores
  therefore equal the parent, and the saved prediction archive has the exact
  parent SHA-256 `8d2392915731af585177bbb79287fc391629dea2fbce9f1faab0c965db911872`.
  Its two float32 arrays have lengths 865,586 and 960,523 and are finite.
- The wrapper completed successfully in `81.0618839263916` seconds at
  `20,103,299,072` bytes peak RSS. Run80 stops at one counted attempt without
  width, learning-rate, dropout, epoch, blend, later-window, or seed search.
  Run52 remains protected; closing this hypothesis does not stop the campaign.
