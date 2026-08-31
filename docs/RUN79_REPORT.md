# Run 79 report: cross-fitted parent-aware LambdaMART rejected

Run79 tested whether Run76's weak forward list-ranking signal could be made
reliable by removing in-sample parent leakage. An exact Run52 rank-32 parent
trained only on April 8–9; a deterministic LambdaMART correction trained from
its out-of-fold April 10 errors and stopped on April 11. The frozen correction
was then applied unchanged to exact Run52's April 12–14 validation and April
15–17 forward predictions. The tree used the same 21 audited causal dense
features plus parent within-user rank, with the parent rank as its initial
score. No coefficient, feature, tree parameter, route, or calibration was
searched.

The supporting parent completed successfully, selected epoch 2, and produced
finite aligned predictions. Its April 10 primary was `0.6282755110503404` and
April 11 primary `0.6225943083488539`. The correction then selected tree
iteration 26. On clean April 11 meta-validation it improved parent primary
`+0.0012127770581434`, GAUC `+0.0006333603463269`, and nDCG@5
`+0.0017921937699596`.

That signal did not transfer safely. Versus exact Run52, April 12–14 primary
changed only `+0.0002593853063149`, below the frozen `+0.0003` gate; GAUC
changed `-0.0004366293071785` and nDCG@5 `+0.0009553999198082`. April 15–17
forward primary changed `-0.0001132338704767`, GAUC
`-0.0003647626589791`, and nDCG@5 `+0.0001382949180256`. High-activity primary
regressed `-0.0030788875590728`, also failing the `-0.001` slice guard.

Attempt 1 took `732.640181` wrapper seconds and peaked at `26,810,564,608`
bytes RSS. Attempt 2 took `18.807056` seconds and peaked at `10,225,319,936`
bytes. The causal exact-repeat sidecar preparation took `5,800.935616` seconds
at `7,461,683,200` bytes RSS and is recorded separately. The ignored tree is
98,218 bytes, SHA-256
`a79b384fa8affd2c94e754ce7f8095c30618a89692ac9bd12475203d1663547d`;
the ignored 7,490,150-byte prediction archive is SHA-256
`108b6936ea8067409d82547d9d67ead4074a6d0d5580b45b4ad78fd4363c71f4`.

Run79 stops at attempt 2 without later windows or official seeds. Together,
Runs76 and 79 show complementary nDCG signal from the causal tree, but not
stable aggregate or high-activity transfer. Run52 remains protected at local
official-sample primary `0.6534977984044839`. These are deterministic 1/32
development-sample results, not the full benchmark, hidden test, submission,
or leaderboard. Closing Run79 closes only this hypothesis; the 72-hour
campaign continues.
