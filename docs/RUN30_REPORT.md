# Run 30 report: four-times denser causal user-item history

## Decision

Run 30 closed at attempt 8 after a three-seed convergence win. The exact Run
24 rank-8 causal user-item FM trained on deterministic residue 0 modulo 8 while
every validation, forward, and robustness comparison remained fixed to the
original residue 0 modulo 32 rows.

| Seed | Run 24 parent | Denser training | Change |
|---|---:|---:|---:|
| 2027 | 0.630043252 | 0.635680029 | +0.005636777 |
| 2028 | 0.630096716 | **0.636251719** | +0.006155003 |
| 2029 | 0.630624629 | 0.636103351 | +0.005478722 |

The candidate mean is 0.636011700, a paired mean gain of +0.005756834. The
three scores span 0.000571690, satisfying the predeclared epsilon 0.002
convergence stop. Every like-for-like date/activity slice improved on all three
official-development seeds. Seed 2028 is the protected checkpoint.

## Audit correction and data boundary

The first early and middle attempts computed activity groups from all denser
training rows, making those groups incomparable with Run 24. Their overall,
forward, and date metrics remained valid, but their activity claims were
withdrawn. The scorer was corrected and tested so fitting uses dense rows while
activity groups use the fixed residue-0 reference rows. Corrected early,
middle, and late attempts then matched parent cutpoints and slice row counts
exactly and passed all gates.

The expanded cache retains 25,927,452 eligible April 8–28 rows for training and
uses exactly the original 6,481,138 residue-0 rows for evaluation/reference.
Ordered user, source-video, timestamp, date, and label identity was verified
before scoring. User/item history fields remain chronological and causal.

These metrics are not the full KuaiRand-27K benchmark, organizer hidden test,
submission, or leaderboard score. Exposure bias, unseen-item fallback, and
distribution shift remain transfer risks.

## Accounting

Eight counted attempts completed successfully. Model subprocess time totals
1,220.454 seconds; peak subprocess RSS is 4,734,566,400 bytes. Sampling, cache,
user-history, and item-history preparation took 1,810.54 recorded seconds; the
campaign was approximately 3,703 seconds old at closure. One official command
was blocked before execution because the audited shadow-state flag had not yet
been opened; it produced no iteration or score.

The protected local checkpoint is 334,657,829 bytes with SHA-256
`6349cc5d1f47bddf81fd667e8647708dec44fca56c7afb899fa9c05efaf156eb`.
No public-test labels, hidden labels, upload, submission, push, contact, or
public release occurred.
