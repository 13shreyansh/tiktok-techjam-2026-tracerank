# Run 24 fresh-context review — after eight scored iterations

## What the evidence says

The sampled 27K anchor is stable enough to support paired decisions, but its
absolute scores are not comparable to an organizer hidden result. The base FM
completed three chronological windows. Adding label-free content/context fields
then improved validation by 0.010302 to 0.011702 and forward primary by 0.010598
to 0.011682 on all three windows, with every activity slice improving. That is
the strongest Run 24 evidence and establishes content FM as the current 27K
sample parent.

The strictly causal history family has completed two paired windows. Against
content FM it improved early validation by 0.001654 and forward by 0.002534;
middle validation improved by 0.003696 and forward by 0.003614. The early
high-activity slice regressed by 0.000825, close to but inside the fixed 0.001
tolerance; all middle-window slices improved. This is promising but not yet a
promotion.

## Main risk and likely bottleneck

The largest residual weakness is nDCG@5 for high-activity users, not aggregate
GAUC. The history fields mainly add smoothed counts and recent category state;
they may improve broad discrimination while still ordering the top five poorly.
The 27K sample also retains only 1/32 of events, so its history is incomplete by
construction. A sampled score can guide robust engineering but cannot establish
full-history quality, an organizer bonus, or hidden-set transfer.

The rejected late-run command was a governance stop before execution, not a
model failure and not a scored iteration. No public or hidden labels were used.

## Decision

Run the unchanged late history shadow. Promote the history family only if it
beats the paired content parent by at least 0.001 primary, does not lose more
than 0.0005 forward, and has no activity/date slice regression beyond 0.001.
If it passes, establish paired official-development content and history anchors
with identical seeds, then require three unchanged history seeds as declared.
If it fails, close aggregate history and move to one independently declared
top-of-list objective or denser-history experiment; do not tune buckets from
the observed late result.
