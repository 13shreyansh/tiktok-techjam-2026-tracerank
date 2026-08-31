# Run 40 report: causal user-creator explicit feedback affinity

## Decision

Run 40 was rejected and closed after its first chronological shadow. It added
two strictly causal per-user creator rates—explicit strong feedback and hate—
to the protected repeat-affinity FM.

| Measure | Repeat parent | Explicit-feedback result | Change |
|---|---:|---:|---:|
| Early validation | 0.632885873 | 0.632646871 | -0.000239002 |
| Forward period | 0.634753164 | 0.634540801 | -0.000212363 |

GAUC and nDCG@5 both declined. The medium-activity slice regressed
`-0.001200064`, crossing the predeclared `-0.001` slice guard; only the
high-activity and early-date slices improved. No later feature archive,
official seed, ablation, action-union variation, prior change, or bucket sweep
was attempted. The protected Run 39 seed-2029 candidate remains
`0.6492243384881571`.

## Validity and accounting

The early archive contains all 207,446,146 cache rows, is 829,784,712 bytes,
and has SHA-256
`9860323b7270447397343b855b8c311397ae4deff7bf2abb93d2eb6d08852f49`.
Its build completed in 1,491.886 seconds with 6,712,590,336-byte peak RSS.
The single scored attempt completed in 560.011 seconds with
15,276,818,432-byte peak subprocess RSS.

This negative result is deterministic development-sample evidence, not hidden
test or leaderboard evidence. No public-test labels, hidden labels, upload,
submission, push, organizer contact, or public release occurred.
