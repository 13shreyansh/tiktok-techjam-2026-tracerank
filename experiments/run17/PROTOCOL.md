# Run 17 protocol: KuaiRand-1K DeepFM interaction family

Started: **2026-08-29 20:12 SGT**.

## Independent question

Can a compact DeepFM-style nonlinear interaction tower improve the stable
KuaiRand-1K content sparse-FM family by learning higher-order interactions
among user, video, author, tab, duration, primary tag, upload type, and video
type, without using public-test outcomes or changing the label-free inputs?

This is a new, predeclared architecture-family run after Run 16 converged and
closed. The official statement says the 50-iteration and six-hour limits apply
"per benchmark run" but does not define valid restart boundaries. Therefore
Run 17 reports its own limits **and** the cumulative execution, token, wall-time,
and intervention totals across all Track 2 research. It is not represented as
an organizer-approved reset.

## Fixed first candidate

- Dataset: KuaiRand-1K ignored development cache, April 8-28 only.
- Features: the exact Run 16 `content` fields.
- Model: the unchanged rank-16 FM plus a two-layer `32 -> 16` ReLU tower over
  concatenated field embeddings, dropout 0.1, and a learned scalar output.
- Training: native long-view BCE, seed 2027, sparse learning rate 0.001, dense
  learning rate 0.001, batch 65,536, at most 20 epochs, patience 4.
- First split: `shadow_early`; official validation remains locked.
- Parent: the paired Run 16 content sparse FM on the same split.

## Gates

1. The implementation must pass syntax and synthetic shape/gradient tests
   without reading benchmark labels.
2. Attempt 1 must improve shadow validation by at least 0.001 and may not lose
   more than 0.0005 on the forward window. Activity/date slices must not show
   an unexplained collapse larger than 0.001.
3. If the first gate passes, repeat unchanged on middle and late windows. At
   least two of three windows must pass before official validation unlocks.
4. Promotion requires official validation, three fixed seeds (2026-2028), and
   the predeclared equal within-user-rank ensemble. No seed cherry-picking or
   weight search.
5. Convergence is binding within this run: stop after three consecutive gains
   of at most 0.002, 50 counted attempts, or six wall-clock hours, whichever
   occurs first.

## Hard boundaries

No public-test label evaluation, hidden-test access, submission, upload, push,
organizer contact, credential use, registration change, or visibility change.
Every execution, failure, command, hash, metric, elapsed time, and resource
reading is append-only evidence. The protected Run 16 candidate at
`0.6537467530366082` remains immutable unless all promotion gates pass.
