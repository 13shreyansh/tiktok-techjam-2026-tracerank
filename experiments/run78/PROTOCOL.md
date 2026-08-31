# Run 78 protocol: exact-parent creator-and-tag DIN residual

Started: 2026-08-31 12:46 SGT

## Frozen hypothesis

Ordered recent positive creator and category identities provide candidate-
aware preference signal absent from both Run52's aggregate repeat fields and
Run77's coarse tag-only attention.

## First attempt

- `shadow_early`, seed 2027; exact Run52 checkpoint and parent prediction.
- Five positive creator IDs, SHA-256
  `d3c563e5d1f70fcde871e01c0d7185979141804d541a2391714f3a30bc140ec7`.
- Matching five positive tags, SHA-256
  `c923ffff272f87b9a93b78be7ba523c6b3b059399a1079af041b15cfbfaae712`.
- Shared creator embedding width 8 and tag embedding width 8; DIN attention
  width 64; head 64/32; dropout 0.1; Adam/SparseAdam 0.001; batch 65,536;
  prediction batch 262,144; maximum three epochs; patience one; 16 threads.
- Zero residual must reproduce the parent within `1e-6`; epoch zero is rollback.

Continue only if validation and forward primary each improve `>= +0.0003`,
component deltas stay `>= -0.0005`, all established slices stay
`>= -0.001`, and RSS is below 60 GB. A pass repeats unchanged on middle and
late; at least two windows must pass. Only then build official state, train
three seeds, and require a fixed consensus gain `>= +0.0003` with seed and
slice safety.

Stop at a failed gate, convergence, 50 counted attempts, six hours, or resource
risk. Closing Run78 does not stop the 72-hour campaign. Public-test/hidden
labels and all submission or external actions remain locked.
