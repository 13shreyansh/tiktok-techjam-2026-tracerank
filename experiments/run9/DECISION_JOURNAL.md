# Run 9 decision journal

## 2026-08-29 15:40 SGT — campaign start

- Protected fallback: official validation primary 0.605400885.
- Paired early control from Run 8: 0.616858721 validation and 0.603960752
  forward.
- One predeclared architecture: two full-rank cross layers in parallel with the
  existing deep tower; no parameter sweep after observing the result.

## 2026-08-29 15:44 SGT — attempt 001 rejected

- Candidate validation: 0.616292357, a change of -0.000566363 from the paired
  parent. It missed the required +0.001 validation gain.
- Candidate forward validation: 0.604613423, a change of +0.000652671.
- All five robustness slices were below the parent; the largest decline was
  -0.001339921 for high-activity users.
- The successful command used 215.64 wall seconds and 3,815,112,704 maximum
  resident bytes. Public-test labels were not evaluated.
- Decision: reject the architecture, preserve the 0.605400885 fallback, and
  stop this family without a layer/rank/width/learning-rate sweep.
