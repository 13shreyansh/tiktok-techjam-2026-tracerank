# Run 39 decision journal

## 2026-08-30 13:51 SGT — run opened

- A fresh-context audit selected confirmation over a new model change because
  Run 38 has strong cross-time and two-seed evidence but is missing its third
  seed solely due to the six-hour wall-clock boundary.
- Inherit the already-passed Run 38 temporal gate for this exact frozen
  candidate. Run one official seed 2029, disclose it as Run 39 attempt 1, and
  close immediately after the campaign-level gate is evaluated.
- Protected Run 34 remains unchanged until that gate passes.

## 2026-08-30 14:22 SGT — confirmation passed; run closed

- Attempt 1 completed successfully in 1,838.667 seconds with
  23,444,537,344-byte peak RSS. Epoch 1 was selected.
- Seed 2029 primary is `0.6492243384881571`, `+0.0044201326297953` over the
  exact Run 34 seed-2029 parent. GAUC improves `+0.0023787608225704` and
  nDCG@5 improves `+0.0064615044370204`.
- Every seed-2029 slice improves: cold/low `+0.002878284`, medium
  `+0.004768130`, high `+0.011288490`, early dates `+0.004468752`, and late
  dates `+0.003947711`.
- Combining Run 38 seeds 2027-2028 with this independently logged confirmation
  gives mean `0.6489308670307136`, paired mean gain `+0.0040966194469133`,
  worst seed gain `+0.0039330988963173`, and span `0.0006726389322296`.
  Every predeclared gate passes.
- Protect the seed-2029 checkpoint and close Run 39 after its single attempt.
  This is deterministic development-sample evidence, not hidden-test or
  leaderboard evidence. Continue the hackathon with a fresh hypothesis family.
