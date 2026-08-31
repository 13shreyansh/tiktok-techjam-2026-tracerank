# Run 82 protocol: fully causal six-seed Pure consensus

Started: **2026-08-31 15:04:43 SGT**.

## Frozen candidate

- Parent: protected mixed six-member within-user-rank ensemble, validation
  primary `0.6054008850379737`.
- Reuse exact corrected causal members seeds 2026, 2027, and 2028 with hashes
  in `manifests/candidate-artifacts.json`.
- Train seeds 2029, 2030, and 2031 with exact Run2 causal settings: official
  split; `sequence_nn`; long-view video/tag history length 20; dot attention;
  16-dimensional embeddings; 128 hidden units; dropout 0.2; neural FM term;
  batch 4096; AdamW rate 0.0005 and weight decay 0.00001; at most 12 epochs;
  patience 4; Apple auto device. Export unlabeled test predictions without
  evaluating them.
- Form exactly one equal within-user percentile-rank consensus of corrected
  seeds 2026–2031. No subset, duplicate, weight, normalization, or route.

## Gates and stopping

- All three new attempts must exit zero, produce finite aligned valid/test
  arrays and hashed checkpoints, and each score at least `0.6035` primary. The
  six new/existing causal member primary span must be at most `0.002`.
- Score the fixed consensus only after all member gates pass. Promote only if
  it improves protected primary by `>= +0.0002`, neither GAUC nor nDCG@5 falls
  by more than `0.0002`, and every fixed Pure activity/date slice falls by no
  more than `0.001` versus the protected mixed ensemble.
- Any failure preserves the mixed ensemble and closes Run82 without seed,
  member, weight, architecture, history, epoch, or blend search.
- Stop at the first construction/member failure, final gate, 50 attempts, or
  six hours. Closing this run does not end the broader campaign.

Public-test/hidden labels and all external actions remain locked.
