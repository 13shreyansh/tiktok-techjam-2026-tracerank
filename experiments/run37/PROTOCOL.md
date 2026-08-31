# Run 37 protocol: cross-density rank consensus

## Hypothesis

The protected full-density and half-density causal history-item FMs make
complementary ordering errors. A fixed equal within-user percentile-rank
consensus can reduce density-specific overfit and improve chronological
ranking without changing either member.

## Frozen candidate

- Use the exact matching Run 34 full-density and Run 33 half-density prediction
  archives. No retraining, member selection, or score calibration.
- Convert each member independently to deterministic within-user percentile
  ranks and average 50/50. The two-member set and equal weight are fixed before
  Run 37 reads a score; no weight or subset sweep is permitted.
- Compare each shadow to the exact Run 34 full-density parent on identical
  evaluation rows and fixed activity/date slices.

## Gates

1. Run `shadow_early` first. Continue only for validation and forward gains of
   at least `+0.0003`, with every fixed slice at least `-0.0003` versus Run 34.
2. If early passes, repeat middle and late unchanged. At least two of three
   shadows must pass and no window may show a material transfer failure below
   `-0.0005` aggregate or `-0.001` on a slice.
3. Only then evaluate the fixed matching official seed pairs. Promote for
   paired mean gain `>= +0.0003`, no seed below `-0.0003`, and score span
   `<= 0.002`.
4. Stop on the first decisive family failure, convergence, 50 attempts, or six
   hours. Closing Run 37 does not close the 72-hour campaign.

All metrics are deterministic development-sample evidence, not hidden-test,
full-benchmark, submission, or leaderboard evidence. Public-test labels and
all external actions remain locked.
