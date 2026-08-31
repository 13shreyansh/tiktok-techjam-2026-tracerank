# Run 55 report: protected-parent meta-consensus rejected

Run55 gave one equal within-user rank vote to the protected Run49 mixed-
capacity consensus and one to the matching Run52 rank-32 prediction. It tested
no weights, subsets, duplicate votes, routes, calibration, or training.

The early evaluation completed successfully. Validation primary improved only
`+0.0000869978496522`, below the frozen `+0.00025` gate; forward improved
`+0.0002726783047383`. GAUC changed `-0.0000891803247367` and nDCG@5
`+0.0002631760240410`. Medium activity gained `+0.0011437608614966`, but
high activity regressed `-0.0022600880745046`, crossing the fixed slice guard.
The weaker parent therefore adds some transfer diversity but dilutes the
stronger high-activity ordering.

The one counted attempt took `6.174093` subprocess seconds and peaked at
`3,333,439,488` bytes RSS. Its ignored 4,448,335-byte prediction archive
SHA-256 is
`973ba8f590c9b41fa1583242dd169ebb91a1b7d5668bca3f694f9a9e607fcfb3`.
No later shadow, official evaluation, weight, subset, or route followed.

Run52 remains protected at local primary `0.6534977984044839`. These are fixed
1/32 development-sample results, not the full benchmark, hidden test,
submission, or leaderboard. No public-test labels or external action occurred;
the campaign continues.
