# Run 50 strategic review after eight attempts

Reviewed: **2026-08-31 03:15 SGT**.

## Does the hypothesis still advance the objective?

Yes. The frozen three-seed rank-16 consensus improved the seed-2027 parent on
both validation and forward evaluation in the early and middle chronological
windows. Early gains were `+0.001123218` and `+0.001663388`; middle gains were
`+0.001553357` and `+0.000611963`. Every fixed activity/date slice improved in
both windows. This is replicated evidence for variance reduction rather than a
single-window score fluctuation.

## Leakage and overfitting audit

- Seeds 2027/2028/2029, equal one-third within-user rank aggregation, model
  family, capacity, features, optimizer, and gates were frozen before training.
- No member, subset, weight, feature, epoch, or metric was selected after
  observing the early or middle results.
- Late seed 2028 and 2029 both completed successfully under the identical
  preregistered setup; their individual results do not change the fixed
  consensus definition.
- Public-test and hidden labels remain unused. All reported metrics are from
  the deterministic 1/32 development sample, not a full benchmark or
  leaderboard result.

## What could still go wrong?

- The late consensus can regress even though two earlier windows pass.
- Official seed behavior can be less stable than shadow behavior, and the pure
  rank-16 consensus can still lose to the protected mixed-capacity Run49
  candidate.
- Small development-sample gains may not transfer to the organizer hidden set.
- Three large checkpoints increase packaging and inference complexity; exact
  member order and hashes must be preserved if promotion occurs.

## Decision

Proceed only with attempt 9: score the already-declared equal-rank late
consensus. Do not change its members or weights. If the aggregate multi-window
gate remains satisfied, train only the two missing official seeds and score
the one fixed official consensus under the existing seed-stability and slice
gates. Otherwise close Run 50 without promotion. In either case, closing this
bounded run does not stop the overall 72-hour campaign.

The protected Run49 primary `0.6509565751074728` remains immutable, and no
external submission action is authorized.
