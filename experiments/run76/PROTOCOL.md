# Run 76 protocol: causal dense LambdaMART rank consensus

Started: **2026-08-31 12:22:00 SGT**.

## Independent question

Does a user-grouped list-ranking tree over audited causal dense features add
stable nonlinear ordering signal to exact Run52?

## Frozen candidate

- Training rows: every eligible row in the declared split, stably grouped by
  user. Relevance is the binary long-view label. Because LightGBM enforces a
  10,000-row query maximum, an oversized user's stable rows are partitioned
  into contiguous chunks of at most 10,000 without mixing users or dropping
  rows; no score existed when this compatibility rule was added.
- Features only: `log1p(duration)`, tab, primary tag, upload type, video type,
  all eight Run52 causal user-history fields, all four prior-day item/author
  fields, and all four exact user-author/user-video repeat fields.
- Raw user/video/author identity, date/time, future outcomes, rejected explicit
  actions, recent sequence, recency, topic additions, and text are excluded.
- LightGBM 4.6.0 `lambdarank`, NDCG@5, truncation level 5, learning rate 0.05,
  31 leaves, minimum 1,000 rows per leaf, 63 bins, all features, no bagging,
  maximum 200 rounds, and 20-round early stopping. Deterministic column-wise
  CPU training, 16 threads, seed 2027.
- Candidate score is one equal within-user percentile-rank vote from the tree
  and one from the exact matching Run52 stored prediction. No coefficient,
  tree parameter, feature, subset, raw-score blend, route, or calibration.

## Gates and stopping

- Begin with exact Run52 seed-2027 `shadow_early` only.
- The fixed consensus must improve validation and forward primary each
  `>= +0.0005`, keep GAUC and nDCG@5 deltas each `>= -0.0005`, keep every fixed
  slice delta `>= -0.001`, peak below 60,000,000,000 bytes RSS, and produce a
  finite model/prediction artifact.
- A pass repeats unchanged on `shadow_middle` and `shadow_late`; at least two
  of three windows must pass the same aggregate/safety gates.
- Only then run the three matching official parent seeds. Require paired mean
  gain `>= +0.0005`, no seed below `-0.0005`, span `<= 0.002`, and every fixed
  official slice `>= -0.001`.
- Only after seed stability form one fixed equal within-user rank consensus of
  the three tree-enhanced seed predictions. Promote over Run52 only at primary
  gain `>= +0.0005`, both components `>= -0.0003`, and every slice
  `>= -0.0005`.
- Stop at the first failed gate, convergence, resource/artifact failure,
  50 attempts, or six hours. Closing Run76 does not stop the 72-hour campaign.

## Environment evidence

Source SHA-256 before scoring:
`55dffacc5d6b37116e29ba4c3743ada6f87eac659b5da9b0e3fffadacf0e063a`.
All 76 tests, isolated-cache bytecode compilation, diff checks, LightGBM import,
and a two-query synthetic `lambdarank` fit passed. The repo-local OpenMP
runtime, exact checksums, URLs, licence, and SBOM are recorded in
`docs/LIBOMP_RUNTIME_PROVENANCE.md`; no system path was changed.

Scores remain deterministic 1/32 development-sample evidence, not the full
benchmark, hidden test, submission, or leaderboard. Public-test labels and
external actions remain locked.
