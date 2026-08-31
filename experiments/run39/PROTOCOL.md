# Run 39 protocol: independent repeat-affinity confirmation

## Purpose

Run 38's six-hour guard blocked its third official seed before execution. Run
39 independently confirms the exact frozen candidate; it does not reopen or
tune the feature family.

## Frozen attempt

- Run exactly one official-development attempt with seed 2029.
- Use the exact Run 38 ranker SHA-256
  `85b160894516b5e300c59bda78a1d414bb8b25694f07c637744218f27cacafb1`,
  official feature archive SHA-256
  `b67e0e2ef0f5034df06c01db2c171a875be4bd929913375fe9fbb471c2bb90c2`,
  feature set `history_item_repeat`, rank 8, learning rate `0.001`, 20-epoch
  ceiling, patience 4, and unchanged batches/evaluator.
- Compare only with Run 34 seed 2029 on the identical fixed development rows.
- No code, feature, bucket, prior, seed, or ensemble change is permitted.

## Gate and stop

After the one attempt, combine it with Run 38 seeds 2027 and 2028. Promote at
campaign level only if paired mean gain is at least `+0.0005`, no seed delta is
below `-0.0005`, candidate-score span is at most `0.002`, and the confirmation
seed has no fixed slice below `-0.001`. Close Run 39 after the attempt whether
it passes or fails. A pass protects the best direct checkpoint among the three
seeds; it does not claim hidden-test, submission, or leaderboard performance.

