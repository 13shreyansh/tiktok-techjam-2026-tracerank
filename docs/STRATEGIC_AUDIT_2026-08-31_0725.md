# Strategic audit — 2026-08-31 07:25 SGT

## Remaining major information gap

Run56 shows conservative hard-pair fine-tuning is effectively flat on the
rank-32 parent. The strongest untested organizer-aligned direction is now
ordered recent behavior on KuaiRand-27K. Official research describes extremely
long user histories, and the workshop stressed that what a person watched
before should affect the next candidate.

The prior Run20 sequence-profile result does not answer this question. It used
KuaiRand-1K, rank 16, and a `sequence` feature set that replaced rather than
augmented the later 27K causal user/item/repeat fields. It regressed its content
parent. The current question combines the protected 24-field Run52
representation with 11 strictly causal recent fields: the last five positive
tags, current-tag repeat count, last strong-feedback tag, last hated tag,
candidate match indicators, and time since the last positive event.

## Run57 decision and controls

The combined encoder and per-split builder were committed before any score and
passed 39 targeted tests. Builder SHA-256 is
`25354e101879a278591a903eef59bd32d3a0a36ed4aa2ac202e7a53e93859d35`;
ranker SHA-256 is
`204a5b496f06a08120c3e2bdcd07742a0cc2dc12fc3079faa8029b4223a1cd86`.
Run57 builds only the early causal archive first, hashes it, then trains one
rank-32 seed. Later archives are locked behind score gates.

Risks are substantial: recent categorical memories may duplicate aggregate
history, explicit feedback is sparse, large sequential caches cost time and
disk, and the fixed sample can reward noisy top-five effects. Require forward
transfer, every activity/date slice, three paired official seeds, and one
frozen consensus before promotion. Preserve Run52 regardless of outcome.
