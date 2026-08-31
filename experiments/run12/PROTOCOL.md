# Run 12 hierarchical category-history protocol

Run tag: `run12-category-history`
Branch: `codex/run12-category-history`
Started: 2026-08-29 16:09 SGT

## Objective

Test whether official content-side hierarchical categories improve the strong
target-aware history model beyond its original 111 tag combinations. Add one
categorical three-level path to each candidate and to each positive history
event; keep every other parent setting fixed.

## Fixed candidate and gate

- Paired parent: Run 8 early control, 0.616858721 validation and 0.603960752
  forward, seed 2027.
- Candidate: parent plus the official first/second/third-level category path
  as both a regular field and an additive candidate/history attention signal.
- Require at least +0.001 validation, no forward loss beyond 0.0005, and no
  material activity/date regression before multi-window or seed promotion.
- If it fails, stop category-history search; do not tune hierarchy depth,
  embedding width, or category/tag weights on the same window.

Count every attempt up to 50, stop within six hours, enforce a ten-minute
subprocess timeout, and write a fresh strategic review after the family or
eight attempts. Keep public-test labels locked and preserve the exact
0.605400885 fallback. Do not submit, upload, push, contact organizers, use
credentials, change registration, or change repository visibility.
