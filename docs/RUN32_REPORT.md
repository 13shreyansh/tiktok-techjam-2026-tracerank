# Run 32 report: quarter-density causal user-item history

## Decision

Run 32 closed at attempt 6 after a three-seed convergence win. The exact Run
30 rank-8 causal user-item FM trained on deterministic residue 0 modulo 4 while
every validation, forward, and robustness comparison remained fixed to the
original residue 0 modulo 32 rows.

| Seed | Run 30 parent | Quarter-density training | Change |
|---|---:|---:|---:|
| 2027 | 0.635680029 | 0.638339246 | +0.002659217 |
| 2028 | 0.636251719 | 0.638260620 | +0.002008902 |
| 2029 | 0.636103351 | **0.638563195** | +0.002459844 |

The candidate mean is 0.638387687, a paired mean gain of +0.002375987. The
three scores span 0.000302575, satisfying the predeclared epsilon 0.002
convergence stop. Every like-for-like date/activity slice improved on all
three official-development seeds. Seed 2029 is the protected checkpoint.

## Data and validity boundary

The quarter cache retains 51,858,724 eligible April 8–28 rows for training and
uses exactly the original 6,481,138 residue-0-modulo-32 rows for evaluation
and robustness reference. Ordered user, source-video, timestamp, date, and
label identity was verified before scoring. All user/item history fields were
rebuilt chronologically and causally for the quarter cache.

All three temporal shadows improved validation, forward, and every fixed
activity/date slice before official seeds were opened. The unchanged official
candidate then improved each matched Run 30 seed and every corresponding
slice. These metrics are not the full KuaiRand-27K benchmark, organizer hidden
test, submission, or leaderboard score. Exposure bias, unseen-item fallback,
and distribution shift remain transfer risks.

## Accounting

Six counted attempts completed successfully. Model subprocess time totals
1,693.050 seconds; peak subprocess RSS is 7,720,288,256 bytes. Sampling,
cache, user-history, and item-history preparation took 2,137.08 recorded
seconds; the campaign was approximately 4,230 seconds old when its last model
finished. Three setup commands failed safely before scoring while explicit
scope validation was added; no iteration, model, prediction, or score was
produced by them.

The protected local checkpoint is 499,271,389 bytes with SHA-256
`0575c4fab7d77c38db8f0b012625bbb6a27bf2e0011c3210c7db024419bd6386`.
Its prediction artifact is 8,024,460 bytes with SHA-256
`1db163a487bc2d5b7115b5d8c4f1474973270ddad7b976f267b78ae32c4fcc6f`.
Both remain ignored local artifacts. No public-test labels, hidden labels,
upload, submission, push, contact, or public release occurred.
