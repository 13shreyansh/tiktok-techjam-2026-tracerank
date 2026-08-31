# Run 52 protocol: rank-32 repeat-affinity capacity

Started: **2026-08-31 04:15 SGT**.

## Independent question

Does one exact doubling of repeat-affinity sparse-FM interaction rank from 16
to 32 capture material, temporally stable ordering signal beyond the confirmed
rank-16 architecture?

## Frozen candidate

- Full-density `history_item_repeat` sparse FM, rank 32, learning rate 0.001,
  20 epochs, patience 4, batch 65,536, prediction batch 262,144, 16 threads.
- Seeds 2027, 2028, and 2029 are fixed before any rank-32 score. No other rank,
  optimizer, learning rate, regularizer, feature, objective, seed, or epoch
  variant is allowed.

## Procedure and gates

1. Train seed 2027 on early and compare with the exact rank-16 seed-2027
   archive. Continue only if validation and forward primary each improve
   `>= +0.0003`, no aggregate metric falls below `-0.0005`, and no fixed slice
   falls below `-0.001`.
2. If early passes, repeat seed 2027 unchanged on middle and late. At least two
   of three windows must meet `+0.0003` on validation and forward; no aggregate
   below `-0.0005` and no slice below `-0.001`.
3. Only then train official seeds 2027, 2028, and 2029. Against their exact
   rank-16 counterparts, require paired mean primary gain `>= +0.0003`, no
   seed below `-0.0005`, primary span `<= 0.002`, and no fixed slice below
   `-0.001`.
4. Score exactly one equal within-user rank consensus of the three rank-32
   seeds. Promote over Run49 only if primary gains `>= +0.0003` and every
   official slice is `>= -0.0005`.
5. Stop at gate failure, memory pressure, convergence, 50 counted attempts, or
   six elapsed hours. Closing Run 52 does not stop the 72-hour campaign.

All metrics are deterministic 1/32 development-sample evidence, not the full
benchmark, hidden test, submission, or leaderboard. Public-test labels and
external actions remain locked.
