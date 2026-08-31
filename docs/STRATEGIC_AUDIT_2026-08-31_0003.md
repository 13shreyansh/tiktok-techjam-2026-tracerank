# Fresh-context strategic audit — 2026-08-31 00:03 SGT

## What the last topic runs actually established

Run 45's causal primary-tag affinity was directionally positive on early
validation (`+0.000345186`) and forward (`+0.000381937`) but correctly failed
its `+0.0005` continuation gate. Run 46 and Run 47 showed that neither global
ensembling nor a fixed high-activity route converted that weak specialist into
a robust aggregate gain. Those branches are closed; changing weights or
routing thresholds would be validation micro-tuning.

## One remaining information-loss question

The source exposes up to three tags per video, but Run 45's affinity state used
only the first tag. A read-only full-cache scan found a distinct valid second
tag on 34,333,275 rows (about 16.6%) and a distinct valid third tag on 951,810
rows (about 0.46%). Run 48 asks whether preserving those historical secondary
tags strengthens the same causal signal. It still scores only the candidate's
primary tag, so it adds two bounded fields rather than a new sparse current-tag
model.

This is a data-representation correction, not a search over models. Historical
tags are deduplicated within each row, state is prior-only, equal-timestamp rows
cannot update one another, and state freezes at the training cutoff. The exact
rank-8 repeat-affinity parent and seed 2027 are held fixed. Early validation and
forward gains must both reach `+0.0005`; otherwise the family closes before
other windows. This advances the winning goal only if previously discarded
official fields yield temporal, slice-safe improvement.
