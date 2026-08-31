# Run 54 report: rank-32 topic affinity rejected

Run54 tested whether the two causal primary-topic affinity fields that were
directionally positive at rank 8 became useful on the protected rank-32
repeat-affinity architecture. The early archive, buckets, data, optimizer,
seed, and evaluation were frozen before training.

The attempt completed successfully but failed the continuation gate. Primary
was `0.6341768633198739`, or `-0.0009884757128412` versus exact Run52.
GAUC changed `-0.0005653607709151`, nDCG@5
`-0.0014115906547674`, and forward primary `-0.0001424604771062`. Every
fixed primary slice regressed; high activity (`-0.0031349960604745`) and early
dates (`-0.0012520649948180`) also crossed the frozen slice guard. Greater FM
capacity therefore did not rescue the earlier weak topic signal.

The one counted attempt took `583.584926` subprocess seconds and peaked at
`29,213,523,968` bytes RSS. The ignored 3,786,957,637-byte checkpoint SHA-256
is `a9208acb0f03864066e3f55c0a60b04fc9d84e81e46482f9fa44858f278f4c61`;
the ignored 6,603,912-byte prediction archive SHA-256 is
`85103dc2fe2726f2f9f206be704108133bce2fb075f21a844e4052bc1634c5d8`.

No later feature archive, later shadow, official seed, feature variant, or
ensemble was run. Run52 remains protected at local primary
`0.6534977984044839`. These are fixed 1/32 development-sample results, not the
full benchmark, hidden test, submission, or leaderboard. No public-test labels
or external action occurred; the overall campaign continues.
