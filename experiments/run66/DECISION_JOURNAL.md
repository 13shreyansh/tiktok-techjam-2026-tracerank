# Run 66 decision journal

## 2026-08-31 08:42 SGT — bipartite interaction groups frozen

- Every protected field belongs to exactly one frozen interaction side.
- Keep every field's sparse linear effect; remove only same-side latent pairs.
- Begin with seed-2027 early only. Preserve Run52.
- All 61 tests passed before opening the run.

## 2026-08-31 08:52 SGT — bipartite interaction gate fails

- Attempt 1 completed successfully in `555.888698` seconds with
  `27,523,858,432`-byte peak RSS.
- Early primary regressed `-0.0023992163810768`, GAUC
  `-0.0019601430564387`, nDCG@5 `-0.0028382897057148`, and forward primary
  `-0.0021708443795506` versus Run52.
- Every fixed slice regressed: cold/low `-0.0019051169481528`, medium
  `-0.0019221714599633`, high `-0.0056050698637347`, early dates
  `-0.0015865920756276`, and late dates `-0.0026779519196061`.
- The ignored 3,786,952,285-byte checkpoint SHA-256 is
  `315e9c7e6008d6744e386a7d5c69e632e35308aba0b00d93787edc04ee4da48e`;
  the ignored 6,634,553-byte prediction SHA-256 is
  `1f4725e43d3f37ff8e2216e5e48503402784fde3b423311492b10a1f44fa48fe`.
- Stop the interaction-mask family. No alternate grouping, residual,
  middle/late window, official seed, or ensemble follows.
