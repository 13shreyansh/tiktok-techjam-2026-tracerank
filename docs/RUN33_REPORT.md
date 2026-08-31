# Run 33 report: half-density causal user-item history

## Decision

Run 33 closed at attempt 6 after a three-seed convergence win. The exact Run
32 rank-8 causal user-item FM trained on deterministic residue 0 modulo 2 while
every validation, forward, and robustness comparison remained fixed to the
original residue 0 modulo 32 rows.

| Seed | Run 32 parent | Half-density training | Change |
|---|---:|---:|---:|
| 2027 | 0.638339246 | 0.641520824 | +0.003181578 |
| 2028 | 0.638260620 | **0.642439836** | +0.004179215 |
| 2029 | 0.638563195 | 0.642195882 | +0.003632687 |

The candidate mean is 0.642052181, a paired mean gain of +0.003664494. The
three scores span 0.000919012, satisfying the predeclared epsilon 0.002
convergence stop. Every like-for-like date/activity slice improved on all
three official-development seeds. Seed 2028 is the protected checkpoint.

## Data and validity boundary

The half cache retains 103,722,500 eligible April 8–28 rows for training and
uses exactly the original 6,481,138 residue-0-modulo-32 rows for evaluation
and robustness reference. Ordered user, source-video, timestamp, date, and
label identity was verified before scoring; both serialized row digests are
`1f375523f1f691c5b3ba59538350b98eef4450d28bb0bde0de4dde451d884cd8`.
All user/item histories were rebuilt chronologically and causally.

All three temporal shadows improved validation, forward, and every fixed
activity/date slice before official seeds were opened. The unchanged official
candidate then improved each matched Run 32 seed and every corresponding
slice. These metrics are not the full KuaiRand-27K benchmark, organizer hidden
test, submission, or leaderboard score. Exposure bias, unseen-item fallback,
and distribution shift remain transfer risks.

## Accounting

Six counted attempts completed successfully. Model subprocess time totals
2,974.737 seconds; peak subprocess RSS is 12,938,035,200 bytes. Sampling,
cache, user-history, and item-history preparation took 2,895.519 recorded
seconds. The campaign was approximately 6,186 seconds old when its last model
finished. No failed scored attempt occurred.

The protected local checkpoint is 731,023,621 bytes with SHA-256
`3b5a70099eedad21713f6c99d699a157027d60e9ce62a10f731d73c8681e1ebe`.
Its prediction artifact is 8,032,460 bytes with SHA-256
`4b93fb64ab2ca6b23e62d5bbbe8f7db60ea51c4ec589d451cfe28c3736b256c3`.
Both remain ignored local artifacts. No public-test labels, hidden labels,
upload, submission, push, contact, or public release occurred.
