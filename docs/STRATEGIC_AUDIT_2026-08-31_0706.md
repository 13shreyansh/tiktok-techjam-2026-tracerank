# Strategic audit — 2026-08-31 07:06 SGT

## Evidence after Run53

Rank 64 regressed early validation, both component metrics, and every fixed
slice, while later training epochs deteriorated sharply. Raw capacity scaling
has therefore reached a local boundary. Run52 rank 32 remains the protected
architecture and further rank, learning-rate, batch-size, or regularization
sweeps are not justified by current evidence.

The strongest dormant signal is causal user-topic affinity. Run45 added only
prior user/current-primary-tag exposure count and long-view rate at rank 8. It
improved early validation `+0.000345186`, forward `+0.000381937`, and
high-activity primary `+0.001656192`; every slice stayed inside its safety
guard. It stopped because its old frozen gate required `+0.0005`, not because
the direction was negative. Run52 later demonstrated that rank 32 extracts
materially more value from the unchanged interaction field set across all
three seeds and every official slice.

## Run54 decision

Test exactly the already-defined two-field causal primary-tag affinity encoder
on the protected rank-32 architecture. This is a new interaction-capacity
question, not a retry of Run45 and not a tag-feature search. Keep its original
bucket definitions, causal construction, primary-tag-only scope, model,
optimizer, seeds, and evaluation unchanged. Do not test multi-tag, alternate
priors, recency, explicit actions, or feature subsets.

## Risks and third-person check

Topic affinity previously traded a small GAUC loss for a larger nDCG gain and
had a nearly flat late-date slice. It could still overfit the fixed sample or
heavy users. Chronological forward scores, all activity/date slices, three
paired official seeds, and a consensus promotion gate are therefore required.
Later feature archives are built only after the preceding gate passes.

An independent reviewer would consider this worthwhile because the earlier
signal was positive but underpowered, the parent capacity changed materially,
and the candidate is completely frozen before rescoring. It is more defensible
than validation-derived blending or reopening clearly negative feature
families. Run52 remains untouched regardless of outcome.
