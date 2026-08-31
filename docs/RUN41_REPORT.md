# Run 41 report: causal user-creator recency

## Decision

Run 41 was rejected and closed after its first chronological shadow. It added
two strictly causal current-creator recency fields—time since prior exposure
and time since prior long view—to the protected repeat-affinity FM.

| Measure | Repeat parent | Recency result | Change |
|---|---:|---:|---:|
| Early validation | 0.632885873 | 0.632286841 | -0.000599032 |
| Forward period | 0.634753164 | 0.632405011 | -0.002348153 |

Both GAUC and nDCG@5 declined. Medium-activity primary fell `-0.001827694`;
only high activity improved. The forward failure confirms that recency buckets
learned near the early cutoff did not transfer when elapsed time shifted. No
later archive, official seed, exact-video gap, time-unit change, cap change,
missing-value change, or edge sweep was attempted. The protected Run 39
seed-2029 candidate remains `0.6492243384881571`.

## Validity and accounting

The early archive contains all 207,446,146 rows, is 829,784,712 bytes, and has
SHA-256
`f79d062c88b7775fba7258b5b39bdca4cbbcd758a0ada1f4b81a2a179581af49`.
Its build completed in 1,338.202 seconds with 6,160,990,208-byte peak RSS. The
single scored attempt completed in 712.328 seconds with 15,545,057,280-byte
peak subprocess RSS.

This negative result is deterministic development-sample evidence, not hidden
test or leaderboard evidence. No public-test labels, hidden labels, upload,
submission, push, organizer contact, or public release occurred.
