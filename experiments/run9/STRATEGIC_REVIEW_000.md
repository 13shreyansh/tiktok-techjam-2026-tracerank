# Strategic review 000 — explicit higher-order feature crosses

## Evidence

- The workshop emphasizes categorical IDs, rich features, and feature
  interactions in a ranking-stage model.
- The parent is already a DeepFM-like model: embeddings, a pairwise FM term,
  a two-layer MLP, and target-aware positive-history attention.
- DCN-V2 reports that feed-forward networks can learn feature crosses
  inefficiently and proposes explicit, bounded-degree cross layers for
  web-scale ranking systems.
- AutoInt likewise motivates automatic high-order interactions, but a
  self-attention field tower adds more architectural choices. A two-layer
  full-rank cross tower is the smaller first test on this six-field model.
- Temporal, multi-behavior, listwise, pairwise, multitask, and causal aggregate
  families have already been tested. This is an independent capacity question.

## Decision

Add a two-layer cross tower in parallel with the existing deep tower, retain the
FM term, and make no other change. One failed attempt ends the family.
