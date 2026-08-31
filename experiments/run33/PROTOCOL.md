# Run 33 protocol: half-density causal history-item FM

Started: **2026-08-30 02:17 SGT**.

## Independent question

Does doubling Run 32's successful training density again—from residue 0
modulo 4 to residue 0 modulo 2—improve the same protected causal history-item
FM when all evaluation and robustness-reference rows stay exactly residue 0
modulo 32?

## Why this is the next experiment

Run 30's fourfold density increase improved paired official-development score
by +0.005756834. Run 32's next doubling improved it by +0.002375987. The gain
is diminishing but remained positive across three temporal shadows, three
seeds, and every fixed activity/date slice. This is stronger evidence than an
untested architecture switch. Run 33 changes only training density and keeps
the protected Run 32 checkpoint intact.

## Locked data and model design

- Build a label-safe April 8–28 cache from SplitMix64 residue 0 modulo 2.
- Training uses every retained half-sample row. Validation, forward, and
  robustness reference additionally require residue 0 modulo 32, exactly
  matching Runs 24, 30, and 32. Ordered user, original video, timestamp, date,
  and label equality must pass before scoring.
- Reuse only independently validated raw full-corpus item-work arrays. Rebuild
  all sample-aligned causal user/item histories for the half cache.
- Keep Run 32 rank 8, learning rate 0.001, BCE, batching, epoch/patience caps,
  feature set, and seeds unchanged. First compare `shadow_early` seed 2027.

## Gates and limits

Require +0.0005 validation primary, no more than -0.0005 forward, and no fixed
slice regression beyond -0.001. A pass repeats unchanged on middle and late;
two of three are required before official-development seeds 2027/2028/2029.
Official promotion requires positive paired mean gain of at least +0.0005
with no seed regression beyond -0.0005.

Stop this run at family failure, official epsilon 0.002 / N=3 convergence, 50
attempts, or six hours. That closes only Run 33, not the 72-hour campaign.
Preprocessing time/resource use is recorded separately. Public-test/hidden
labels, submission, upload, push, contact, credentials, registration change,
and public release remain locked.
