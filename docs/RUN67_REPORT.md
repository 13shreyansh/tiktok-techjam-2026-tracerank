# Run 67 report: full positive class balance rejected

Run67 applied one untuned positive BCE multiplier equal to training negatives
divided by training positives (`2.875470768104928`) to exact Run52. Features,
rank, initialization, optimizer, splits, inference, and gates were frozen before
scoring, and all 62 tests passed.

The single attempt completed successfully but regressed early primary
`-0.002635812557784223`, GAUC `-0.0020147203650840995`, nDCG@5
`-0.0032569047504844573`, and forward primary `-0.001973318010540903` versus
exact Run52. Every fixed slice regressed; high activity was worst at
`-0.004088845108808026`.

The attempt took `570.768732` seconds and peaked at `28,662,775,808` bytes RSS.
The ignored 3,786,952,349-byte checkpoint SHA-256 is
`4436bad4796b7d15693e2746c7b519edcff6b44801206b8d232b40ac2c37f568`;
the ignored 6,683,405-byte prediction SHA-256 is
`867d06ab8967ff5babaf8df32607e33b5283ba0702bee52dee6bceea74d6b5cb`.

Full global class balancing overcorrects the protected ranking objective, so
the family closes without weight variants, later windows, official seeds, or
ensemble search. Run52 remains protected at local primary
`0.6534977984044839`. These are fixed 1/32 development-sample results, not the
full benchmark, hidden test, submission, or leaderboard. The 72-hour campaign
continues with a different hypothesis.

## Retrospective parent-drift correction

Run72 later proved that Run60's neutral unknown-row initialization remained the
default. Run67 therefore tested class balancing plus neutral unknown
initialization. It remains decisively rejected versus exact Run60 at
`-0.0022532035892338653` validation, `-0.0016527699456792` forward, and
`-0.003457067663382052` worst slice, but the isolated class-balancing effect is
not claimed.
