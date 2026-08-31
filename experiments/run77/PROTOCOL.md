# Run 77 protocol: exact-parent target-aware tag history

Started: 2026-08-31 12:37 SGT

## Frozen hypothesis

A compact DIN-style residual over the last five strictly causal positive tags
can correct the exact Run52 ordering because it models candidate/history
relevance directly, unlike the failed ordinary-field sequence encodings.

## Exact first attempt

- Split: `shadow_early`; seed: `2027`.
- Parent checkpoint: exact Run52 rank-32 repeat-affinity FM, SHA-256
  `a55600b5348abcf1d959576efbcbd0b7612c4d3dadd03d7cb479cbe077cdf3d8`.
- Parent prediction archive SHA-256:
  `8d2392915731af585177bbb79287fc391629dea2fbce9f1faab0c965db911872`.
- Causal sequence archive SHA-256:
  `c923ffff272f87b9a93b78be7ba523c6b3b059399a1079af041b15cfbfaae712`.
- Residual: tag width 16; DIN attention width 64; head widths 64/32;
  dropout 0.1; Adam 0.001; batch 65,536; prediction batch 262,144;
  maximum three epochs; patience one; 16 CPU threads.
- Final layer starts at zero. Epoch zero must reproduce the supplied parent
  within `1e-6`; it is retained if no epoch improves by more than `1e-5`.

## Gates

1. Continue only if validation and forward primary each improve at least
   `+0.0003` versus exact Run52, neither GAUC nor nDCG@5 regresses more than
   `0.0005`, every fixed slice stays above `-0.001`, and peak RSS stays below
   60 GB.
2. A pass repeats the exact configuration on middle and late shadows. At least
   two of three windows must clear the same gain, with no aggregate below
   `-0.0005` and no slice below `-0.001`.
3. Only then build the missing causal archives and train official seeds
   2027-2029. Require paired mean gain `>= +0.0003`, no seed below `-0.0005`,
   span `<= 0.002`, and a fixed equal-rank consensus gain `>= +0.0003` with
   slice safety.
4. Stop this run at a gate failure, convergence, 50 counted attempts, six
   hours, or resource risk. Closing this run does not stop the 72-hour campaign.

No public-test/hidden labels, submission, upload, push, organizer contact,
credentials, registration change, or visibility change are authorized. All
scores are deterministic 1/32 development-sample evidence only.
