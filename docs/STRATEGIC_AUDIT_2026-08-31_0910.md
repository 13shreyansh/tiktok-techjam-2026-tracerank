# Strategic audit — 2026-08-31 09:10 SGT

## Evidence after Runs 53–67

Run52 remains the protected candidate. Rank 64, normalized initialization,
neutral unknown rows, topic affinity, meta-consensus, hard pairs, sequence
fields, additive sequence tails, full class balancing, and bipartite-only
interactions all failed their frozen gates. Capacity blending produced small
development gains but did not transfer safely enough to promote. Reopening
those knobs would now be validation chasing.

One repeated signal has not yet been isolated: exact Run52 reaches its best
checkpoint after the first complete randomized pass, then both metrics decline
for every later epoch. Several related rank-32 traces show the same shape. The
checkpoint cadence cannot tell whether the true optimum occurs earlier inside
that first pass.

## Run68 decision

Test one predeclared midpoint checkpoint: the deterministic first half of the
seed-2027 shuffled early-window training order. Keep Run52 architecture,
features, loss, optimizer, learning rate, batching, inference, splits, and
evaluator unchanged. This is a learning-duration diagnostic, not an epoch,
learning-rate, fraction, or seed sweep. No alternate fraction follows inside
this family.

## Risks and third-person check

The half pass sees fewer training rows and its random prefix may be less
representative. A gain could therefore be seed-specific or merely reduce
overfitting on the fixed development sample. Require simultaneous validation
and chronological-forward improvement, component and slice guards, unchanged
middle/late repeats, then three official seeds before promotion. Run52 remains
untouched.

An independent reviewer would prefer this bounded diagnostic to another model
family because it is directly implied by every protected learning curve, costs
half a pass, and is frozen before scoring. It does not establish hidden-test or
leaderboard improvement.
