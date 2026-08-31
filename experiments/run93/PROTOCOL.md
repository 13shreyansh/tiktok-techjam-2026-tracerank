# Run93 protocol: twelve-seed causal consensus saturation

Declared: **2026-08-31 20:21 SGT**, before any Run93 model execution.

## Frozen question

Does additional independent initialization diversity reduce stochastic
within-user ordering error in the already selected causal sequence-NFM, or has
the equal-rank ensemble saturated at six members?

This is not an architecture, feature, loss, weight, or history search. Every
member keeps the selected causal construction unchanged: last 20 positive
`long_view` videos and tags, dot attention, embedding dimension 16, hidden
dimension 128, dropout 0.2, neural FM term, batch 4096, AdamW rate 0.0005,
weight decay 0.00001, at most 12 epochs, patience 4, and Apple auto device.
All final-test rows remain feature-only.

The fixed seed set is exactly `2026` through `2037`. For each chronological
shadow, reuse the aligned Run83 seeds `2026` through `2028`, train seeds `2029`
through `2037`, and form exactly one equal within-user percentile-rank
consensus over all twelve members. No seed subset, duplicate, weight,
normalization, checkpoint, epoch, or post-hoc route is permitted.

## Shadow gates

The unchanged three-seed Run83 causal consensuses are the frozen parents:

| Window | Validation primary | Forward primary |
|---|---:|---:|
| early | 0.6175101511752181 | 0.6048488365317426 |
| middle | 0.6121450621306554 | 0.5899162902580050 |
| late | 0.5929336491998536 | 0.6041838833268496 |

1. Every member must exit zero, contain finite aligned validation/forward
   predictions, report the training-only label boundary, and score at least
   `that window's parent-consensus validation primary - 0.002`.
2. A window passes when the twelve-seed consensus improves validation primary
   by at least `+0.00010`, forward primary does not decline by more than
   `0.00005`, neither validation nor forward GAUC/nDCG@5 declines by more than
   `0.00020`, and no fixed activity/date slice declines by more than `0.00050`.
3. Continue after one failed window because two-of-three remains possible.
   Stop after two failures. Official construction is allowed only when at
   least two of three windows pass, mean validation and mean forward deltas are
   positive, no validation/forward primary falls below `-0.00030`, and no
   component or slice crosses `-0.001` on any window.

## Official construction and promotion

If and only if the shadow gate passes, reuse the six clean Run84 members
`2026` through `2031`, freshly train seeds `2032` through `2037` on the
official development split, then form one equal twelve-seed within-user-rank
consensus. No Run82 or other historical official artifact may enter it.

Promotion over clean Run84 requires:

- primary gain at least `+0.00015` over `0.605374519999571`;
- GAUC and nDCG@5 each no worse than `-0.00020`;
- every fixed activity/date slice no worse than `-0.001`;
- all six new members at least `0.6035` primary and all twelve prediction
  archives finite and aligned;
- final label-blind 170,588-row CSV alignment, artifact hashes, and a dedicated
  verifier passing.

Failure preserves Run84 unchanged. There is no seed-count extension, subset,
weight, median, Copeland, or blend rescue after the fixed twelve-seed result.

## Limits and stopping

- Maximum 50 counted executions and six hours for Run93.
- Maximum planned executions: 37 (27 shadow members, three shadow consensuses,
  six official members, one official consensus).
- Fresh strategic reviews are required after attempts 8, 16, 24, and 32.
- Convergence epsilon is `0.00005` over a three-result window, subject to the
  earlier frozen transfer and construction gates. The finite construction
  stops immediately after rejection or the first complete official consensus;
  artificial iterations are forbidden.
- Official final-test outcomes, random-log outcomes, external submission,
  upload, push, visibility changes, and organizer contact remain locked.
