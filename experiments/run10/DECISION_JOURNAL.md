# Run 10 decision journal

## 2026-08-29 15:47 SGT — campaign start

- Protected fallback: official validation primary 0.605400885.
- The prior watch-ratio auxiliary was plain squared error and is not evidence
  against the paper's right-censored likelihood.
- Upstream CWM source has no explicit licence; its local clone is ignored and
  only provenance/checksums are committed.
- Predeclared one candidate at auxiliary weight 0.1, `c_inv=40`, `sigma=2`.

## 2026-08-29 15:54 SGT — attempt 001 rejected

- Candidate validation: 0.613846302, a change of -0.003012419 from the paired
  parent.
- Candidate forward validation: 0.601552606, a change of -0.002408147.
- All five robustness slices regressed; the largest decline was -0.004919455
  for high-activity users.
- The successful command used 296.16 wall seconds and 5,373,296,640 maximum
  resident bytes. Public-test labels were not evaluated.
- Decision: reject and stop this family without tuning auxiliary weight,
  inverse cost, or sigma. Preserve the 0.605400885 fallback.
