# Run 64 report: conservative capacity shrinkage below forward gate

Run64 gave one within-user percentile-rank vote to the fixed rank-16 consensus
and two identical votes to protected rank 32. This predeclared two-to-one ratio
was the only weight tested.

The early attempt completed successfully and improved validation primary
`+0.0003640851113182`, GAUC `+0.0002241039601183`, and nDCG@5
`+0.0005040662625182`. Four slices improved and high activity regressed only
`-0.0005927376477256`, inside the frozen floor. Forward primary, however,
improved only `+0.0001777153613997`, below the `+0.00025` continuation gate.

The attempt took `6.192740` seconds and peaked at `3,367,092,224` bytes RSS.
The ignored 4,771,077-byte prediction SHA-256 is
`7c8a877fe7f0fca0144d1354928510efc75dc417a4a03ae2d8e99b042c9bef43`.

Run64 stops without middle, late, official, or alternate-weight search. Run52
remains protected at local primary `0.6534977984044839`. These are fixed 1/32
development-sample results, not the full benchmark, hidden test, submission,
or leaderboard. The 72-hour campaign continues.
