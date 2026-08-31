# Run 83 protocol: paired causal-history transfer audit

Started: **2026-08-31 16:14:49 SGT**.

## Frozen question

Does correcting source-row history to strictly chronological per-user history
improve generalization of the exact Pure sequence-FM architecture, independently
of the already observed official score?

For each chronological window in order (`shadow_early`, `shadow_middle`, then
`shadow_late`), train paired source-order and causal-history models at fixed
seeds 2026, 2027, and 2028. Both sides use the exact Run2/Run82 settings:
`long_view` video/tag history length 20, dot attention, embedding 16, hidden
128, dropout 0.2, neural FM term, batch 4096, at most 12 epochs, patience 4,
AdamW rate 0.0005 and weight decay 0.00001, Apple auto device, and later
forward evaluation. Form one equal within-user percentile-rank consensus for
each side after all six members in a window succeed.

The source-order mode exactly follows the original CSV traversal when building
training histories. It is an audit comparator only and cannot be promoted,
packaged, blended, or evaluated on official/public/hidden data. Causal mode
remains the default code path. No architecture, member, seed, epoch, subset,
weight, normalization, or window is selected after scoring.

## Decision gates

- Every output must exit zero and contain finite aligned validation and forward
  arrays. The causal/source comparison must use matching rows and seeds.
- A window supports causal selection only when the causal consensus improves
  both validation and forward primary, at least two of three paired seeds
  improve validation primary, paired mean validation primary is positive, and
  neither GAUC nor nDCG@5 regresses by more than `0.0005` on validation or
  forward.
- Every fixed causal-consensus activity/date slice must remain within `0.001`
  of the source-order consensus. A primary regression below `-0.0005` in either
  validation or forward is a window failure even if other gates pass.
- Select the already frozen Run82 six-causal official artifact as the final
  Pure candidate only if at least two of three windows support causal selection
  and no window crosses a catastrophic component, primary, or slice floor.
  Otherwise retain the exact Run2 mixed fallback at `0.6054008850379737`.
- Continue after one failed window because two-of-three remains possible. Stop
  after two failed windows, a construction/alignment failure, the final gate,
  50 attempts, or six hours. Complete the mandatory fresh review after each
  eight counted attempts before continuing.

Run83 never scores official validation or public/hidden test labels. Its only
possible candidate decision is between the two already frozen Pure artifacts.

