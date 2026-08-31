# Run 73 report: exact-parent recurring time context rejected

Run73 corrected Run70's parent drift by combining only the frozen
Asia/Shanghai hour and weekday categorical fields with explicit Run52 legacy
unknown-row initialization. The parent, fields, model, optimizer, evaluator,
gates, and seed were frozen before scoring. All 71 tests and isolated-cache
bytecode compilation passed.

Versus exact Run52, validation primary changed
`-0.00029070048570811746`, GAUC `-0.0003252553931565316`, and nDCG@5
`-0.0002561455782595923`. Forward primary changed only
`+0.000032334112790022296`, while forward GAUC changed
`-0.00045090182408125123`. High-activity primary was the worst fixed slice at
`-0.001939133643000801`, beyond the frozen `-0.001` floor.

The one counted attempt took `771.624602` seconds and peaked at
`28,139,356,160` bytes RSS. The ignored 3,786,956,885-byte checkpoint SHA-256
is `69c8ec9f92abc7042fae64b39ff61320b80f783d969b3f8a6e2ad90f46005b39`;
the ignored 6,617,545-byte prediction SHA-256 is
`939cd8048a45ec54298a231738065f8deceae4a67f008bff534d2a65aea476ae`.

This exact-parent correction resolves Run70's ambiguity and closes recurring
time context without later windows, official seeds, temporal variants, or
blends. Run52 remains protected at local primary `0.6534977984044839`. These
scores are fixed deterministic 1/32 development-sample evidence, not the full
benchmark, hidden test, submission, or leaderboard. The 72-hour campaign
continues with a different hypothesis.
