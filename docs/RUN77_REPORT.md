# Run 77 report: target-aware tag residual rejected

Run77 tested the first target-aware history mechanism on the protected 27K
representation. The exact Run52 rank-32 checkpoint was frozen while a compact
DIN residual let the current primary tag attend over the user's five most
recent strictly earlier long-view-positive primary tags. The final residual
layer was initialized to zero, making epoch zero an exact rollback.

The pre-score 4,096-row smoke test and the full attempt both reproduced the
preserved parent predictions with maximum absolute error `0.0`. Epoch 1 then
scored primary `0.6336730452542434`, GAUC `0.7016082842946603`, and nDCG@5
`0.5657378062138265`. Versus exact Run52 this is primary
`-0.0014922937784717`, GAUC `-0.0012904440931404`, and nDCG@5
`-0.0016941434638031`. Patience one stopped training and restored epoch zero.
The final validation and forward metrics therefore equal exact Run52 at
`0.6351653390327151` and `0.6367819403169371` respectively.

The successful command took `168.070475` wrapper seconds and peaked at
`21,586,870,272` bytes RSS. The ignored 57,685-byte rollback metadata model
SHA-256 is
`5a03e49f00a54406da1f4e02c410199a348780b4d7ebdc24ed7250f5d88849c1`.
The ignored 6,607,883-byte final prediction archive is byte-identical to the
parent and has SHA-256
`8d2392915731af585177bbb79287fc391629dea2fbce9f1faab0c965db911872`.

The immutable ledger's robustness section used all 41,010,906 training rows
to form activity tertiles, yielding cutpoints 1,577/3,374 rather than the
established evaluation-sampled 1,282,407-row reference. This was a reporting-
only defect: because the saved candidate is the exact parent, a read-only
rescore with the established reference reproduced Run52 cutpoints 49/106 and
all five Run52 slice metrics. Source was corrected and 80 tests passed; no
score or decision was revised.

No middle/late archive, later seed, history/action variant, public-test label,
submission, upload, or external action followed. Run52 remains protected at
local official-sample primary `0.6534977984044839`. Closing Run77 closes only
this coarse five-tag residual; the 72-hour campaign continues. These scores
are deterministic 1/32 development-sample evidence, not hidden-test,
full-benchmark, submission, or leaderboard results.
