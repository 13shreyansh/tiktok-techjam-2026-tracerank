# Run85 protocol: dual positive and strict-skip histories

Declared: **2026-08-31 17:30 SGT**, before any Run85 scored model execution.

## Fixed hypothesis

A ranking model should distinguish prior attraction from prior rejection.
Retain the Run84 member architecture unchanged except for one separate causal
negative-history channel:

- positive history: last 20 prior `long_view=1` videos and tags;
- negative history: last 20 prior rows satisfying all of `long_view=0`,
  `is_click=0`, and `play_time_ms / max(duration_ms, 1) <= 0.05`;
- each history is built in within-user `(time_ms, source_index)` order;
- validation, forward, and final-test histories are frozen from training rows;
- candidate-aware dot attention is applied separately to the two channels;
- negative profile, candidate-product, and absolute-difference enter only the
  nonlinear head; the FM fields remain unchanged;
- embeddings 16, hidden 128, dropout 0.2, neural FM term, batch 4096, AdamW
  rate 0.0005 and weight decay 0.00001, at most 12 epochs, patience 4;
- no threshold, history length, blend weight, optimizer, capacity, or loss
  search is permitted in this family.

Only standard Pure training rows may create either history. The random log and
the 1K/27K benchmarks are excluded. Final-test rows are feature-only.

## Staged evaluation and promotion

1. Run seed 2027 on `shadow_early`, paired to the exact causal Run83 seed-2027
   parent: validation `0.6169077754020691`, forward
   `0.6040810346603394`. Continue only if validation improves by at least
   `0.0005`, forward does not decline, neither GAUC nor nDCG@5 declines by more
   than `0.0005`, and no activity/date slice declines by more than `0.001`.
2. If step 1 passes, run seeds 2026 and 2028 on `shadow_early`, then a fixed
   equal within-user-rank consensus. Require the consensus to beat the Run83
   causal consensus (`0.6175101511752181`) by at least `0.0005`, with forward
   at least `0.6048488365317426` and the same component/slice floors.
3. If step 2 passes, repeat the same three fixed seeds and equal consensus on
   `shadow_middle` and `shadow_late`. Both windows must pass the corresponding
   paired Run83 causal consensus by at least `0.0002`, with no component or
   slice loss beyond `0.001` and no forward loss.
4. Only after all shadow gates, run official seeds 2026, 2027, and 2028 plus
   their fixed equal within-user-rank consensus. Promote only if consensus
   improves the clean Run84 primary by at least `0.0002`, has no component or
   slice loss beyond `0.001`, and all members attest the test-label boundary.
5. One optional candidate is predeclared: an equal within-user-rank blend of
   the promoted three-seed dual-history consensus and the clean Run84
   six-member consensus. It may replace the standalone candidate only if it
   adds another `0.0002` official-validation primary with the same floors.

There is no rescue attempt after a failed stage. A failure closes the family.

## Limits and stopping

- Hard limits: at most 50 counted executions and six hours for Run85.
- Convergence declaration: epsilon `0.00005`, `N=3`, minimum floor 4. The
  staged family closes earlier on a failed promotion gate; if it reaches the
  official stage, it stops at the first completed predeclared candidate after
  the minimum floor and does not add artificial iterations.
- Every launched model or ensemble command is counted, including failures.
- A fresh strategic review is required after eight counted executions.
- The clean Run84 CSV and predictions remain untouched fallback artifacts.
- No upload, submission, push, visibility change, organizer contact, or
  credential use is authorized.
