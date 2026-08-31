# Run 18 decision journal

## 2026-08-29 20:23 SGT — field-aware family opened

- Run 17 showed that a generic nonlinear tower overfits and damages top-list
  ordering. Run 18 instead changes the inductive bias of pair interactions.
- Fixed rank 8 controls the field-aware table's memory footprint; it is not
  selected from benchmark scores.
- Parent: Run 16 attempt 8 on the same shadow split. Fallback remains Run 16
  seed 2028 official validation `0.6537467530366082`.

## 2026-08-29 20:31 SGT — first gate failed; family closed

- Command succeeded in 103.717 seconds with 9,652,256,768-byte peak RSS.
- Field-aware validation primary: `0.623862295`; paired content-FM parent:
  `0.636106651`; change: `-0.012244356`.
- Field-aware forward primary: `0.625255762`; parent: `0.641647569`; change:
  `-0.016391807`.
- All five activity/date slices regressed. The minimum slice fell from
  `0.573007340` to `0.554531866`, a change of `-0.018475474`.
- Decision: reject and close Run 18 after one counted attempt. Do not tune rank,
  learning rate, batch size, or epochs after the failed architecture gate.
