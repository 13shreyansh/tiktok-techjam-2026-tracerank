# Run86 protocol: task-protected click extraction

Declared: **2026-08-31 17:53 SGT**, before implementation or any Run86 scored
execution.

## Fixed hypothesis and architecture

The dense training-only click label can regularize the judged long-view model
only if task-specific capacity prevents the negative transfer already observed
with fully shared auxiliary/funnel designs.

Retain the exact Run83 causal sequence-NFM member settings and change only the
nonlinear tower:

- positive history: last 20 prior long-view videos and tags, causal order;
- two shared two-layer experts, one long-view-only expert, one click-only expert;
- separate long-view and click softmax gates, each over the two shared experts
  plus its own task-specific expert;
- separate scalar heads; only the long-view score is used at inference;
- judged loss: long-view BCE; auxiliary loss: click BCE at fixed weight `0.05`;
- embeddings 16, hidden 128, dropout 0.2, neural FM term, batch 4096, AdamW
  rate 0.0005, weight decay 0.00001, at most 12 epochs, patience 4;
- no expert count, loss weight, task label, history, optimizer, capacity, seed,
  threshold, or blend search inside this family.

Only the standard Pure training rows from 8--21 April provide either label.
The random log and 1K/27K datasets are excluded. Validation outcomes are used
only for declared evaluation and early stopping. Final-test rows remain
feature-only and final-test outcomes are never loaded.

## Staged gates

1. Run seed 2027 on `shadow_early`, paired to exact Run83 seed 2027: validation
   primary `0.6169077754020691`, forward primary `0.6040810346603394`.
   Continue only if validation improves by at least `0.0005`, forward declines
   by no more than `0.0002`, neither GAUC nor nDCG@5 declines by more than
   `0.0005`, and no fixed activity/date slice declines by more than `0.001`.
2. If step 1 passes, run the unchanged candidate on `shadow_middle` and
   `shadow_late` at seed 2027. At least two of three windows must improve
   validation by `0.0005`; all three must meet the same component/slice floors,
   and mean forward change must be nonnegative.
3. If step 2 passes, run official seeds 2026, 2027, and 2028 and form exactly
   one equal within-user-rank three-seed consensus. Every member must score at
   least `0.6035`. Continue only if the consensus is within `0.0002` of clean
   Run84 primary `0.605374519999571`, with no component or slice loss beyond
   `0.001`.
4. One final construction is then allowed: give the three-member Run86 family
   one-third total weight and the six clean Run84 members two-thirds total
   weight through equal member-level within-user ranks. Promote only for at
   least `+0.0002` primary over Run84 with the same component/slice floors.

Failure at any stage closes the family without a rescue attempt.

## Limits and stopping

- Hard limits: 50 counted executions and six hours for Run86.
- Convergence: epsilon `0.00005`, window `N=3`, minimum floor 4. A failed
  staged gate closes earlier; a successful finite construction stops at the
  first completed predeclared final candidate.
- Every launched model or ensemble command counts, including failures.
- A fresh strategic review is required after eight counted executions.
- Run84 artifacts remain untouched.
- No upload, submission, push, visibility change, organizer contact, or secret
  use is authorized.

