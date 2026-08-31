# Strategic audit — 2026-08-31 11:55 SGT

## Evidence after Run73

The exact-parent correction cleanly closes recurring time fields. Most recent
failures add representational burden or change the judged loss; neither has
improved chronological transfer. Run52 still peaks after one complete pass in
all six independent trainings, so a change to how that one pass traverses the
same rows is more defensible than more epochs, capacity, or feature search.

## Run74 decision

Run52 currently applies a seed-specific uniform shuffle to all eligible rows.
Run74 uses exactly one alternative: stable global ascending `time_ms` order.
Equal timestamps retain verified cache order. All rows, labels, features,
initialization, optimizer, learning rate, batches, epochs, patience, evaluator,
and seed remain unchanged; explicit legacy unknown initialization preserves
Run52. No reverse order, day shuffle, recency weight, rolling window, order
mixture, or seed-specific ordering is allowed.

The hypothesis is that SparseAdam's final state after one pass should reflect
the latest training interactions more strongly, matching later validation and
forward periods without changing the dataset or using future labels. The risk
is correlated batches and loss of random mixing, which can reduce optimization
quality or overemphasize a narrow late period.

Start with seed-2027 early. Require validation and forward primary each
`>= +0.00025`, both component deltas `>= -0.0005`, every fixed slice
`>= -0.001`, and peak RSS below 60 GB. A failure closes ordering without a
recency/order sweep. The 1/32 sample remains local evidence, not hidden or
full-benchmark proof.

## Third-person goal check

This tests a parameter-free, causal alignment between training and temporal
evaluation that has not appeared in prior 27K runs. It is more independent
than reopening a failed feature, loss, capacity, or ensemble family. Run52
remains immutable regardless of the result.
