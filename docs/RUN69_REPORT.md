# Run 69 report: entire-space click funnel rejected

Run69 adapted the primary ESMM sequential-action factorization to the protected
rank-32 repeat-affinity FM. Shared sparse interactions and separate click and
conditional-long-view linear heads produced a joint long-view probability;
equal click and joint-long-view losses were frozen before scoring. All 65 tests
and bytecode compilation passed.

The single attempt completed successfully but regressed early primary
`-0.006267336552150726`, GAUC `-0.004435765308803186`, nDCG@5
`-0.008098907795498156`, and forward primary `-0.006994462133835477` versus
exact Run52. Every fixed slice regressed; high activity was worst at
`-0.00859225263258001`.

The attempt took `732.257255` seconds and peaked at `29,608,329,216` bytes RSS.
The ignored 3,900,845,725-byte checkpoint SHA-256 is
`11954e3e20e93aa4a7375eb52dcccd39262bde85e751e553ce84d7bf6499fb38`;
the ignored 6,474,068-byte prediction SHA-256 is
`0ce13c0805b6fff347fc880d164c5618dcfd5e78ca785563379c941b62ba7b13`.

The click task creates substantial negative transfer for judged long-view
ranking under this frozen representation, so the family closes without task
weights, alternate heads, later windows, official seeds, or ensemble search.
Run52 remains protected at local primary `0.6534977984044839`. These are fixed
1/32 development-sample results, not the full benchmark, hidden test,
submission, or leaderboard. The 72-hour campaign continues with a different
hypothesis.

## Retrospective parent-drift correction

Run72 later proved that Run60's neutral unknown-row initialization remained the
default. Run69 therefore tested the funnel objective plus neutral unknown
initialization. It remains decisively rejected versus exact Run60 at
`-0.005884727583600369` validation, `-0.006673914068973774` forward, and
`-0.007960475187154037` worst slice, but the loss alone is not assigned the
whole regression.
