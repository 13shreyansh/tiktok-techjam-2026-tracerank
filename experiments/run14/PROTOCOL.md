# Run 14 median-rank consensus protocol

Run tag: `run14-median-rank-consensus`
Branch: `codex/run14-median-rank-consensus`
Started: 2026-08-29 16:26 SGT

## Objective

Test one robust ensemble rule without changing the ranking model: replace mean
within-user rank across independent seeds with the within-user median rank. The
median discards extreme seed-specific ordering errors and may improve top-list
consensus, especially nDCG@5, while retaining the scale invariance that helped
Run 2.

## Fixed experiment and gate

- Base learner settings exactly match the Run 8 causal parent.
- Use seeds 2026, 2027, and 2028 on each early, middle, and late chronological
  shadow window. Reuse the already verified seed-2027 Run 8 prediction archive;
  train only the two missing seeds per window.
- Compare exactly two fixed three-seed aggregators in each window: equal mean
  within-user percentile rank and median within-user percentile rank. No
  weights, trimming level, or top-k parameter is searched.
- Median must beat mean by at least 0.0003 on both validation and forward in at
  least two of three windows, with no material activity/date regression, before
  it may be evaluated on the six frozen official-validation members.
- Official promotion then requires at least +0.0002 primary over 0.605400885,
  with neither GAUC nor nDCG@5 lower. Otherwise preserve the fallback.

Count every newly executed command as an attempt up to 50, stop within six
hours, enforce a ten-minute subprocess timeout, and write a fresh strategic
review after the family or eight attempts. Public-test labels remain locked.
Do not submit, upload, push, contact organizers, use credentials, change
registration, or change repository visibility.
