# Run 39 fresh-context strategic audit

## Evidence reviewed

- Run 34 is the protected full-density causal user/item-history candidate at
  seed-2028 primary `0.6450834641517389`.
- Run 35 hard within-user pairwise fine-tuning restored epoch zero with no
  gain; Run 36 rare identity pooling and Run 37 fixed rank blending both
  regressed their early shadows and closed immediately.
- Run 38 added user-author/video repeat-affinity fields. All three temporal
  shadows improved validation, forward periods, and every fixed slice. Its two
  completed official seeds gained `+0.003936627` and `+0.003933099`, but its
  six-hour guard blocked the predeclared third seed before execution.

## Third-person goal check

The goal is not to manufacture more iterations; it is to maximize likely
hidden-test performance without leakage or validation overfitting. The most
valuable uncertainty is now seed stability of a frozen, broadly positive
candidate. Changing the model before resolving that would discard strong
evidence and confound whether the repeat-affinity fields generalize.

The best next action is therefore one independent confirmation attempt using
seed 2029 with the exact frozen Run 38 code, features, data, and stopping rule.
This new benchmark run is disclosed separately because Run 38 exhausted its
wall-clock budget. It is not permission to tune or search the same family.

## Risks and next family

- The development sample is deterministic and may not represent the hidden
  test; exposure bias, unseen identities, and temporal distribution shift
  remain unresolved.
- Epoch 1 wins consistently and later epochs deteriorate, so learning-rate or
  epoch tuning on official development would be validation chasing.
- The ledger's historical `model_sha256` field hashes source, not checkpoints;
  direct checkpoint and prediction hashes must remain authoritative.
- If confirmation passes, the next independent family should test one
  predeclared behavioral interaction motivated by the workshop (for example,
  causal user-creator strong/negative feedback affinity), starting from fresh
  temporal shadows. It must not sweep bucket counts, priors, or weights.

