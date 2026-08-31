# Run 23 decision journal

## 2026-08-29 20:52 SGT — regularized wide-cross family opened

- Run 22 improved every validation slice but missed the forward guard by
  `0.001164701` beyond tolerance. Direct shrinkage is a principled response to
  temporally unstable memorization.
- Coefficient 0.01 is fixed once; this run will not become a validation-driven
  regularization sweep.
- This is an autonomous family transition under the active goal; no new human
  model configuration or score was supplied.
- Protected fallback remains Run 16 seed 2028 at `0.6537467530366082`.

## 2026-08-29 20:54 SGT — fixed shrinkage failed; branch closed

- Command succeeded in 71.142 seconds with 3,119,480,832-byte peak RSS.
- Validation changed from the Run 16 parent `0.636106651` to `0.642455467`
  (`+0.006348816`), but forward changed from `0.641647569` to `0.640082951`
  (`-0.001564619`).
- Relative to Run 22, the result changed by only `-0.000001240` validation and
  `+0.000100083` forward. Coefficient 0.01 did not materially shrink the branch.
- Decision: reject and close Run 23. Do not sweep regularization strength. Shift
  the active search to the independently acquired KuaiRand-27K long-sequence
  benchmark after checksum verification.
