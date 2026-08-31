# Run 24 fresh-context review — before attempt 24

## Evidence that survived falsification

The causal user-item history FM passed all three paired chronological windows.
Validation gains over the promoted causal user-history FM were 0.006483188,
0.007094634, and 0.004750812; forward gains were 0.004121988, 0.003395730,
and 0.002872807. Both GAUC and nDCG@5 improved in every window. Fourteen of
fifteen date/activity slice comparisons improved; late high-activity changed
by only -0.000038036, inside the fixed -0.001 guard.

The signal is independently auditable. Four prior-day count/rate fields were
built from 149,177,950 official events for the fixed sampled videos. Training
rows use only earlier calendar days and scoring rows freeze at the training
cutoff. Full-month item-statistics tables, post-April-28 outcomes, public-test
labels, and hidden labels remain unused.

## What failed and stays closed

Replacing sampled user aggregates with all 207,446,146 full-corpus user events
improved early validation by only 0.000248 and was closed. One within-user
pairwise epoch improved by only 0.000016 after an implementation-only retry;
that objective is also closed. Rich current-item metadata and a post-hoc seed
ensemble remain rejected. No rate, bucket, field subset, or seed was tuned from
these failures.

## Main transfer risks

This remains a deterministic 1/32 development sample, not the organizer hidden
benchmark. The item fields encode logged exposure and long-view propensity, so
policy bias or temporal drift could reduce hidden transfer. Prior-day features
are deliberately coarser than true timestamp-causal features; this avoids
leakage but may leave signal unused. Unseen videos/authors fall back to the
fixed prior and cannot benefit. The absolute score is not comparable to the
protected KuaiRand-1K score or the organizer oracle ceiling.

## Locked next gate

Run official-development causal user-item models for seeds 2027, 2028, and
2029, each paired to history attempts 11, 13, and 15 respectively. Architecture,
features, optimizer, rank, and gates stay unchanged. Promotion requires three
aggregate seed wins and no unexplained slice regression beyond 0.001; the
existing history seed-2028 checkpoint remains protected until then. After the
three receipts, perform the attempt-24 strategic audit continuation rather than
ending the 72-hour search.
