# Run 69 decision journal

## 2026-08-31 09:19 SGT — entire-space funnel frozen

- Early training has 41,010,906 rows; long-view rate `0.2580331681`, click
  rate `0.3761665007`, and `P(click | long_view)=0.9927932578`.
- Use the primary ESMM factorization without a tunable task coefficient.
- Share latent interactions to control memory; keep separate sparse linear
  heads for click and conditional long view.
- Begin with seed-2027 early only. Preserve Run52.
- All 65 tests and bytecode compilation passed before opening the run.

## 2026-08-31 09:32 SGT — entire-space funnel gate fails

- Attempt 1 completed successfully in `732.257255` seconds with
  `29,608,329,216`-byte peak RSS.
- Early primary regressed `-0.006267336552150726`, GAUC
  `-0.004435765308803186`, nDCG@5 `-0.008098907795498156`, and forward
  primary `-0.006994462133835477` versus exact Run52.
- Every fixed slice regressed: cold/low `-0.004848112131069837`, medium
  `-0.008348362389651198`, high `-0.00859225263258001`, early dates
  `-0.0037778262765606474`, and late dates `-0.00613352694680358`.
- The ignored 3,900,845,725-byte checkpoint SHA-256 is
  `11954e3e20e93aa4a7375eb52dcccd39262bde85e751e553ce84d7bf6499fb38`;
  the ignored 6,474,068-byte prediction SHA-256 is
  `0ce13c0805b6fff347fc880d164c5618dcfd5e78ca785563379c941b62ba7b13`.
- Stop the entire-space funnel family. No task-weight, head, latent-sharing,
  action-union, later-window, official-seed, or ensemble variant follows.
