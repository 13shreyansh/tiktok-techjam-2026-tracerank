# Strategic audit — 2026-08-31 14:57 SGT

## Evidence after Run80

Run80's standard shallow nonlinear head regressed the exact Run52 parent by
`0.0032981268` primary on its first trained epoch and rolled back exactly.
Recent-history attention, ordinary BPR, tree list correction, additional
categorical fields, multi-action objectives, capacity, optimization changes,
and standard DeepFM interactions have now failed their frozen gates. Run52
remains protected.

## Remaining metric-aligned gap

The protected official-sample consensus has GAUC `0.7066506868` and nDCG@5
`0.6003449100`. The starter documents an empirical nDCG@5 ceiling of `0.7289`,
so top-five ordering remains the larger measurable gap. Run56 tested equal
hard-pair BPR on exact Run52 and found only noise-sized movement. Run11 tested
an explicit primary-aligned LambdaLoss on an older Pure neural model, but no
27K run has applied swap-weighted nDCG@5 plus positive-weighted within-user AUC
directly to the exact protected sparse FM.

Run81 therefore reuses Run11's untuned learning rate `0.00002`, at most five
deterministically sampled positives, the twenty highest-parent-score negatives
per user, equal AUC/nDCG loss components, one trained epoch, and exact rollback.
Unlike equal BPR, nDCG pair weights use each selected row's rank in the user's
full parent-scored training list and the user's exact ideal DCG at five. No
feature, architecture, label, coefficient, sampler, rank, route, or ensemble is
searched.

## Third-person goal check

This is a materially new objective on the strongest representation and directly
matches both organizer metrics. Its main risks are overfitting the top of the
training lists, sparse coverage from sampled positives, and degrading GAUC to
buy nDCG. Require validation and forward primary gains, both component floors,
all established slice floors, exact parent reproduction, finite hashed outputs,
and the 60 GB resource guard. A first-gate failure closes the loss on 27K; it
does not end the 72-hour campaign. All scores remain deterministic development
evidence, not full-benchmark, hidden-test, submission, or leaderboard results.
