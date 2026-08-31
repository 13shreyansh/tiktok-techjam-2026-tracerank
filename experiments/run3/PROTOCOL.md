# Run 3 ranking-family protocol

Run tag: `run3-ranking-families`
Branch: `codex/run3-ranking-families`
Started: 2026-08-29 14:04 SGT

## Objective

Find a materially stronger and likely hidden-test-robust model family, not a
micro-tuned variant of the 0.605400885 fallback. The public date-based test
labels remain locked.

## Evaluation design

Every candidate family is compared with the unchanged causal parent on three
expanding chronological windows:

| Window | Training dates | Validation dates | Forward dates |
|---|---|---|---|
| early | Apr 8-11 | Apr 12-14 | Apr 15-17 |
| middle | Apr 8-14 | Apr 15-17 | Apr 18-21 |
| late | Apr 8-17 | Apr 18-21 | Apr 22-28 |

The first three counted attempts establish paired parent scores. A family is
eligible for official validation only when its median paired gain is at least
0.001, it does not lose more than 0.0005 on any window, and it does not create a
material late-date or activity-segment regression. A smaller gain may survive
only if its predictions add independently verified ensemble diversity.

Official-validation promotion is replicated with seeds 2026, 2027, and 2028.
The frozen Run 2 CSV remains the fallback until an exact packaged replacement
passes all gates.

## Limits and stopping

1. Count every launched attempt, including failures and timeouts, up to 50.
2. Stop no later than six hours after this run starts.
3. Reject `--evaluate-test`; no public-test labels may be read.
4. Keep the organizer evaluator unchanged and record its hash every time.
5. Change one coherent idea per family and preserve every result.
6. Stop a family after its three-window result is clearly noncompetitive.
7. Stop the run after three completed families fail to improve their paired
   parent by more than 0.002, or when another organizer convergence condition
   is reached.
8. After every family or eight counted attempts, write a fresh strategic review
   before launching more work.
9. Do not upload, submit, push, contact organizers, change registration, expose
   secrets, or alter repository visibility.

## Initial family order

1. Leakage-safe numeric aggregate features with a binary/ranking tree model.
2. Efficient multi-behavior sequential supervision with conflict controls.
3. Exposure-bias and temporal-drift correction using authorized KuaiRand data.
4. Cross-fitted stacking and rank ensembling across only robust families.
