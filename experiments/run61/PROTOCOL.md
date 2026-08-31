# Run 61 protocol: equal capacity-group consensus

Started: **2026-08-31 08:27:00 SGT**.

## Independent question

Does an equal rank-16/rank-32 capacity-group consensus reduce complementary
ordering error beyond the protected rank-32 family?

## Frozen candidate and gates

- Each chronological shadow aggregates exactly two group predictions with
  equal within-user percentile-rank mean: the fixed three-seed rank-16
  consensus and matching rank-32 seed 2027.
- Early source SHA-256 values are
  `168e80be2b8e52c22d27460d746cd844c670bd6a57512e36577c94ea8d272e65`
  and `8d2392915731af585177bbb79287fc391629dea2fbce9f1faab0c965db911872`.
- Middle source SHA-256 values are
  `872321deea7aa2cb6a86e54b4bd7ac313d76407380b3255ad0078777484dba3a`
  and `1ea3cfdf6a04c4bcae31db2cbf66ebfea09caab85d44ed6508b60bb47ca1c93b`.
- Late source SHA-256 values are
  `aed7b50d4d7996a27404e99b18551e373477bece9c4edf6cb094f6ab7b7280eb`
  and `468e9a1a76b5a25afab7e7ca3b3af5350320bc654a38eef8ae9e95fc5ff8fcc6`.
- No subset, weight, duplication, raw-logit, calibration, route, seed, rank,
  retraining, or alternative aggregation variation.
- Early must improve validation and forward primary each `>= +0.00025`, with
  no component below `-0.0005` and no fixed slice below `-0.001` versus the
  matching Run52 rank-32 seed.
- A pass scores middle and late unchanged; at least two of three windows must
  meet the same gain and safety guards.
- Only then create one official three-seed rank-16 consensus from its three
  already trained members and aggregate it equally with the protected Run52
  three-seed rank-32 consensus. Promote only at primary `>= +0.0003` versus
  Run52 and every official slice `>= -0.0005`.
- Stop at any gate or artifact failure, convergence, 50 attempts, or six hours.
  Closing Run61 does not stop the 72-hour campaign.

All scores remain deterministic 1/32 development-sample evidence, not the full
benchmark, hidden test, submission, or leaderboard. Public-test labels and
external actions remain locked.
