# Run 70 report: recurring time context rejected

Run70 appended Asia/Shanghai hour-of-day and weekday categorical interactions
to the protected Run52 rank-32 repeat-affinity sparse FM. The configuration,
early/forward split, parent, seed, evaluator, and promotion gates were frozen
before scoring. All 67 tests and bytecode compilation passed before the run.

The single counted attempt completed successfully. Versus exact Run52,
validation primary changed `-0.0001767074512381006`, GAUC
`-0.00027586647815647236`, and nDCG@5 `-0.00007754842431983988`. Forward
primary improved `+0.00036272161371619926`, but forward GAUC changed
`-0.00016697906000517904`. High-activity primary was the worst fixed slice at
`-0.0019364014300199406`, outside the frozen `-0.001` limit.

The counted attempt took `874.084590` seconds and peaked at
`27,723,776,000` bytes RSS. The ignored 3,786,956,725-byte checkpoint SHA-256
is `126f683f8ba82810ff60033953c4b7a34f50499a39ac8ce94e090ba2816cf449`;
the ignored 6,617,418-byte prediction SHA-256 is
`95da5fb49a9be61b19b2208b86252cb0387a2f902d1c4b941e4f257be16c05e5`.
The first launch was separately disclosed as interrupted and unscored because
it produced no result, artifact, ledger row, or iteration increment.

Recurring time context does not transfer robustly enough to justify more
compute. Run70 closes after one counted experiment without alternate time bins,
timezones, dates, later windows, official seeds, or blend search. Run52 remains
protected at local primary `0.6534977984044839`. These scores are from a fixed
deterministic 1/32 development sample, not the full benchmark, hidden test,
submission, or leaderboard. The 72-hour campaign continues with a different
hypothesis.

## Retrospective parent-drift correction

Run72 later proved that Run60's neutral unknown-row initialization remained the
default. Run70 therefore measured time context plus neutral unknown
initialization. Versus exact Run60 it changed validation
`+0.00020590151731225692`, forward `+0.0006832696785779024`, and high activity
`-0.0013046239845939667`. The combined candidate remains unpromoted, but this
is the only confounded branch with positive aggregate movement; one fresh
exact-Run52 compatibility retest is therefore allowed. The earlier statement
that temporal context itself was closed is withdrawn.
