# Run 53 protocol: rank-64 repeat-affinity capacity

Started: **2026-08-31 06:48:52 SGT**.

## Independent question

Does one exact doubling of the confirmed rank-32 repeat-affinity sparse-FM
interaction capacity to rank 64 produce another material, temporally stable
ordering gain without unacceptable memory use?

## Frozen candidate

- Full-density `history_item_repeat` sparse FM, rank 64, learning rate 0.001,
  20 epochs, patience 4, batch 65,536, prediction batch 262,144, 16 threads.
- Seeds 2027, 2028, and 2029 are fixed. No other rank, batch size, optimizer,
  learning rate, regularizer, feature, objective, seed, or epoch variant is
  allowed in Run53. An out-of-memory result closes this configuration; it does
  not unlock an adaptive rescue setting.
- Exact paired parent: the matching Run52 rank-32 split and seed.

## Procedure and gates

1. Train seed 2027 on early. Continue only if validation primary improves
   `>= +0.00025`, forward primary is `>= -0.0005`, no component metric falls
   below `-0.0005`, no fixed slice falls below `-0.001`, and peak RSS remains
   below 60,000,000,000 bytes.
2. If early passes, repeat unchanged on middle and late. At least two of three
   windows must improve validation `>= +0.00025`; every forward score must stay
   `>= -0.0005`, with the same component, slice, and memory guards.
3. Only then train official seeds 2027–2029. Require paired mean primary gain
   `>= +0.00025`, no seed below `-0.0005`, primary span `<= 0.002`, every fixed
   slice `>= -0.001`, and peak RSS below 60,000,000,000 bytes.
4. Score exactly one equal within-user percentile-rank consensus of the three
   rank-64 seeds. Promote over Run52 only if primary gains `>= +0.0003` and
   every official slice is `>= -0.0005`.
5. Stop at gate failure, memory pressure, convergence, 50 counted attempts, or
   six elapsed hours. Closing Run53 does not stop the 72-hour campaign.

All scores are deterministic 1/32 development-sample evidence, not the full
benchmark, organizer hidden test, submission, or leaderboard. Public-test
labels and external actions remain locked.
