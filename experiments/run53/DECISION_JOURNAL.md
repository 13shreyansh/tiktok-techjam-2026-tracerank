# Run 53 decision journal

## 2026-08-31 06:49 SGT — rank 64 and gates frozen before training

- Run52 supplied three-seed and all-slice evidence for one more exact capacity
  doubling. Rank 64 is the only capacity tested in this run.
- Preserve Run52 and Run49 regardless of score, runtime, or memory outcome.
- Host physical memory is `68,719,476,736` bytes. The frozen operational guard
  is 60,000,000,000-byte peak RSS; no adaptive batch-size rescue is allowed.
- Begin with seed-2027 early shadow only.

## 2026-08-31 07:03 SGT — early gate fails; rank-64 branch closes

- Attempt 1 completed successfully in `801.822829` seconds with
  `45,272,547,328`-byte peak RSS, below the frozen memory guard.
- Rank-64 early primary is `0.6345003457781826`, a regression of
  `-0.0006649932545325` versus the exact rank-32 parent. GAUC regressed
  `-0.0006160701398239` and nDCG@5 regressed `-0.0007139163692410`.
- Forward primary changed only `-0.0001154281760545`, but the required early
  validation gain was `>= +0.00025`. Every fixed primary slice also regressed:
  cold/low `-0.0006094115338365`, medium `-0.0009157586253021`, high
  `-0.0005898996609932`, early dates `-0.0003736139882768`, and late dates
  `-0.0007960130751231`.
- The ignored 7,431,533,773-byte checkpoint SHA-256 is
  `950d76ffde16efcdc3c9a3edf7c013035aad5fc8ddda75d17914e38d61aef96f`;
  the 6,614,916-byte prediction archive SHA-256 is
  `2b30f563a58def1b34949a5a8e82991a003f58495420f0a999e0028e01b8372a`.
- Stop without middle, late, official, alternate-rank, learning-rate, or batch
  experiments. Run52 remains protected and the overall campaign continues.
