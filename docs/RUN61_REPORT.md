# Run 61 report: capacity-group consensus stopped at slice gate

Run61 gave one equal within-user percentile-rank vote to the fixed three-seed
rank-16 consensus and one to the matching rank-32 prediction. This exact
capacity-group composition had not been tested in prior runs. Membership,
hashes, aggregation, and gates were frozen before scoring.

The early attempt completed successfully and improved validation primary
`+0.0003645742050721`, GAUC `+0.0001391450849392`, nDCG@5
`+0.0005900033252050`, and forward primary `+0.0003768823102682` versus exact
Run52. Cold/low and medium activity improved, and both date slices were
positive. High activity, however, regressed `-0.0013542772549110`, crossing
the frozen `-0.001` continuation floor.

The attempt took `6.087807` seconds and peaked at `3,333,341,184` bytes RSS.
The ignored 4,446,671-byte prediction SHA-256 is
`c621cddf7c46af11e5bc1f3841a018c15167d4a0dd9a56d878bd44bf281980e4`.

Run61 therefore stopped without middle, late, official, subset, weight, or
route variation. Its aggregate gain is evidence for capacity diversity, not a
promoted candidate. Run52 remains protected at local primary
`0.6534977984044839`. These are fixed 1/32 development-sample results, not the
full benchmark, hidden test, submission, or leaderboard. The 72-hour campaign
continues in a new bounded run.
