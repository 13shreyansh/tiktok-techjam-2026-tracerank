# Run 50 protocol: rank-16 three-seed consensus

Started: **2026-08-31 01:50 SGT**.

## Independent question

Can equal within-user rank aggregation of three fixed rank-16 repeat-affinity
seeds reduce seed-specific error beyond the confirmed seed-2027 rank-16 model
and the protected mixed-capacity Run49 consensus?

## Frozen candidate

- Exact full-density repeat-affinity sparse FM at rank 16, seeds 2027, 2028,
  and 2029. All other data, feature, optimizer, loss, learning-rate, epoch,
  patience, batch, evaluator, split, and slice settings are unchanged.
- Convert each member independently to deterministic within-user percentile
  ranks and average exactly `1/3` each in seed order 2027, 2028, 2029.
- No raw/logit averaging, weight, subset, extra seed, rank, calibration, route,
  feature, or objective variation is allowed.

## Procedure and gates

1. Reuse the existing rank-16 seed-2027 early archive; train only seeds 2028
   and 2029, then score one fixed consensus. Continue only if validation and
   forward each improve `>= +0.0003` over rank-16 seed 2027 and every slice is
   `>= -0.0005`.
2. If early passes, repeat unchanged for middle and late. At least two of three
   windows must pass the `+0.0003` validation/forward gate; no aggregate may be
   below `-0.0005` and no slice below `-0.001`.
3. Only then train official seeds 2028 and 2029 beside the existing seed 2027.
   Require no seed below `-0.0005` versus seed 2027, candidate primary span
   `<= 0.002`, and no fixed slice below `-0.001` versus seed 2027.
4. Score exactly one official three-member consensus. Promote over Run49 only
   if primary gains `>= +0.0003` and every official slice is `>= -0.0005`.
5. Stop at gate failure, convergence, 50 counted attempts, or six elapsed
   hours. Closing Run 50 does not stop the 72-hour campaign.

All metrics are fixed development-sample evidence, not full-benchmark,
hidden-test, submission, or leaderboard results. Public-test labels and all
external actions remain locked.
