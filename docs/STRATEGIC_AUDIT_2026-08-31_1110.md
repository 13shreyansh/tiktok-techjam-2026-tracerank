# Strategic audit — 2026-08-31 11:10 SGT

## Evidence after Run70

Run70 closes recurring calendar context. Across Runs53–70, added capacity,
fields, objectives, and interaction changes usually worsen both transfer and
high-activity users. Capacity consensus is the only family with repeated small
aggregate gains, but its safe routes failed frozen transfer gates. Run52 stays
the protected candidate.

One structural training asymmetry remains untested. Every Run52 shadow and all
three official seeds select epoch 1. Epoch 2 loses between `0.002360023` and
`0.006658144` primary, and later epochs fall much further. The single sparse
table forces raw user, video, and author identities to keep updating together
with bounded context and causal-history fields. The identities have millions
of rows and can memorize quickly; the history/context fields have only a few
dozen buckets and may still benefit from later interaction updates.

## Run71 decision

Reproduce exact Run52 through epoch 1. From epoch 2 onward, remove only raw
user, video, and author rows from both sparse latent and linear optimizer
updates. Continue updating all content, context, causal user history, causal
item history, and repeat-affinity rows with the unchanged optimizer, learning
rate, order, patience, and evaluator. Model selection may restore epoch 1 if
refinement is not useful.

Freeze after exactly one epoch because all six independent Run52 trainings
peak there; do not search the freeze point, frozen field subset, learning rate,
regularization, epoch count, or blend. Start with seed-2027 early and require
validation and forward primary each `>= +0.00025`, both component deltas
`>= -0.0005`, every fixed slice `>= -0.001`, and peak RSS below 60 GB. A pass
repeats unchanged on middle and late, then three official seeds and the fixed
equal within-user rank consensus.

## Third-person goal check

This is not another capacity or feature retry. It tests whether the universal
one-pass peak is caused specifically by high-cardinality identity overfitting
while preserving Run52 bit-for-bit at epoch 1. The risk is that all fields
overfit together; in that case best-checkpoint rollback should reproduce the
parent and the branch closes after one attempt. The fixed 1/32 development
sample remains only local evidence, never hidden/full-benchmark proof.
