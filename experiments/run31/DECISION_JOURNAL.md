# Run 31 decision journal

## 2026-08-30 00:59 SGT — lower-step family opened after Run 30 convergence

- Run 30 produced a large, stable density gain and closed at its predeclared
  convergence stop; further work must be a separately disclosed run.
- Its best epoch moved from 3 on early to 2 on middle/late and 1 on every
  official seed. This consistent train-window pattern suggests the original
  step size may be too aggressive for denser training rather than indicating
  a seed-specific accident.
- Test one narrow intervention: learning rate 0.0005. Preserve every other
  model, data, evaluator, robustness, and stopping setting. The protected Run
  30 seed-2028 checkpoint at `0.636251719` remains untouched.

## 2026-08-30 01:02 SGT — attempt 1 fails; Run 31 closed

- Attempt `001-lr0005-history-item-shadow-early` completed in 106.12 seconds
  with maximum RSS 3,918,659,584 bytes. Best epoch moved to 5, but primary fell
  from `0.621415726` to `0.620468420` (`-0.000947306`). Forward fell
  `-0.000785125`.
- Every protected slice regressed: cold/low `-0.000651694`, medium
  `-0.001145316`, high `-0.001559055`, early dates `-0.000994828`, and late
  dates `-0.000532470`. The candidate fails validation, forward, and slice
  gates.
- Close the family without trying an intermediate learning rate. Run 30's
  seed-2028 `0.636251719` checkpoint remains protected. The next independent
  question should follow the demonstrated density scaling signal rather than
  micro-tune this failed optimizer branch.
