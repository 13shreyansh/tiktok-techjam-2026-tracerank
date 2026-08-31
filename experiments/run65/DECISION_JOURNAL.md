# Run 65 decision journal

## 2026-08-31 08:37 SGT — midpoint high-activity blend frozen

- Ordinary users receive exact Run61.
- Users above the fixed training-activity upper tertile receive exactly
  `0.5 * Run61 + 0.5 * Run52` in within-user rank space.
- Begin with early only. Preserve Run52.
- All 60 tests passed before opening the run.

## 2026-08-31 08:38 SGT — validation gain misses gate

- Attempt 1 completed successfully in `6.311961` seconds with
  `3,363,045,376`-byte peak RSS.
- Validation primary improved `+0.0001612512807933`, GAUC
  `+0.0001628008424297`, nDCG@5 `+0.0001597017191567`, below the frozen
  `+0.00025` validation gate.
- Forward primary improved `+0.0002994301760143` and passed its gate.
- Cold/low improved `+0.0000949539624020`, medium `+0.0008699618058720`;
  high activity regressed `-0.0008893458736898`, early dates
  `-0.0003429566470923`, and late dates `-0.0002493850678525`, all inside
  the `-0.001` floor.
- The ignored 4,254,072-byte prediction SHA-256 is
  `f9b47fb73fc3f9b094600d6b8059c90827a934e2c38b86bd1a777139fdd3eefa`.
- Stop without middle, late, official, or alternate blend/cutoff.
