# Strategic audit: Run86 task-protected multi-task extraction

Recorded: **2026-08-31 17:53 SGT**, before implementation or scoring.

## Evidence reviewed

The organizer identifies multiple observed feedback fields as legitimate
ranking-stage supervision, but prior local evidence warns against indiscriminate
sharing:

- Run7's seven action-coded histories and any-action histories regressed every
  fixed chronological slice.
- Run10's separate censored-watch auxiliary head regressed validation and
  forward transfer.
- Run69's shared click/conditional-long-view funnel regressed every fixed 27K
  development slice. That benchmark is not transferable training data for Pure,
  but its negative-transfer warning is relevant to architecture selection.
- A reusable audit of only the authorized Pure training log counted 1,141,112
  rows. Click covers 46.34% of rows, has phi `0.76049` with long-view, and is
  present on 99.58% of long-view rows. The union of like/follow/comment/forward
  covers only 2.23% of rows and has phi `0.11556` with long-view. The feedback
  labels are therefore neither independent nor uniformly dense.

The original MMoE paper proposes shared experts with task-specific gates to
learn task relationships rather than force one shared representation:
<https://research.google/pubs/modeling-task-relationships-in-multi-task-learning-with-multi-gate-mixture-of-experts/>.
The RecSys 2020 PLE paper specifically targets negative transfer and the
"seesaw" effect with shared and task-specific experts; DOI
<https://doi.org/10.1145/3383313.3412236>. These are conceptual references;
no third-party implementation is copied.

## Decision

Do not spend a run on a plain shared click auxiliary head or a large multi-label
network. Run86 will test one small, task-protected extraction layer on the exact
causal sequence-NFM parent:

- two shared experts;
- one long-view-only expert and one click-only expert;
- a separate soft gate for each task over its two shared experts plus its own
  task-specific expert;
- the judged long-view head remains primary and retains the unchanged NFM term;
- click is training-only auxiliary supervision at fixed weight `0.05`.

This is a bounded architectural test of whether task-specific routing prevents
the already observed negative transfer. If it misses the first chronological
gate, the family closes; no expert-count, auxiliary-weight, label-union, or
optimizer sweep follows. Run84 remains the protected clean candidate.

