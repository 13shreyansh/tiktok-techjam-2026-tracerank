# Run 8 decision journal

## 2026-08-29 15:10 SGT — campaign start

- Protected fallback: official validation primary 0.605400885.
- Fresh controls are required because MPS runs show small seed-fixed variance.
- The ensemble mode and equal weights are fixed before exporting predictions;
  no alpha search will be performed.

## 2026-08-29 15:20 SGT — early-window ensemble promoted

- Fresh parent: validation 0.616858721, forward 0.603960752.
- Fresh temporal member: validation 0.618115127, forward 0.602672994.
- Equal within-user rank ensemble: validation 0.618297050
  (+0.001438329) and forward 0.604082451 (+0.000121698).
- The ensemble improved every robustness slice over the fresh parent: low
  +0.001564174, medium +0.001311344, high +0.001477598, early dates
  +0.001362335, and late dates +0.000948163.
- This is the first post-fallback family to pass validation magnitude, forward
  safety, and slice robustness simultaneously. Proceed to matched middle and
  late chronological windows without changing weights or rank normalization.

## 2026-08-29 15:31 SGT — three-window confirmation complete

- Middle ensemble: validation +0.000585882, forward +0.000459553; all five
  slices positive.
- Late ensemble: validation 0.593479373 (+0.000693538), forward 0.603695803
  (+0.000248366); all five slices nonnegative.
- The fixed blend improved validation and forward scores in all three windows.
  Its gains are smaller in middle/late than early, so the evidence supports
  official seed replication but not a claim of hidden-test improvement.
- Official phase: train only temporal members for seeds 2026, 2027, and 2028.
  Combine them by equal within-user rank with the protected six raw parent
  members, giving the new temporal family one third of total ensemble weight.
  Do not search weights or evaluate public-test labels.

## 2026-08-29 15:38 SGT — official confirmation failed; fallback retained

- Temporal seeds 2026/2027/2028: 0.603768229, 0.604628444, and 0.604765832.
- Predeclared nine-member equal-rank ensemble: 0.605206580.
- Protected six-member fallback: 0.605400885. Delta: -0.000194305.
- The chronological blend was directionally consistent but did not transfer to
  the official validation ensemble. Reject it without searching weights.
- Test score arrays were generated for reproducibility but their labels were
  never evaluated; do not package the rejected nine-member output as final.
