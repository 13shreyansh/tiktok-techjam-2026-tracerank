# Strategic audit — 2026-08-31 12:53 SGT

## Evidence after Runs 76–78

Run76 established a small but temporally promising list-ranking signal: its
fixed LambdaMART/parent consensus changed early validation primary only
`+0.0000588416694892`, but forward primary `+0.0006535903495063` and forward
nDCG@5 `+0.0015016265840292`. The equal-vote candidate failed its frozen gate.
Runs77 and 78 then rejected target-aware attention over five recent positive
tags and over aligned tag/creator identities; their first trained epochs lost
`0.0014922937784717` and `0.0012762197489246` primary respectively, and both
rolled back exactly to Run52.

## Methodological problem

Run76 trained the tree on the same rows used to train its FM parent. That is
valid as an ordinary ensemble, but it is unsafe for a residual learner because
the parent scores are in-sample and can make correction patterns look easier
than they will be later. Repeatedly tuning the blend or tree on the protected
window would compound local-sample overfitting. The next test must first ask
whether the tree correction transfers when both its parent scores and labels
are chronologically out of sample.

## Run79 selection

Create a new `stack_early` split: fit an exact Run52 rank-32 parent only on
April 8–9, use its April 10 predictions and labels to fit one conservative
LambdaMART correction, and use April 11 only for early stopping. The correction
receives the 21 audited causal dense fields plus the parent's within-user rank.
The parent rank is also the LightGBM initial score, so the tree is explicitly a
correction rather than an equal independent vote. Apply the frozen correction
unchanged to exact Run52's April 12–14 validation and April 15–17 forward
predictions.

This is a new anti-leakage mechanism, not parameter tuning of Run76. The parent
architecture, tree configuration, features, dates, seed, aggregation, and gates
are frozen before scoring. Require improvement on both April 11 meta-validation
and the later protected validation/forward windows; preserve Run52 regardless.
All scores remain deterministic 1/32 development-sample evidence, not the full
benchmark, hidden test, submission, or leaderboard.
