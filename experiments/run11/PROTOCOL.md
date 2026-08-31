# Run 11 neural LambdaLoss protocol

Run tag: `run11-neural-lambdaloss`
Branch: `codex/run11-neural-lambdaloss`
Started: 2026-08-29 15:55 SGT

## Objective

Test whether a short metric-aware LambdaLoss fine-tune improves the strong
pointwise history model. Pairwise errors are combined in the same proportions
as the organizer primary: positive-weighted per-user AUC and per-user nDCG@5.

## Fixed candidate and gate

- Paired parent: Run 8 early control, 0.616858721 validation and 0.603960752
  forward, seed 2027.
- Candidate: identical BCE parent followed by at most two LambdaLoss epochs,
  learning rate 0.00002, up to five randomly sampled positives and the twenty
  parent-hardest negatives per user; patience one.
- Require at least +0.001 validation, no forward loss beyond 0.0005, and no
  material activity/date regression before multi-window or seed promotion.
- If the candidate fails, stop this loss family; do not tune learning rate,
  pair counts, or component weights on the same window.

Count every attempt up to 50, stop within six hours, enforce a ten-minute
subprocess timeout, and write a fresh strategic review after the family or
eight attempts. Keep public-test labels locked and preserve the exact
0.605400885 fallback. Do not submit, upload, push, contact organizers, use
credentials, change registration, or change repository visibility.
