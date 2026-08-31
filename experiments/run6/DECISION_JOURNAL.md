# Run 6 decision journal

## 2026-08-29 14:48 SGT — campaign start

- Protected fallback: exact Run 2 six-seed within-user rank ensemble at
  validation primary 0.605400885.
- Paired early parent from Run 5: validation 0.616920352, forward 0.603989244.
- First family: add hour-of-day and weekday as categorical context.

## 2026-08-29 14:56 SGT — attempt 1 and strategic audit

- Hour plus weekday scored 0.618160486 on early validation, a gain of
  0.001240134 over the paired parent.
- Its next-window score was 0.603295803, a loss of 0.000693440. This misses the
  predeclared forward-safety gate by 0.000193440 and is not promoted.
- Every recorded robustness slice improved: low activity +0.001227985,
  medium +0.001315437, high +0.001644868, early dates +0.001333606, and late
  dates +0.000554296. Preserve the result as possible ensemble diversity, but
  do not validation-select it into the final candidate.
- The organizer workshop distinguishes ranking (this challenge) from final
  whole-list re-ranking (explicitly outside this challenge). Previous Run 5
  user-listwise and pairwise fine-tuning directly tested ranking-aligned losses
  and reduced their own pointwise checkpoints.
- The protected parent uses only positive long-view video/tag history. Click,
  like, follow, comment, and forward have been tested as aggregates, auxiliary
  targets, or latest-event context, but not as a unified causal sequence; the
  available `is_hate` signal has not yet been represented. That is a larger,
  organizer-grounded gap than further time-bin tuning.
- Stop Run 6 after one attempt. The next independent family should encode
  causal multi-behavior history while keeping the official target and
  user-grouped evaluator fixed.
