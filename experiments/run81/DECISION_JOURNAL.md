# Run 81 decision journal

## 2026-08-31 14:57 SGT — primary-aligned loss selected

- Run80 safely rejected standard higher-order DeepFM interactions. The protected
  representation remains Run52.
- The largest organizer-metric gap is nDCG@5, and exact Run52 has only seen BCE
  and equal hard-pair BPR. Freeze the previously audited Run11 LambdaLoss
  defaults and improve its rank weighting by using exact full parent-list ranks.
- Begin with one exact seed-2027 early attempt. Preserve Run52 regardless of the
  result and keep public/hidden evaluation locked.

## 2026-08-31 15:02 SGT — attempt 1 rejected and exact parent restored

- Epoch zero reproduced both stored parent arrays with maximum absolute error
  `0.0`. Construction used 25,883 usable users, 128,849 selected positives,
  513,587 hard negatives, and 19,171 users with nonzero top-five swap weights.
- The trained epoch regressed validation GAUC `-0.0211876477586898`, nDCG@5
  `-0.0335669496275842`, and primary `-0.0273772986931370`. Forward primary
  regressed `-0.0288984309742814`. All five fixed slices regressed between
  `-0.0177642464261869` and `-0.0337121869129439`.
- Exact rollback selected epoch zero. The final finite prediction archive has
  SHA-256 `8d2392915731af585177bbb79287fc391629dea2fbce9f1faab0c965db911872`,
  byte-identical to Run52. The wrapper completed in `78.51258707046509`
  seconds at `29,959,077,888` bytes peak RSS.
- Stop without rate, cap, sampler, weight, epoch, blend, window, or seed search.
  Run52 remains protected; closing this loss does not stop the campaign.
