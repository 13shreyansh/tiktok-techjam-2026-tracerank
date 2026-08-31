# Run 13 caption-content history protocol

Run tag: `run13-caption-history`
Branch: `codex/run13-caption-history`
Started: 2026-08-29 16:18 SGT

## Objective

Test whether official video captions improve target-aware history matching by
representing semantic similarity beyond exact video IDs, starter tags, and
hierarchical categories. Fit a deterministic, label-free character n-gram
TF-IDF/SVD representation to the official text for all 7,583 Pure videos, then
add its projected vector to both candidate and historical-video embeddings.

## Fixed representation, candidate, and gate

- Text is `caption + show_cover_text`; missing text maps to an all-zero vector.
- TF-IDF uses character 2-4 grams, minimum document frequency 2, sublinear term
  frequency, and at most 50,000 terms.
- Truncated SVD uses 16 components, 7 iterations, and random seed 2026; each
  nonzero video vector is L2-normalized.
- The SVD table is frozen. One learned linear projection, initialized with
  standard deviation 0.01, maps it into the model's 16-dimensional history
  space. No caption label or validation result enters the representation.
- Paired parent: Run 8 early control, 0.616858721 validation and 0.603960752
  forward, seed 2027.
- Candidate: the paired parent plus caption-content vectors. Every other parent
  setting remains fixed.
- Require at least +0.001 validation, no forward loss beyond 0.0005, and no
  material activity/date regression before multi-window or seed promotion.
- If it fails, stop caption-content search; do not tune vocabulary size,
  n-gram range, SVD width, or projection scaling on the same window.

Count every attempt up to 50, stop within six hours, enforce a ten-minute
subprocess timeout, and write a fresh strategic review after the family or
eight attempts. Keep public-test labels locked and preserve the exact
0.605400885 fallback. Do not submit, upload, push, contact organizers, use
credentials, change registration, or change repository visibility.
