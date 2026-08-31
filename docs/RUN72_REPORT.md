# Run 72 report: corrected identity-freeze refinement rejected

Run72 explicitly restored Run52's legacy random unknown-row initialization,
reproduced exact Run52 through epoch 1, and then froze raw user, video, and
author latent/linear rows while context and causal-history rows continued
learning. All 71 tests and isolated-cache bytecode compilation passed before
the run.

The construction gate passed exactly. Epoch-1 loss, validation GAUC, nDCG@5,
primary, forward metrics, and every fixed robustness slice equal Run52. Direct
array comparison found maximum absolute difference `0.0` for both validation
and forward predictions. This distinguishes the valid Run72 test from Run71's
disclosed Run60-parent drift.

No post-freeze epoch improved the parent. The best later checkpoint was epoch
4 at primary `0.6337686895740273`, which is
`-0.001396649458687782` below Run52. The selected best therefore remained exact
epoch 1, with zero validation and forward delta. The attempt took
`692.105190` seconds and peaked at `26,780,942,336` bytes RSS.

The ignored 3,786,952,845-byte checkpoint SHA-256 is
`42d7cd91ef42acdad003669ace6020787428ff83b02bafa432df9ace8a928bba`;
the ignored 6,607,883-byte prediction archive SHA-256 is
`8d2392915731af585177bbb79287fc391629dea2fbce9f1faab0c965db911872`.
The archive container hash differs from Run52, but both stored arrays are
bit-for-bit equal.

Run72 closes after one counted experiment without freeze-point, field-subset,
later-window, official-seed, or blend search. Run52 remains protected at local
primary `0.6534977984044839`. These scores are fixed deterministic 1/32
development-sample evidence, not the full benchmark, hidden test, submission,
or leaderboard. The 72-hour campaign continues with a different hypothesis.
