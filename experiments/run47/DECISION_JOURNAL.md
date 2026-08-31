# Run 47 decision journal

## 2026-08-30 23:56 SGT — route frozen before score

- Run 43 remains protected at local 27K development-sample primary
  `0.6501881386335703`.
- The route uses the already established upper training-activity tertile; it is
  not selected from a threshold sweep. The route reads no outcome label.
- Score early once. If validation or forward gains less than `+0.0003`, close
  before any additional feature build or routing variation.

## 2026-08-31 00:00 SGT — attempt 1 excluded after cutoff defect

- Attempt 1 completed and remains counted, but its routing metadata reported
  cutoff `52.0` while the same evaluation's robustness upper cutpoint was
  `106.0`. The helper incorrectly took a quantile across unique training users
  instead of the existing validation-row-weighted activity population.
- No Run 47 decision is made from attempt 1. Correct the implementation to
  derive the cutoff from `activity[valid_users]`, add a regression test, and
  rerun the otherwise unchanged command as attempt 2. This is an error recovery,
  not a new threshold or hypothesis.

## 2026-08-30 23:59 SGT — corrected route fails; close

- Attempt 2 used cutoff `106.0`, exactly matching the robustness upper
  cutpoint, and routed 284,656 validation rows from 2,686 users. Cold/low and
  medium predictions remained identical to Run 43 as required.
- Corrected validation reached `0.6340668646760825`, a gain of
  `+0.0001789779986697`; forward reached `0.6360483014254156`, a change of
  `-0.0000502042058407`. The high-activity slice gained
  `+0.0015700308002025` but both aggregate gates failed.
- Close without another threshold, soft gate, middle/late build, or official
  evaluation. Preserve Run 43 and move to a different signal family.
