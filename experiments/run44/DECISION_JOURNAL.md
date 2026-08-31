# Run 44 decision journal

## 2026-08-30 23:16 SGT — frozen before any Run 44 score

- Run 43's rank consensus is protected at `0.6501881386335703` on the 27K
  development sample.
- Raw-logit averaging is selected because all three members use the same model
  and loss scale; it retains confidence-margin agreement that ordinal ranks
  discard. This is not chosen from a Run 44 score.
- Exactly one aggregation is allowed. The three chronological archives remain
  first; official development remains locked until the frozen shadow gate.

## 2026-08-30 23:18 SGT — close after two sub-gate shadows

- Early validation gained `+0.0002386258619838`, but forward changed
  `-0.0000486774336870`; it is not a full win. Every slice remained inside the
  continuation guard.
- Middle validation gained `+0.0001210911721909` and forward gained
  `+0.0001485212787781`; it is also not a full `+0.0002` win. Every slice
  improved, but only by `+0.0000243139` to `+0.0003454705`.
- With zero qualifying wins after two windows, the required two-of-three gate
  is mathematically unreachable. Stop before late and official evaluation.
  Do not try another aggregation. Preserve Run 43 and continue the campaign in
  a new independent run.
