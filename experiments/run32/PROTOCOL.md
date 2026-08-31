# Run 32 protocol: quarter-density causal history-item FM

Started: **2026-08-30 01:03 SGT**.

## Independent question

Does doubling Run 30's successful training density again—from residue 0
modulo 8 to residue 0 modulo 4—improve the same protected causal history-item
FM when all evaluation and robustness-reference rows stay exactly residue 0
modulo 32?

## Locked data and model design

- Build a label-safe April 8–28 cache from SplitMix64 residue 0 modulo 4.
- Training uses every retained 1/4 row. Validation, forward, and robustness
  reference additionally require residue 0 modulo 32, exactly matching Run 30
  and Run 24. Ordered user, original video, timestamp, date, and label equality
  must pass before scoring.
- Reuse only the independently validated raw full-corpus item-work arrays.
  Rebuild all sample-aligned causal user/item histories for the 1/4 cache.
- Keep Run 30 rank 8, learning rate 0.001, BCE, batching, epoch/patience caps,
  feature set, and seeds unchanged. First compare `shadow_early` seed 2027.

## Gates and limits

Require +0.001 validation primary, no more than -0.0005 forward, and no fixed
slice regression beyond -0.001. A pass repeats unchanged on middle and late;
two of three are required before official-development seeds 2027/2028/2029.
Official promotion requires positive paired mean gain of at least +0.001 with
no seed regression beyond -0.0005.

Stop at family failure, official epsilon 0.002 / N=3 convergence, 50 attempts,
or six hours. Preprocessing time/resource use is recorded separately. Run 32
is separately and cumulatively disclosed. Public-test/hidden labels,
submission, upload, push, contact, credentials, registration change, and
public release remain locked.
