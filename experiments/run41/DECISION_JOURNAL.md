# Run 41 decision journal

## 2026-08-30 20:27 SGT — run opened and code frozen

- Run 40 rejected creator-specific explicit feedback after early validation,
  forward, and medium-activity regressions. No tuning followed; the protected
  repeat-affinity seed-2029 candidate remains `0.6492243384881571`.
- Fresh-context review identifies recency—not more action types—as the most
  important missing interaction. Cumulative user-author history can be stale,
  while the workshop emphasizes recent behavior and ranking context.
- Add only exposure-gap and positive-gap log2-hour buckets, with a fixed never
  value. Do not add exact-video gaps or tune bucket definitions.
- Frozen ranker SHA-256 is
  `3546226f7af3307fa3051f19794d0fff54aa02e20748a27e34f9afaab85f25d1`;
  builder SHA-256 is
  `69b577e8cbb4de7d4cf713bdb65d24c1b063d8cef00f2ef035b82dec56b51c74`.
  Compilation and all 51 standard-library tests pass before scoring.
- This advances the winning objective only if freshness transfers across
  chronological windows and robustness slices. Build early features first;
  official development remains locked.

## 2026-08-30 20:49 SGT — early recency build verified

- The builder completed successfully in 1,338.202 seconds with
  6,160,990,208-byte peak RSS and all 207,446,146 rows written.
- The ignored 829,784,712-byte archive SHA-256 is
  `f79d062c88b7775fba7258b5b39bdca4cbbcd758a0ada1f4b81a2a179581af49`.
- On fixed early validation rows, prior exposure recency is available for
  198,310 / 865,586 rows (22.91%) and prior long-view recency for 82,643
  (9.55%). Forward coverage is 182,852 / 960,523 (19.04%) and 76,681 (7.98%).
- Forward seen buckets are 6-7 because state freezes at the early training
  cutoff and elapsed time continues; this is a real transfer condition to test,
  not a reason to alter buckets after inspection.
- Proceed to attempt 1 with the frozen candidate and exact Run 38 early parent.
  Later feature builds and official development remain locked.

## 2026-08-30 21:02 SGT — early gate failed; run closed

- Attempt 1 completed successfully in 712.328 seconds with
  15,545,057,280-byte peak RSS. Epoch 1 was selected.
- Validation primary is `0.6322868410224808`, `-0.0005990322738646` versus the
  exact repeat parent. GAUC falls `-0.0005870245780074`, nDCG@5 falls
  `-0.0006110399697217`, and forward primary falls `-0.0023481531650886`.
- Cold/low falls `-0.000384823`, medium falls `-0.001827694`, high improves
  `+0.000767240`, early dates fall `-0.000167207`, and late dates fall
  `-0.000439332`. Both the forward and medium-activity guards fail materially.
- Close after one scored attempt. Do not build middle, late, or official
  recency features and do not tune time units, caps, missing values, or edges.
  The protected repeat-affinity candidate remains unchanged; continue the
  overall campaign with a fresh hypothesis.
