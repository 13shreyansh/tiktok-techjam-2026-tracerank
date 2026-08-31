# Run 57 protocol: rank-32 repeat plus recent sequence

Started: **2026-08-31 07:25:08 SGT**.

## Independent question

Do 11 strictly causal recent sequence/context fields add temporally stable
ordering signal beyond the protected rank-32 full-density repeat-affinity FM?

## Frozen candidate

- Exact Run52 rank-32 `history_item_repeat` data, model, BCE, learning rate
  0.001, 20 epochs, patience 4, batch 65,536, prediction batch 262,144,
  16 threads, and seeds 2027–2029.
- Append exactly the existing Run20 sequence profile: last five positive tags,
  current-tag count among those five, last strong tag and match, last hate tag
  and match, and log2 hours since last positive.
- Training rows see only earlier timestamps; same-timestamp rows update after
  the batch; validation/forward state freezes at the training cutoff.
- No history length, action union, bucket, field subset, rank, objective,
  optimizer, learning-rate, epoch, seed, or ensemble-weight variation.

## Procedure and gates

1. Build and hash only `shadow_early`; training is forbidden until construction
   succeeds with zero causal timestamp inversions and the 207,446,146-row shape.
2. Train seed 2027 early. Continue only if validation and forward primary each
   improve `>= +0.0003` versus exact Run52, no component metric falls below
   `-0.0005`, and no fixed slice falls below `-0.001`.
3. A pass builds/trains middle then late unchanged. At least two of three
   windows must meet the same gain; no aggregate below `-0.0005` and no slice
   below `-0.001`.
4. Only then build official state and train seeds 2027–2029. Require paired
   mean primary gain `>= +0.0003`, no seed below `-0.0005`, span `<= 0.002`,
   and no fixed official slice below `-0.001`.
5. Score one equal within-user percentile-rank consensus. Promote over Run52
   only at `>= +0.0003` primary with every slice `>= -0.0005`.
6. Stop at construction/gate failure, memory pressure, convergence, 50 counted
   model attempts, or six hours including preparation. Closing Run57 does not
   stop the 72-hour campaign.

All scores remain deterministic 1/32 development-sample evidence, not the full
benchmark, hidden test, submission, or leaderboard. Public-test labels and
external actions remain locked.
