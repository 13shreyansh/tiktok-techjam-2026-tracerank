# Run 34 report: full-density causal user-item history

## Decision

Run 34 closed at attempt 6 after a three-seed convergence win. The exact Run
33 rank-8 causal user-item FM trained on every eligible April 8–21 row while
every validation, forward, and robustness comparison remained fixed to the
original residue 0 modulo 32 rows.

| Seed | Run 33 parent | Full-density training | Change |
|---|---:|---:|---:|
| 2027 | 0.641520824 | 0.644615073 | +0.003094248 |
| 2028 | 0.642439836 | **0.645083464** | +0.002643628 |
| 2029 | 0.642195882 | 0.644804206 | +0.002608324 |

The candidate mean is 0.644834248, a paired mean gain of +0.002782067. The
three scores span 0.000468391, satisfying the predeclared epsilon 0.002
convergence stop. Every like-for-like date/activity slice improved on all
three official-development seeds. Seed 2028 is the protected checkpoint.

## Data and validity boundary

The full cache retains all 207,446,146 eligible April 8–28 rows for training
and uses exactly the original 6,481,138 residue-0-modulo-32 rows for evaluation
and robustness reference. Ordered user, source-video, timestamp, date, and
label identity was verified before scoring; both serialized row digests are
`1f375523f1f691c5b3ba59538350b98eef4450d28bb0bde0de4dde451d884cd8`.
All user/item histories were rebuilt chronologically and causally.

All three temporal shadows improved validation, forward, and every fixed
activity/date slice before official seeds were opened. The unchanged official
candidate then improved each matched Run 33 seed and every corresponding
slice. These metrics are not the full KuaiRand-27K benchmark, organizer hidden
test, submission, or leaderboard score. Exposure bias, unseen-item fallback,
and distribution shift remain transfer risks.

## Accounting

Six counted attempts completed successfully. Model subprocess time totals
6,058.573 seconds; peak subprocess RSS is 23,416,307,712 bytes. Sampling,
cache, user-history, and item-history preparation took 3,810.067 recorded
seconds. The campaign was approximately 10,258 seconds old when its last model
finished. No failed scored attempt occurred.

The protected local checkpoint is 1,053,512,773 bytes with SHA-256
`0b473b20f570e64d46f68600432db21c047fb92ab2d2e97db59f08b7d5f26190`.
Its prediction artifact is 8,034,023 bytes with SHA-256
`e00a479ec967caa8b25264f14b3e14d872194d19845a50d3f4e43e3e9387cdb7`.
Both remain ignored local artifacts. No public-test labels, hidden labels,
upload, submission, push, contact, or public release occurred.
