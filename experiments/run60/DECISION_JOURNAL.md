# Run 60 decision journal

## 2026-08-31 08:16 SGT — unknown-initialization correction frozen

- Use exact protected Run52 rank-32 settings.
- Correct only the intended unknown/missing row initialization; rows remain
  trainable.
- Begin with seed-2027 early only. Preserve Run52.
- All 58 tests passed before opening the run.

## 2026-08-31 08:26 SGT — unknown-initialization gate fails

- Attempt 1 completed successfully in `557.108509` seconds with
  `28,753,444,864`-byte peak RSS.
- Early primary regressed `-0.0003826089685504`, GAUC
  `-0.0002979030931107`, nDCG@5 `-0.0004673148439900`, and forward primary
  `-0.0003205480648617` versus exact Run52.
- Every fixed slice was mildly negative: cold/low `-0.0003282626909842`,
  medium `-0.0004154583873868`, high `-0.0006317774454260`, early dates
  `-0.0003103781519754`, and late dates `-0.0003191483829156`.
- The ignored 3,786,952,333-byte checkpoint SHA-256 is
  `f8fb0d541dbfb992c54caa17405151c9681205c6a518ca8e365f1787b8bf56fc`;
  the ignored 6,602,754-byte prediction SHA-256 is
  `91976e932b79719f0d51344740868d9016b0fed0945205defbf820455cbd5d8c`.
- Stop after one attempt. No later window, freezing/masking variant, other
  initialization, official seed, or consensus follows.
