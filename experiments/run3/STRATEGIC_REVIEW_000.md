# Strategic review 000 — fresh campaign audit

## Evidence read without relying on the live narrative

- Run 2 ledger: 37 attempts, 35 successes, 2 failures, zero public-test
  evaluations.
- Exact fallback: six-seed within-user rank ensemble, primary 0.605400885.
- Best single causal-history models: approximately 0.60418-0.60466 across exact
  packaging replications.
- Most architecture additions were rejected: DIN, GRU, labeled negative
  history, explicit match features, profile features, primary-tag history,
  user-balanced loss, auxiliary targets, target-rate buckets, and listwise
  fine-tuning.
- The useful Run 2 gain came mainly from seed and model-construction diversity
  plus within-user rank aggregation.
- Earlier LightGBM ranking attempts scored 0.59646 without history and 0.58922
  with weak aggregate rates; they do not test a strong leakage-safe numeric
  aggregate classifier.

## Third-person assessment

Continuing to alter the same neural history encoder is unlikely to maximize the
chance of winning. The current model already captures ID interactions and a
short positive history, but it does not explicitly expose stable counts,
smoothed rates, recency trends, user-category affinity, or item momentum. The
large gap is a missing model family and stronger validation, not more parameter
tuning.

## Decision

Build three paired chronological parent baselines, then test one tree-based
family using numeric, training-only aggregate features. Rates for validation
must use training dates only; training features must be leave-one-out or causal.
Do not access public-test labels. Reject the family quickly if it cannot improve
at least two windows or if gains are smaller than measured noise.

## Win-alignment questions

- Does this work create a genuinely different source of signal? **Yes.**
- Could it improve only the familiar official validation split? **The three
  paired windows are designed to detect that.**
- Is the expected upside materially larger than another same-model tweak?
  **Yes, but unproven until the first family completes.**
- Is the fallback protected? **Yes; Run 2 artifacts and commit remain intact.**
- What would cause an immediate pivot? **Negative median paired gain, a late
  window loss above 0.0005, leakage evidence, or runtime beyond ten minutes.**
