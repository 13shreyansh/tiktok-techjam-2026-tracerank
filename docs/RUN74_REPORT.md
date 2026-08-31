# Run 74 report: chronological one-pass ordering rejected

Run74 changed exactly one aspect of the protected Run52 seed-2027 early
candidate: every eligible training row was traversed in stable ascending
`time_ms` order instead of Run52's seeded random order. Data, labels,
features, legacy unknown-row initialization, rank, loss, optimizer, evaluator,
splits, and inference were frozen. All 73 tests and isolated-cache bytecode
compilation passed before scoring.

The first gate failed decisively. Validation primary was
`0.6319153908834496`, or `-0.0032499481492655` versus exact Run52; validation
GAUC changed `-0.0025960065812070` and nDCG@5 changed
`-0.0039038897173241`. Forward primary was `0.6335973787010323`, or
`-0.0031845616159048`; forward GAUC changed `-0.0027324294563834` and
forward nDCG@5 changed `-0.0036366937754263`.

Every fixed robustness slice regressed: cold/low activity
`-0.0030870332540780`, medium activity `-0.0034972288173032`, high activity
`-0.0033359818949272`, early dates `-0.0022259141974909`, and late dates
`-0.0028829041425308`. Chronological batching therefore harmed both
optimization and temporal transfer; there is no evidence for later windows,
official seeds, ordering variants, or an ensemble.

The one counted attempt completed successfully in `677.178521` seconds and
peaked at `27,782,021,120` bytes RSS. The ignored 3,786,952,605-byte
checkpoint SHA-256 is
`5cb225413f8b2293b8b212c3486dd1e32133695aff03b9468383ff46d05faeba`;
the ignored 6,600,680-byte prediction SHA-256 is
`141ddbcad89fdb11e431aa31250f70ad886889654c438bc1a08330f9521c044e`.

Run52 remains protected at local primary `0.6534977984044839`. These scores
are deterministic 1/32 development-sample evidence, not the full benchmark,
hidden test, submission, or leaderboard. Closing Run74 closes only this
hypothesis; the 72-hour campaign continues with a fresh strategic audit.
