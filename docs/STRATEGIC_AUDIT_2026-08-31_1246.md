# Strategic audit — 2026-08-31 12:46 SGT

Run77 establishes that target-aware attention over only five coarse primary
tags is not sufficient: its first trained epoch regressed primary
`-0.0014922937784717` and both components, then exact-parent rollback restored
Run52. Do not tune that tag-only model.

The representation gap remains more specific than the failed mechanism. The
workshop and the successful Pure history model use item/creator identity as
well as topic. The 27K tag vocabulary has only 69 values, while the official
cache contains 6,522,683 creator identities. Run52 knows aggregate and exact
user-creator repeats, but not an ordered candidate-aware representation of
which recent positive creators and categories resemble the current candidate.

Run78 therefore adds a new causal information source rather than changing a
Run77 parameter: the five most recent positive creator IDs aligned with the
existing five positive tags. Candidate and history creator embeddings have
width 8; tag embeddings have width 8; their concatenation uses the same frozen
DIN attention/head and exact-parent zero residual. No video identity, user
identity, auxiliary action, longer history, blend, or parameter search is
allowed.

The 4,148,923,048-byte creator archive built in `43.692960` seconds at
`14,940,323,840` bytes RSS, has SHA-256
`d3c563e5d1f70fcde871e01c0d7185979141804d541a2391714f3a30bc140ec7`,
zero timestamp inversions, and the same 6,626,844 equal-time batches as the tag
archive. All 84 tests pass and a 4,096-row epoch-zero smoke test matches Run52
with maximum absolute error `0.0`.

The risk is that creator identities are sparse and exact candidate/history
creator matches occur on only 1,906 of 865,586 sampled validation rows. A
learned creator embedding can still capture cross-creator compatibility, but a
first-gate failure closes creator/tag attention. Run52 stays protected and all
scores remain local 1/32 development evidence.
