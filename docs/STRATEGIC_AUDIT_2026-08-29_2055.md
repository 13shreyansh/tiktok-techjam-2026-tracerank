# Fresh-context strategic audit — 2026-08-29 20:55 SGT

## Decision

Pause new KuaiRand-1K model families and shift the next benchmark run to the
checksum-verified KuaiRand-27K bonus data when acquisition completes. This is
not a global stop: the active goal continues, the 27K download is running, and
the next run will begin only after schema, licence, split, and resource
feasibility are observed.

## Evidence

- Required KuaiRand-Pure: 115 attempts across Runs 1-15. The protected
  six-member user-rank ensemble scores `0.605400885`, versus the published
  `0.6016` FM validation baseline. DIN, GRU, listwise/pairwise, multi-behavior,
  context, aggregate, caption/category, and multiple ensemble families did not
  produce a robust successor.
- Optional KuaiRand-1K: Run 16's content sparse FM seed 2028 scores
  `0.653746753` and passed all three chronological shadow windows. Runs 17-23
  tested DeepFM, field-aware FM, user-wide BPR, causal recent-interest memory,
  unrestricted exact user crosses, additive-only crosses, and fixed cross
  shrinkage. None passed the predeclared validation/forward/slice gate.
- The most informative rejected result was Run 22: all validation slices
  improved and primary gained `+0.006350056`, but forward primary regressed
  `-0.001664701`. Run 23's one fixed shrinkage coefficient barely changed it.
  This closes the cross branch without a validation-driven sweep.
- KuaiRand-27K is explicitly an optional organizer bonus benchmark and offers
  a materially different scale: 27,285 users, 32,038,725 items, and
  322,278,385 interactions. It is the highest-value remaining independent
  source of long-sequence evidence, subject to local feasibility.

## Safeguards for the next run

1. Accept the 27K archive only after exact 9,892,191,178-byte and official MD5
   verification, safe-entry inspection, extraction, and embedded-licence audit.
2. Inspect the observed schema and dates before defining any split or model.
3. Start with a memory-bounded unmodified/simple baseline; do not claim a score
   until the documented command exits zero.
4. Declare the 27K run protocol before model scoring and report its own 50/
   six-hour/convergence counters plus cumulative totals.
5. Keep Pure `0.605400885` and 1K `0.653746753` artifacts immutable. Do not
   submit, upload, push, expose secrets, or alter repository visibility.
