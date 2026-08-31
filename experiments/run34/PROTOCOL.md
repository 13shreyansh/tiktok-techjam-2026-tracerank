# Run 34 protocol: full-density causal history-item FM

Started: **2026-08-30 04:02 SGT**.

## Independent question

Does the final density doubling—from Run 33's residue 0 modulo 2 to every
eligible April 8–28 development row—improve the same protected causal
history-item FM when all evaluation and robustness-reference rows stay exactly
residue 0 modulo 32?

## Why this is the next experiment

Run 33's half-density change improved the paired official-development mean by
+0.003664494, with positive gains on three temporal shadows, three seeds, and
every fixed activity/date slice. The effect did not collapse as density grew.
Full density is the last direct scaling test and remains a single-variable
continuation; the protected Run 33 checkpoint stays untouched.

## Locked data and model design

- Build a label-safe April 8–28 cache from SplitMix64 residue 0 modulo 1.
- Training uses every eligible development row. Validation, forward, and
  robustness reference additionally require residue 0 modulo 32, exactly
  matching Runs 24, 30, 32, and 33. Ordered user, original video, timestamp,
  date, and label equality must pass before scoring.
- Reuse only independently validated raw full-corpus item-work arrays. Rebuild
  all sample-aligned causal user/item histories for the full cache.
- Keep Run 33 rank 8, learning rate 0.001, BCE, batching, epoch/patience caps,
  feature set, and seeds unchanged. First compare `shadow_early` seed 2027.

## Gates and limits

Require +0.0005 validation primary, no more than -0.0005 forward, and no fixed
slice regression beyond -0.001. A pass repeats unchanged on middle and late;
two of three are required before official-development seeds 2027/2028/2029.
Official promotion requires positive paired mean gain of at least +0.0005
with no seed regression beyond -0.0005.

Stop this run at family failure, official epsilon 0.002 / N=3 convergence, 50
attempts, or six hours. That closes only Run 34, not the 72-hour campaign.
Preprocessing time/resource use is recorded separately. Public-test/hidden
labels, submission, upload, push, contact, credentials, registration change,
and public release remain locked.
