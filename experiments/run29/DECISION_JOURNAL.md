# Run 29 decision journal

## 2026-08-29 23:54 SGT — user-balanced objective opened

- The evaluator averages each user's ranking contribution, while unweighted BCE
  gives users influence proportional to their row count. This mismatch is
  distinct from the rejected feature, trend, capacity, and ensemble families.
- Use one fixed inverse-square-root weighting to reduce dominance without giving
  the sparsest users full inverse-count weight. No coefficient search follows.
- Run 24 seed 2029 at `0.630624629` remains protected.

## 2026-08-29 23:56 SGT — first gate failed; family closed

- Attempt `001-user-balanced-history-item-shadow-early` completed in 47.227
  seconds with peak RSS 1,976,139,776 bytes and selected epoch 7.
- Validation changed `-0.001226000` and forward changed `-0.001354108` versus
  the exact Run 24 parent. Cold/low and medium activity regressed
  `-0.001216411` and `-0.001568478`; high activity improved only `+0.000121765`.
- The fixed alpha fails the aggregate, forward, and slice gates. Close without
  alpha, clipping, optimizer, or seed tuning; retain the unweighted Run 24
  checkpoint.
