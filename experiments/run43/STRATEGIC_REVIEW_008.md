# Run 43 strategic review after eight attempts

Reviewed: **2026-08-30 23:08 SGT**.

## Does the current work advance the objective of winning?

Yes. The fixed three-seed repeat-affinity rank consensus gained
`+0.001002013` on early validation and `+0.001368092` on middle validation,
while forward time and every fixed activity/date slice improved in both
windows. These gains are larger than recent capacity and feature changes,
replicate across time, and require no new labels or model selection.

## Are we drifting or overfitting the development score?

No protocol drift is visible. Seeds 2027/2028/2029, equal one-third weights,
within-user percentile ranks, model configuration, and all gates were frozen
before Run 43 scores. No member, weight, subset, normalization, or parameter
was changed after early or middle results. Official prediction archives remain
unread by the Run 43 evaluator.

## What could still go wrong?

- The late consensus can fail despite its members completing successfully.
- An official ensemble can score below the best individual seed even after
  shadow gains, because seed diversity may differ by training cutoff.
- Fixed development-sample gains do not prove full-benchmark or hidden-test
  generalization.
- Three checkpoints increase artifact and inference complexity; packaging must
  retain exact member order and hashes if promotion occurs.

## Decision

Proceed only with attempt 9: the already-declared equal three-seed late-shadow
consensus. If it passes, unlock exactly one fixed official consensus using the
three existing verified archives. Do not train more seeds, search weights,
change normalization, or introduce another hypothesis inside Run 43.

The protected single seed `0.6492243384881571` remains immutable and available
as fallback. Public-test/hidden labels and external actions remain locked.
