# Run 17 decision journal

## 2026-08-29 20:12 SGT — independent DeepFM family opened

- Live source re-read: the official statement says 50 iterations and six hours
  **per benchmark run**. It does not define when a restart is legitimate.
- User correction accepted: convergence closes and documents a run; it is not
  explicit evidence that all hackathon research must stop.
- Conservative safeguard: Run 17 is predeclared before any new score, tests a
  genuinely different architecture family, and will disclose both per-run and
  cumulative resource totals. It is not a micro-tuning continuation of Run 16.
- Protected fallback: Run 16 content sparse FM seed 2028, validation primary
  `0.6537467530366082`.

## 2026-08-29 20:15 SGT — first gate failed; family closed

- Command succeeded in 67.127 seconds with 3,157,721,088-byte peak RSS.
- DeepFM validation primary: `0.626560563`; paired content-FM parent:
  `0.636106651`; change: `-0.009546088`.
- DeepFM forward primary: `0.631056253`; parent: `0.641647569`; change:
  `-0.010591317`.
- All five activity/date slices regressed; the high-activity slice fell by
  `0.021996837`.
- Decision: reject and close Run 17 after one counted attempt. Do not tune
  widths, dropout, learning rates, or epochs after the failed family gate.
