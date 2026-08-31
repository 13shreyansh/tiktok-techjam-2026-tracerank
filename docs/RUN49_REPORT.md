# Run 49 report: rank-diverse consensus promoted

## Decision

Run 49 promoted the fixed equal within-user percentile-rank ensemble of three
rank-8 repeat-affinity seeds and one rank-16 seed-2027 repeat-affinity member.
Membership, order, equal weights, aggregation, temporal windows, and gates were
committed before the first score. No subset, weight, seed, rank, calibration,
or route search occurred.

| Window | Run 43 primary | Run 49 primary | Change | Forward change |
|---|---:|---:|---:|---:|
| Early | 0.633887887 | 0.634300435 | +0.000412549 | +0.000351766 |
| Middle | 0.644987055 | 0.645304390 | +0.000317335 | +0.000650068 |
| Late | 0.641519584 | 0.642019414 | +0.000499831 | +0.000753834 |

Every validation, forward, and fixed robustness slice improved in all three
windows. On the locked official development sample, Run 49 reached GAUC
`0.7047811197152637`, nDCG@5 `0.5971320304996821`, and primary
`0.6509565751074728`. This gains `+0.0007684364739026` over Run 43. Official
slice gains were cold/low `+0.0006515642245275`, medium
`+0.0007329051292458`, high `+0.0013066670931650`, early dates
`+0.0003003591877796`, and late dates `+0.0007348126573359`.

## Artifacts and accounting

The ignored 6,803,132-byte ensemble prediction archive has SHA-256
`d78777fa1e0193bc9b2b23df5baf02f20113405f031d79dc2df74aab0250cfd1`.
The new ignored rank-16 checkpoint is 1,964,661,421 bytes with SHA-256
`254109e02b71a8f756c9f58bbd4befc15c75fc043b29c8531ff6c840aadb3e8b`;
its 8,040,461-byte prediction archive has SHA-256
`c3507f1faa5eb0d8eaf068768eda478db76c3603b2f592cbd74ccce195207c66`.
The three rank-8 member hashes remain preserved in the candidate manifest.

Seven counted attempts completed successfully in 3,943.229 subprocess
seconds; peak subprocess RSS was 28,455,649,280 bytes. Run 49 began at
2026-08-31 00:39 SGT and reached its final score at 01:49 SGT, below both the
50-attempt and six-hour limits.

## Validity boundary

This score uses full eligible training rows and a fixed deterministic 1/32
development evaluation sample. It is not the full KuaiRand-27K benchmark,
organizer hidden test, submission, or leaderboard. Promotion protects the best
local candidate; it does not estimate a hidden score or end the 72-hour
campaign. No public-test labels, hidden labels, upload, submission, push,
organizer contact, registration change, or public release occurred.
