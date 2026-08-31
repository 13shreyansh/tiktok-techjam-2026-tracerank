# Run87 protocol: chronological cross-fit LambdaMART residual

Declared: **2026-08-31 18:09 SGT**, before implementation or any Run87 score.

## Fixed construction

Train one low-capacity user-grouped residual ranker on causally separated
errors from the frozen three-seed causal ensemble:

- meta parent: exact Run83 early causal consensus;
- meta parent archive SHA-256
  `2646d2c9bc9f28c50614c10a13956d5177b682a696a5e18e5a6aa0b25d0706cc`;
- meta-train rows: 12--14 April, parent trained only on 8--11 April;
- meta-validation rows: 15--17 April, used only for tree early stopping;
- opening target parent: exact Run83 late causal consensus;
- target parent archive SHA-256
  `ccd35a4ace535d82065adcbc69279c8f9e6b21272a62ce9850e88457dd95975e`;
- target validation: 18--21 April; target forward: 22--28 April;
- features: within-user parent percentile rank plus the complete existing
  `CausalAggregateBuilder` matrix. Aggregate labels/rates are frozen from
  8--11 April for meta rows and advanced chronologically only through the
  target parent training cutoff for target rows;
- no evaluation row updates aggregate state;
- LightGBM 4.6.0 `lambdarank`, nDCG@5, truncation 5, learning rate 0.05,
  31 leaves, minimum 1,000 rows per leaf, 63 bins, no feature/bagging sampling,
  200 rounds maximum, 20-round early stopping, 16 CPU threads, seed 2027;
- final score is within-user parent rank plus the tree raw residual. No blend
  coefficient, clipping, route, calibration, feature subset, tree parameter,
  or alternate parent is allowed.

Public validation labels are permitted development evidence. Final-test
outcomes are never loaded. The random log and 1K/27K data are excluded.

## Gates and continuation

1. Opening attempt targets `shadow_late`. The meta-validation corrected score
   must improve its saved-artifact early parent primary
   `0.6048954350050247` by at least `0.0005`. On the independent
   18--21 April target validation, require at least `+0.0005` primary, no GAUC
   or nDCG@5 loss beyond `0.0005`, and no activity/date slice below `-0.001`.
   The exact saved target parent is GAUC `0.6670450748473019`, nDCG@5
   `0.5187261229696177`, primary `0.5928855989084598`; target forward primary
   on 22--28 April is `0.6042330415190079` and may decline by at most `0.0002`.
2. If step 1 passes, apply the unchanged tree configuration to the clean Run84
   official-validation/final-test parent. The aggregate state may advance only
   through 21 April training rows; the tree remains trained solely on the
   frozen 12--17 April meta windows. Promote only for `+0.0002` official
   primary over Run84, no component/slice loss beyond `0.001`, finite aligned
   feature-only final-test predictions, and a passing label-blind CSV checker.

Failure at either stage closes the family without rescue tuning.

## Limits and stopping

- Hard limits: 50 counted executions and six hours for Run87.
- Convergence: epsilon `0.00005`, `N=3`, minimum floor 2. This finite two-stage
  construction stops at the first failed gate or the first completed official
  candidate; no artificial iterations are added.
- Every launched command counts, including failures. A fresh review is needed
  after eight counted executions.
- No submission, upload, push, visibility change, organizer contact, or secret
  use is authorized.
