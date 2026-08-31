# Fresh-context strategic audit — 2026-08-30 23:16 SGT

## Current protected evidence

Run 43 promoted a three-seed equal within-user rank ensemble at local 27K
development-sample primary `0.6501881386335703`. It improved all three
chronological windows, all forward periods, and all fixed slices. This is a
stronger robustness basis than choosing a single high visible score, but it is
still a deterministic 1/32 evaluation sample and not hidden/full-benchmark
evidence.

## Branches not worth repeating now

- DeepFM, field-aware FM, explicit user/content crosses, rare-ID pooling,
  inverse-frequency user weighting, explicit-feedback rates, and creator
  recency all failed their transfer gates.
- Same-impression and within-user pair/list losses failed earlier campaigns;
  the later 27K hard-pair fine-tune restored its parent after both ranking
  epochs regressed. A new ranking-loss sweep would currently be weakly
  justified and expensive.
- Rank 16 was positive but below its frozen materiality gate, while two prior
  cross-capacity/density consensus tests failed. It remains a possible later
  diversity candidate, not the first Run 44 choice.

## Highest-value next bounded question

The three Run 43 members share the same architecture and training protocol.
Their stored predictions are raw FM logits on a common numerical scale. Equal
within-user rank averaging is robust but discards the size of each member's
preference margin. Standard equal logit averaging may reduce seed noise while
retaining agreement strength. This is a distinct, cheap, deterministic
aggregation hypothesis requiring no model retraining and no access to hidden
or public-test labels.

Run 44 therefore tests exactly one alternative: the equal arithmetic mean of
the same three raw logits, with the same member order and no weights, subsets,
calibration, clipping, or alternative transforms. It will be evaluated on the
three chronological shadows before the official development archive is
unlocked. If it fails, the branch closes immediately; there will be no
aggregation sweep.
