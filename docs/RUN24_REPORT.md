# Run 24 report: KuaiRand-27K causal user-item history

## Decision

Run 24 closed at attempt 26 after a three-seed convergence win. Four causal
prior-day video/author count and long-view-rate fields, computed from all
official development events for the fixed sampled videos, improved the
previous causal user-history FM on three chronological windows and three
locked official-development seeds.

| Seed | User-history parent | User + item history | Change |
|---|---:|---:|---:|
| 2027 | 0.624713481 | 0.630043252 | +0.005329771 |
| 2028 | 0.626141456 | 0.630096716 | +0.003955259 |
| 2029 | 0.625046342 | **0.630624629** | +0.005578288 |

Both GAUC and nDCG@5 improved for every seed. All fifteen date/activity slice
comparisons improved; the minimum was +0.002234925. The three candidate scores
span 0.000581378, satisfying the predeclared epsilon 0.002 convergence stop.
Seed 2029 is the protected 27K-sample checkpoint.

## Data and leakage boundary

The scored data is a deterministic 1/32 sample: 6,481,138 rows, with April
8-21 training and April 22-28 development. The item cache matched 149,177,950
full-corpus events involving sampled videos. Training features use only prior
calendar days; scoring features freeze at the training cutoff. Post-April-28
outcomes and the official full-month item-statistics tables were not used.

This score is not a full KuaiRand-27K benchmark, hidden-test, submission, or
leaderboard result. Logged exposure bias, day-level coarsening, and unseen-item
fallback remain transfer risks.

## Accounting

Twenty-six counted attempts completed: 25 successful results and one failed
pre-score pair-constructor execution. Recorded model subprocess time totals
2,327.005 seconds; peak subprocess RSS is 2,357,280,768 bytes. The campaign was
approximately 7,277 seconds old at closure, including deterministic sampling,
cache construction, failed preprocessing attempts, and causal full-corpus
feature preparation. No public-test labels, hidden labels, upload, submission,
push, or public release occurred.
