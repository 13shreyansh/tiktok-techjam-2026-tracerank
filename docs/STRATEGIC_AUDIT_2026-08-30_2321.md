# Fresh-context strategic audit — 2026-08-30 23:21 SGT

## Why the next run changes signal, not aggregation

Run 44 showed that preserving raw seed margins gives only sub-gate movements;
another aggregation transform would be validation micro-tuning. The protected
Run 43 rank ensemble remains the strongest robust local 27K candidate.

The most important unresolved workshop/research clue is broader user interest:
a user who repeatedly long-views one topic may prefer a new video with the same
topic even when the exact video and creator are unseen. The current FM already
interacts static user and primary-tag embeddings, but it does not receive the
user's direct causal exposure count and empirical long-view rate for the
current tag. Exact user-video/creator repeat statistics produced the largest
recent gain, so extending that same prior-only statistic to the much smaller
topic space is a high-upside and interpretable hypothesis.

## Scope selected and alternatives rejected

Run 45 adds exactly two fields: prior user/current-primary-tag exposure count
and smoothed long-view rate. State uses only earlier timestamps through the
training cutoff; simultaneous impressions cannot see one another and scoring
state is frozen. It does not use tag2/tag3, future outcomes, full-month item
statistics, explicit actions, recency, a sequence network, model-capacity
changes, or a parameter sweep. Those additions would confound the causal
question and several already failed nearby families.

This is still evaluated on the deterministic 1/32 development sample, not the
full benchmark or hidden test. Promotion requires chronological transfer,
fixed slices, three official seeds, and a final fixed seed-consensus check
against Run 43.
