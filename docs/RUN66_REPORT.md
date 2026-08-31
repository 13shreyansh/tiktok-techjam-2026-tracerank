# Run 66 report: bipartite history-to-candidate FM rejected

Run66 replaced all-pairs FM interactions with one frozen bipartite structure:
user, context, and user histories on one side; candidate identity, content, and
item histories on the other. All fields retained linear effects. The grouping,
rank, training settings, and gates were fixed before scoring, and all 61 tests
passed.

The single attempt completed successfully but regressed early primary
`-0.0023992163810768`, GAUC `-0.0019601430564387`, nDCG@5
`-0.0028382897057148`, and forward primary `-0.0021708443795506` versus exact
Run52. Every fixed slice regressed; high activity was worst at
`-0.0056050698637347`.

The attempt took `555.888698` seconds and peaked at `27,523,858,432` bytes RSS.
The ignored 3,786,952,285-byte checkpoint SHA-256 is
`315e9c7e6008d6744e386a7d5c69e632e35308aba0b00d93787edc04ee4da48e`;
the ignored 6,634,553-byte prediction SHA-256 is
`1f4725e43d3f37ff8e2216e5e48503402784fde3b423311492b10a1f44fa48fe`.

Same-side interactions carry useful signal under this representation, so the
interaction-mask family closes without alternate grouping, residual, later
window, official seed, or ensemble search. Run52 remains protected at local
primary `0.6534977984044839`. These are fixed 1/32 development-sample results,
not the full benchmark, hidden test, submission, or leaderboard. The 72-hour
campaign continues with a different hypothesis.

## Retrospective parent-drift correction

Run72 later proved that Run60's neutral unknown-row initialization remained the
default. Run66 therefore tested bipartite interactions plus neutral unknown
initialization, not the isolated interaction mask claimed above. The combined
candidate is still decisively negative versus both Run52 and exact Run60
(`-0.0020166074125264055` validation, `-0.001850296314688915` forward, and
`-0.0049732924183086835` worst slice versus Run60), so it remains rejected;
the causal attribution to the interaction mask alone is withdrawn.
