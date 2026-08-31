# Strategic audit — 2026-08-31 06:49 SGT

## Fresh-context conclusion

Run52 is a genuine local advance: rank 32 improved all three official seeds,
all fixed official slices, GAUC, nDCG@5, and the consensus primary. The
three-seed span is only `0.0002684491083153`. That pattern is inconsistent with
a one-seed accident and makes one further exact capacity doubling the highest
expected-value next question. A new bounded run is required for truthful
accounting, but it continues the successful modeling direction; it does not
end or reset the 72-hour campaign.

The strongest alternative families are currently less justified. Earlier
sampled-listwise and pairwise/BPR attempts reduced their own pointwise parents;
deep-cross, explicit-feedback, recency, topic-affinity, and multi-tag branches
also failed frozen temporal or slice gates. Recent mixed-capacity ensembles
were near convergence. Reopening those branches now would ignore stronger
direct evidence from capacity scaling.

## Run53 decision

Test exactly rank 64 against the exact rank-32 parent, with no intermediate
rank, learning-rate, batch-size, regularization, feature, loss, or seed sweep.
Use chronological shadows first and stop quickly if the gain does not transfer.
This is not validation-driven model search: rank 64, three seeds, gates, and
the single final consensus are frozen before the first score.

## Resource and generalization risks

- Rank-32 official training peaked at `35,985,244,160` bytes and produced a
  3,786,952,173-byte checkpoint. Linear extrapolation suggests a roughly
  7.43-GB rank-64 checkpoint and about 48–52 GB peak RSS. The host has
  68,719,476,736 physical bytes, so the attempt is feasible but memory is the
  primary operational risk.
- Rank-32 official attempts took 1,825–2,028 seconds. A conservative doubling
  forecast leaves three shadows and three official seeds close to, but inside,
  the six-hour run ceiling. Gates must prevent wasting time after weak shadows.
- Capacity may overfit identities or improve nDCG while weakening GAUC. Require
  chronological transfer, three paired seeds, and every fixed activity/date
  slice before promotion.
- The score remains a deterministic 1/32 development sample, not the hidden
  test. Repeated use can still overfit research decisions, so do not tune rank
  64 after observing it and do not infer a hidden or leaderboard score.

## Third-person goal check

An independent reviewer should prefer Run53 only if it answers a materially
new, falsifiable question, preserves Run52 unchanged, and can be stopped by
predeclared evidence. It meets those conditions. Winning probability is better
served by one controlled extrapolation from a three-seed monotonic gain than by
many small post-hoc blends or by reopening previously negative branches.
