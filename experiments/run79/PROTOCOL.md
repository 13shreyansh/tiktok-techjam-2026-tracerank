# Run 79 protocol: chronological out-of-fold parent-aware LambdaMART residual

Started: **2026-08-31 12:53:26 SGT**. This conservative start includes the
split implementation and causal-sidecar construction, before any model score.

## Independent question

Does Run76's forward list-ranking signal become stable when the tree learns a
chronologically out-of-fold correction to its parent rather than an equal vote
trained on the parent's in-sample rows?

## Frozen construction

- Supporting parent: exact Run52 `history_item_repeat` sparse FM, rank 32,
  seed 2027, legacy unknown initialization, learning rate 0.001, batch 65,536,
  maximum 20 epochs, patience four. Train April 8–9, predict April 10 and 11.
- Meta-train: April 10 deterministic evaluation-sample rows. Meta-validation:
  April 11 deterministic evaluation-sample rows. Neither date trained the
  supporting parent.
- Features: Run76's 21 audited causal dense fields plus the supporting parent's
  within-user percentile rank. Raw user/video/author identity, raw date/time,
  future outcomes, actions, text, rejected histories, and test data are absent.
- Tree: LightGBM 4.6.0 `lambdarank`, NDCG@5, truncation five, learning rate
  0.05, 31 leaves, minimum 1,000 rows per leaf, 63 bins, maximum 200 rounds,
  20-round early stopping, deterministic column-wise CPU training, 16 threads,
  seed 2027. Oversized same-user queries use the already-tested stable 10,000
  row partition with exact row conservation.
- The within-user parent rank is the LightGBM `init_score`. The frozen tree
  output is added to the matching parent rank; no blend coefficient, route,
  calibration, feature subset, or tree parameter is searched.
- Target gate: apply the frozen correction to exact Run52 seed-2027
  `shadow_early` April 12–14 validation and April 15–17 forward predictions,
  using causal sidecars frozen at April 11.

## Gates and stopping

- The supporting parent is counted as attempt 1 and must produce finite,
  aligned April 10/11 predictions and a valid hashed checkpoint.
- The residual is attempt 2. Its final meta-validation primary on April 11 must
  beat its parent rank by `>= +0.0003` with GAUC and nDCG@5 each `>= -0.0005`.
- On the protected target, validation and forward primary must each improve
  exact Run52 by `>= +0.0003`; GAUC and nDCG@5 deltas must each be
  `>= -0.0005`; every fixed robustness slice must be `>= -0.001`; peak RSS
  must remain below 60,000,000,000 bytes; model and prediction artifacts must
  be finite and hashed.
- A first-gate failure closes this residual configuration without parameter,
  feature, blend, or cutoff tuning. A pass repeats the same chronological
  construction on later windows before any official three-seed promotion.
- Stop at convergence, the first failed gate, an artifact/resource failure,
  50 attempts, or six hours. Closing Run79 closes only this hypothesis; it does
  not stop the 72-hour campaign.

No public-test or hidden labels, upload, submission, push, organizer contact,
registration change, or repository-visibility change is authorized.
