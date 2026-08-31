# Run 67 decision journal

## 2026-08-31 08:55 SGT — positive class balance frozen

- Derive the sole positive multiplier from training labels; do not tune it.
- Keep exact Run52 rank-32 model, features, and inference.
- Begin with seed-2027 early only. Preserve Run52.
- All 62 tests passed before opening the run.

## 2026-08-31 09:06 SGT — full class-balance gate fails

- Attempt 1 completed successfully in `570.768732` seconds with
  `28,662,775,808`-byte peak RSS. The training-derived positive multiplier was
  `2.875470768104928`.
- Early primary regressed `-0.002635812557784223`, GAUC
  `-0.0020147203650840995`, nDCG@5 `-0.0032569047504844573`, and forward
  primary `-0.001973318010540903` versus exact Run52.
- Every fixed slice regressed: cold/low `-0.0026239995189378806`, medium
  `-0.0021275398684342806`, high `-0.004088845108808026`, early dates
  `-0.001656180518430972`, and late dates `-0.002753281097485738`.
- The ignored 3,786,952,349-byte checkpoint SHA-256 is
  `4436bad4796b7d15693e2746c7b519edcff6b44801206b8d232b40ac2c37f568`;
  the ignored 6,683,405-byte prediction SHA-256 is
  `867d06ab8967ff5babaf8df32607e33b5283ba0702bee52dee6bceea74d6b5cb`.
- Stop the class-balance family. No alternate weight, clipping, focal variant,
  later window, official seed, or ensemble follows.
