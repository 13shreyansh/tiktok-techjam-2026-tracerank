# Run 54 protocol: rank-32 causal primary-topic affinity

Started: **2026-08-31 07:06:02 SGT**.

## Independent question

Can the confirmed rank-32 repeat-affinity sparse FM use two strictly causal
user/current-primary-tag fields to improve ranking beyond Run52 without
temporal or activity-slice overfit?

## Frozen candidate

- Exact Run52 sparse FM, rank 32, learning rate 0.001, 20 epochs, patience 4,
  batch 65,536, prediction batch 262,144, 16 threads, seeds 2027–2029.
- Change only feature set from `history_item_repeat` to
  `history_item_repeat_tag_affinity`, adding the existing prior primary-tag
  count-log2 bucket and beta-smoothed long-view-rate bucket.
- Keep the Run45 causal contract and bucket definitions unchanged. Do not test
  multi-tag history, secondary tags, alternative buckets or priors, recency,
  explicit actions, another rank, optimizer, learning rate, regularizer, seed,
  or ensemble weight.

## Procedure and gates

1. Use the checksum-verified existing early tag archive and train seed 2027.
   Continue only if validation and forward primary each improve
   `>= +0.00025` versus exact Run52 rank-32 seed 2027, no component metric
   falls below `-0.0005`, and no fixed slice falls below `-0.001`.
2. A pass unlocks causal tag-archive construction and unchanged seed-2027
   training for middle, then late. At least two of three windows must meet the
   `+0.00025` validation-and-forward gate; no aggregate below `-0.0005` and no
   fixed slice below `-0.001`.
3. Only then build official tag state and train seeds 2027–2029. Require paired
   mean primary gain `>= +0.00025`, no seed below `-0.0005`, primary span
   `<= 0.002`, and no fixed official slice below `-0.001`.
4. Score exactly one equal within-user percentile-rank consensus of the three
   tag-affinity seeds. Promote over Run52 only if primary gains `>= +0.0003`
   and every fixed official slice is `>= -0.0005`.
5. Stop at gate failure, memory pressure, convergence, 50 counted model
   attempts, or six hours including newly required feature preparation.
   Closing Run54 does not stop the 72-hour campaign.

All scores are deterministic 1/32 development-sample evidence, not the full
benchmark, hidden test, submission, or leaderboard. Public-test labels and
external actions remain locked.
