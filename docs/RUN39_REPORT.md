# Run 39 report: independent repeat-affinity confirmation

## Decision

Run 39 closed after its single predeclared attempt. It independently evaluated
the exact frozen Run 38 repeat-affinity candidate on missing seed 2029 after
Run 38's six-hour guard had prevented that command from starting.

Seed 2029 reached GAUC `0.7035301008552636`, nDCG@5
`0.5949185761210506`, and primary `0.6492243384881571`. Relative to the exact
Run 34 seed-2029 parent, the primary gain is `+0.0044201326297953`; every fixed
activity/date slice also improved.

Combining this confirmation with the two Run 38 seeds gives:

| Seed | Run 34 parent | Repeat affinity | Change |
|---|---:|---:|---:|
| 2027 | 0.644615073 | 0.648551700 | +0.003936627 |
| 2028 | 0.645083464 | 0.649016563 | +0.003933099 |
| 2029 | 0.644804206 | **0.649224338** | +0.004420133 |

The candidate mean is `0.6489308670307136`, paired mean gain is
`+0.0040966194469133`, minimum seed gain is `+0.0039330988963173`, and score
span is `0.0006726389322296`. These pass the frozen campaign-level promotion
gate. Seed 2029 is the new protected KuaiRand-27K development candidate.

## Artifact and accounting evidence

The ignored seed-2029 checkpoint is 1,053,516,117 bytes with SHA-256
`9cf1bdb3ceb4ee7dd9e55c4f4160167ead6a06c6e27a607bd9662093d3ec0826`.
Its 8,035,582-byte prediction archive has SHA-256
`831b805d5c0aa7dadef5c940e09a7b364c75dc3c68300d5804c892fc91d7aeeb`.
The ranker and official repeat-feature hashes match the Run 39 protocol.

One counted attempt completed in 1,838.667 seconds with peak subprocess RSS
23,444,537,344 bytes. Run 39 used no tuning, public-test labels, hidden labels,
upload, submission, push, organizer contact, or public release.

## Validity boundary

This score is from the fixed deterministic development evaluation sample after
training on all eligible April 8-21 rows. It is not the full hidden benchmark,
organizer hidden test, submission, or leaderboard. Cross-run confirmation is
reported explicitly because Run 38 itself remains closed and unpromoted after
only two official seeds; Run 39 supplies separate third-seed evidence at the
campaign level.
