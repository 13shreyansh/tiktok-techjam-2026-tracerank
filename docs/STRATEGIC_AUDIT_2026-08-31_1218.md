# Strategic audit — 2026-08-31 12:18 SGT

## Evidence after Run75

Frozen FM-video cosine similarity regressed every aggregate and slice by a
large margin. The learned FM rows are interaction parameters, not a trustworthy
metric item space. Do not change cosine, profile weighting, or routing: that
would tune a failed mechanism. Run52 remains protected.

## Independent list-ranking question

The workshop emphasized that the task judges the ordering of each user's list,
yet the protected FM is optimized row by row with BCE. Pairwise fine-tunes and
sampled neural listwise losses have already failed, so repeating those losses
is unjustified. A still-untested alternative is LambdaMART: boosted decision
trees trained directly on user-grouped ranking lists. It has a different
inductive bias and can learn nonlinear thresholds among causal counts/rates
without adding millions of identity parameters.

Run76 will use only bounded, training-cutoff-safe fields already audited in
Run52: log duration; tab; primary tag; upload/video type; eight causal user
history fields; four prior-day item/author fields; and four exact user-entity
repeat fields. It excludes raw user, video, and author identities, dates,
future outcomes, explicit-action additions, recurring time, sequence fields,
and rejected feature families. Training rows are stably grouped by user and
the binary long-view label becomes relevance 0/1.

Freeze one conservative deterministic configuration before scoring: LightGBM
`lambdarank`, NDCG@5, 200 maximum rounds, learning rate 0.05, 31 leaves,
minimum 1,000 rows per leaf, 63 bins, truncation level 5, all features, no row
bagging, and 20-round early stopping. The tree score is not promoted alone; it
gets exactly one equal within-user rank vote with the matching exact Run52
prediction. There is no parameter, feature, weight, subset, or route search.

## Gates and third-person check

Begin on seed-2027 early. Require the fixed parent/tree consensus to improve
validation and forward primary each `>= +0.0005`, both components
`>= -0.0005`, every slice `>= -0.001`, and peak RSS below 60 GB. A pass repeats
unchanged on middle and late; at least two windows must pass before official
training. Official promotion requires three fixed runs, mean gain
`>= +0.0005`, no seed below `-0.0005`, and one fixed consensus gain
`>= +0.0005` with slice safety. A first-gate failure closes LambdaMART without
a hyperparameter or blend sweep.

An independent reviewer should allow this because it tests list-grouped
optimization through a model class not previously used on 27K, consumes only
causal audited features, and has a single frozen complementarity check. The
1/32 evaluator remains local evidence, not hidden/full-benchmark proof.
