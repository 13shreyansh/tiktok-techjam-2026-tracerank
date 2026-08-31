# Run 35 decision journal

## 2026-08-30 06:56 SGT — fresh strategic audit and run opening

- Run 34 closed correctly at six attempts, but the overall hackathon goal stays
  active. Its protected seed-2028 development score is `0.6450834641517389`;
  the three-seed mean is `0.6448342475838004` and span `0.0004683914104386`.
- Do not repeat already rejected branches: lower pointwise learning rate,
  rank 16, inverse-frequency user balancing, DeepFM, field-aware FM, recent
  trend/extra behavior histories, or fixed rank/seed ensembles. Their prior
  gates were negative or immaterial.
- The unresolved ranking signal is narrower. Earlier random within-user BPR on
  KuaiRand-1K improved forward primary `+0.001208670` but regressed paired
  validation `-0.000332769` and medium activity `-0.001977811`. Random
  same-impression pairs were noise-sized. This does not justify replaying
  either method unchanged.
- Run 35 therefore tests a single ranking-aligned change: hard within-user
  pairs from the frozen pointwise parent, using lowest-scored positives and
  highest-scored negatives. The smaller `0.00005` fine-tune rate and validation
  rollback address the earlier instability. Pair generation sees training
  labels only.
- First add checkpoint-load validation, hard-pair construction, and pairwise
  best-checkpoint rollback with focused unit tests. No scored attempt occurs
  until all tests pass and the code diff is committed.

## 2026-08-30 07:05 SGT — implementation gate passed

- Added exact checkpoint metadata/tensor-shape validation and SHA-256 lineage.
  Checkpoint loading requires pointwise epochs 0, so the parent cannot be
  silently retrained.
- Added deterministic hard within-user pairs: lowest parent-scored positives
  versus highest parent-scored negatives, capped at five per user. Nonfinite
  scores, length mismatches, empty pair sets, and incompatible scope fail
  closed.
- Added pairwise best-checkpoint selection with the loaded parent as epoch 0,
  `0.00001` selection epsilon, and explicit patience. A regressive fine-tune is
  rolled back before forward/slice evaluation and artifact writing.
- Ranker SHA-256 is
  `a488786ee7e2a629838689e99d4201a4b33ef7b0769976ee4b3bcdf0b75e07d2`.
  Python compilation passed. The standard-library suite passed 45 tests with
  zero failures in 0.261 seconds. Commit the implementation before attempt 1.

## 2026-08-30 07:01 SGT — attempt 1 failed the gate; Run 35 closed

- The command completed successfully in 31.33 seconds with maximum RSS
  18,265,079,808 bytes. It loaded checkpoint SHA-256
  `2492fc6f11caf75596244a1ac932b0d5ec8083f6062ed6479a0de14937bcc39f`
  and constructed 128,765 hard pairs from 25,883 usable users.
- Parent reproduction was exact at validation `0.6296437130222816`. Pairwise
  epoch 1 scored `0.6295735681162747` (`-0.0000701449060069`); epoch 2 scored
  `0.6294655955696862` (`-0.0001781174525954`). Neither cleared the selection
  epsilon, so patience stopped the stage and restored pairwise epoch 0.
- Final validation, forward, and every fixed slice exactly equal Run 34.
  Independently loaded valid and forward prediction arrays are bit-for-bit
  equal with maximum absolute difference `0.0`.
- The required `+0.0005` early-validation gain was not met. Close Run 35 after
  attempt 1 without a learning-rate, pair-count, or sampling-rule sweep. The
  protected Run 34 seed-2028 candidate remains unchanged. The overall goal
  remains active and requires a fresh hypothesis.
