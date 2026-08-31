# Fresh-context strategic audit — 2026-08-30 23:54 SGT

## Evidence carried forward

Run 45's causal user-topic model was not strong enough to replace the repeat
parent: `+0.000345186` early and `+0.000381937` forward, below its frozen
`+0.0005` gate. It nevertheless increased nDCG@5 by `+0.000905392` and the
high-activity slice by `+0.001656192`, while all slices stayed within guard.
That different error profile may add ensemble diversity even though the single
model is not promotable.

## One bounded diversity question

Run 46 tests exactly one equal within-user rank consensus containing the three
confirmed repeat-affinity seeds and the Run 45 seed-2027 topic-affinity model.
This is equivalent to retaining 75% total vote from the robust repeat family
and adding one 25% topic vote, but no weight was selected from scores: every
independent member receives one equal vote. Do not test raw means, other
weights, member subsets, duplicate members, or rank-16 additions.

The early archive is already available. If the four-member early consensus is
not materially better than the exact Run 43 early consensus on validation,
forward, and slices, the family closes before any additional preprocessing.
If it passes, later topic archives/models are prepared one window at a time
under the same six-hour run clock and fixed gates.
