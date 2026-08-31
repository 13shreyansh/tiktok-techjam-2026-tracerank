# Run 81 report: exact-parent primary-aligned LambdaLoss rejected

Run81 applied an explicit organizer-primary proxy to exact Run52. For each of
25,883 usable training users, it sampled at most five positives and retained
the twenty highest-parent-score negatives. It computed nDCG@5 swap weights from
the rows' exact ranks in the user's complete parent-scored training list and
combined that user-equal loss with positive-count-weighted pairwise AUC loss.
The previously audited learning rate `0.00002`, equal component weights, one
epoch, caps, batching, seed, and stop gates were frozen before scoring.

Epoch zero reproduced both stored parent arrays with maximum absolute error
`0.0`. The training set contributed 128,849 positives, 513,587 negatives, and
19,171 users with nonzero top-five swap weights. The one trained epoch then
changed validation GAUC by `-0.0211876477586898`, nDCG@5 by
`-0.0335669496275842`, and primary by `-0.0273772986931370`. Forward primary
changed `-0.0288984309742814`. Every fixed slice failed: cold/low activity
`-0.0248457871791993`, medium `-0.0337121869129439`, high
`-0.0296957332235809`, early dates `-0.0177642464261869`, and late dates
`-0.0266459304317982`. The direct sparse-table update is therefore much too
destructive under the frozen objective, not a plausible promotion.

The successful wrapper took `78.51258707046509` seconds and peaked at
`29,959,077,888` bytes RSS. The ignored 3,758,478,053-byte rollback checkpoint
has SHA-256 `69e1d33ce60ac9a7b7f3e498341a58c9b92caa60ebd02ee06e984388555a86f3`.
The ignored 6,607,883-byte finite prediction archive is byte-identical to the
parent, SHA-256
`8d2392915731af585177bbb79287fc391629dea2fbce9f1faab0c965db911872`.
Run81 stops at attempt one with no tuning. Run52 remains protected at local
official-sample primary `0.6534977984044839`. These are deterministic 1/32
development-sample results, not the full benchmark, hidden test, submission,
or leaderboard. Closing Run81 closes only this loss; the campaign continues.
