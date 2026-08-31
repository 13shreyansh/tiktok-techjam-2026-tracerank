# Run 75 decision journal

## 2026-08-31 12:14 SGT — collaborative profile frozen

- Run74 closed global training order after every aggregate and slice regressed.
- The new mechanism uses exact Run52 video vectors and training positives to
  match a different candidate to the user's positive history.
- Slot preservation prevents unsupported candidates from receiving arbitrary
  tie ranks or cold-item penalties.
- Freeze positive exposure weighting, cosine, equal voting, parent membership,
  split order, seed order, and all gates before scoring.
- Begin with seed-2027 early only. Preserve Run52.
- All 75 tests, isolated-cache bytecode compilation, and diff checks passed.

## 2026-08-31 12:15 SGT — first gate failed; branch closed

- The command exited zero in `10.479538` wrapper seconds and peaked at
  `6,708,346,880` bytes RSS.
- The training-only profile used 10,582,174 positive exposures from 25,904
  users. It supported 422,189 validation rows and 300,735 forward rows.
- Versus exact Run52, validation primary changed `-0.0148223688068639`,
  GAUC `-0.0172306770585478`, and nDCG@5 `-0.0124140605551800`.
  Forward primary changed `-0.0084229486199109`.
- Every fixed slice regressed by at least `-0.0121832853933422`; high activity
  changed `-0.0153969365590679`.
- This is a decisive mechanism failure, not noise. Do not repeat, run other
  windows/seeds, change cosine/profile definitions, reduce its weight, or
  route it. Preserve Run52 and continue the 72-hour campaign elsewhere.
