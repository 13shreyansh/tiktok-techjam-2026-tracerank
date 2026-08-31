# Run 60 report: neutral unknown initialization rejected

Run60 corrected an implementation defect in the intended initialization of
trainable unknown/missing embedding rows. The exact protected Run52 rank-32
configuration was retained; only the ineffective advanced-index zero operation
was replaced by an actual in-place fill. Unknown rows remained trainable. All
58 tests passed before scoring.

The one attempt completed successfully but did not improve. Versus exact
Run52, early primary regressed `-0.0003826089685504`, GAUC regressed
`-0.0002979030931107`, nDCG@5 regressed `-0.0004673148439900`, and forward
primary regressed `-0.0003205480648617`. Every fixed slice was also mildly
negative, with the largest decline `-0.0006317774454260` on high activity.

The subprocess took `557.108509` seconds and peaked at `28,753,444,864` bytes
RSS. The ignored 3,786,952,333-byte checkpoint SHA-256 is
`f8fb0d541dbfb992c54caa17405151c9681205c6a518ca8e365f1787b8bf56fc`;
the ignored 6,602,754-byte prediction SHA-256 is
`91976e932b79719f0d51344740868d9016b0fed0945205defbf820455cbd5d8c`.

The intended neutral start is cleaner but not better under the frozen gate, so
no later window, freezing/masking variant, official seed, or consensus follows.
Run52 remains protected at local primary `0.6534977984044839`. These are fixed
1/32 development-sample results, not the full benchmark, hidden test,
submission, or leaderboard. The 72-hour campaign continues in a new bounded
run.
