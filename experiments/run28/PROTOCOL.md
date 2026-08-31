# Run 28 protocol: KuaiRand-27K cross-capacity rank consensus

Started: **2026-08-29 23:49:40 SGT**.

## Independent question

Do the near-tied rank-8 and rank-16 causal history-item models make sufficiently
different errors for a fixed equal within-user rank consensus to improve both
nearby and forward ranking?

## Fixed candidate

- Exact Run 24 attempt 21 rank-8 shadow predictions and Run 27 attempt 1 rank-16
  shadow predictions; no retraining, member selection, or score calibration.
- Convert each member independently to deterministic within-user percentile
  ranks, then average 50/50. This mirrors the robust aggregation that won the
  required Pure benchmark search and is fixed before any Run 28 score.
- First and only screen: `shadow_early`. Require +0.0003 validation and forward,
  with no activity/date slice regression beyond -0.0003. Close on failure.

Passing requires unchanged middle and late replication before any official
members. Stop at family failure, official epsilon 0.002 / N=3 convergence, 50
attempts, or six hours. Run 28 is separately and cumulatively disclosed; no
organizer-approved reset is claimed. Public-test/hidden labels remain locked.
