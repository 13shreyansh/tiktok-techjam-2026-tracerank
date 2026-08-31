# Run 53 report: rank-64 capacity rejected

Run53 tested one frozen extrapolation from the newly protected rank-32
repeat-affinity sparse FM: exact rank 64, unchanged data, features, optimizer,
learning rate, epochs, patience, batch sizes, seed, and chronological window.

The early-shadow attempt completed successfully but missed the predeclared
gate. Rank-64 primary was `0.6345003457781826`, or
`-0.0006649932545325` versus the exact rank-32 parent. GAUC changed
`-0.0006160701398239`, nDCG@5 `-0.0007139163692410`, and forward primary
`-0.0001154281760545`. All five fixed primary slices regressed, ranging from
`-0.0003736139882768` to `-0.0009157586253021`. The best checkpoint occurred
after epoch 1; later epochs deteriorated sharply, consistent with excess
capacity rather than an undertrained candidate.

The attempt took `801.822829` subprocess seconds and peaked at
`45,272,547,328` bytes RSS. The ignored 7,431,533,773-byte checkpoint SHA-256
is `950d76ffde16efcdc3c9a3edf7c013035aad5fc8ddda75d17914e38d61aef96f`;
the ignored 6,614,916-byte prediction archive SHA-256 is
`2b30f563a58def1b34949a5a8e82991a003f58495420f0a999e0028e01b8372a`.

The branch stopped after one counted attempt. No middle, late, official,
alternate-rank, learning-rate, batch-size, or ensemble evaluation followed.
Run52 remains protected at local primary `0.6534977984044839`. These are fixed
1/32 development-sample results, not the full benchmark, hidden test,
submission, or leaderboard. No public-test labels or external action occurred;
closing Run53 does not stop the 72-hour campaign.
