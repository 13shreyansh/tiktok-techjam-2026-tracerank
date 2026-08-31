# Run 40 decision journal

## 2026-08-30 14:27 SGT — run opened and code frozen

- Run 39 promoted repeat affinity at campaign level with three-seed mean
  `0.6489308670307136` and best seed-2029 primary `0.6492243384881571`.
- Fresh-context review selected creator-specific explicit feedback because the
  workshop named likes, follows, comments, forwards, and negative feedback as
  useful history, while the current user-author interaction uses only long
  view. Global item/author behavior failed earlier; this test asks the distinct
  user-author interaction question.
- Add only strong-feedback and hate-rate buckets for the current creator.
  Exact-video behavior is excluded for sparse coverage, and no hyperparameter
  or bucket search is allowed.
- Frozen ranker SHA-256 is
  `5014d779322a2add1eb6857cce70dfed50264c587cc51dbd41e8755577a1bea9`;
  builder SHA-256 is
  `99c14dd1f7a24895c97183a8b6694cb846675187f3bc8109e3341b12ffe10746`.
  Compilation and all 50 standard-library tests pass before scoring.
- This advances the winning objective only if it transfers across time and
  users beyond the already-strong repeat parent. Build early features first;
  official development remains locked.

## 2026-08-30 14:52 SGT — early feature build verified

- The builder completed successfully in 1,491.886 seconds with
  6,712,590,336-byte peak RSS and all 207,446,146 rows written.
- The ignored 829,784,712-byte archive SHA-256 is
  `9860323b7270447397343b855b8c311397ae4deff7bf2abb93d2eb6d08852f49`.
- On fixed early evaluation rows, prior exposure to the current author exists
  for 198,310 / 865,586 validation rows (22.91%) and 182,852 / 960,523 forward
  rows (19.04%). Among exposed rows, more than 99.6% of strong-rate buckets and
  more than 99.99% of hate-rate buckets differ from the no-history prior.
- Proceed to attempt 1 with the frozen candidate and exact Run 38 early parent.
  Later feature builds and official development remain locked.

## 2026-08-30 15:03 SGT — early gate failed; run closed

- Attempt 1 completed successfully in 560.011 seconds with
  15,276,818,432-byte peak RSS. Epoch 1 was selected.
- Validation primary is `0.6326468709152537`, `-0.0002390023810916` versus the
  exact repeat-affinity parent. GAUC falls `-0.0003962265202262`, nDCG@5 falls
  `-0.0000817782419571`, and forward primary falls `-0.0002123632214432`.
- Cold/low falls `-0.000055531`, medium falls `-0.001200064`, high improves
  `+0.001124302`, early dates improve `+0.000501065`, and late dates fall
  `-0.000322016`. The required validation gain fails and the medium slice also
  crosses the `-0.001` guard.
- Close the family after one scored attempt. Do not build middle, late, or
  official features; do not tune the action union, prior, buckets, or weights.
  The protected repeat-affinity candidate remains unchanged and the overall
  hackathon campaign continues with a fresh hypothesis.
