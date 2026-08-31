# Strategic audit — 2026-08-31 16:07 SGT

## Current truth

The required KuaiRand-Pure protected result remains primary
`0.6054008850379737` (GAUC `0.6723790951304006`, nDCG@5
`0.5384226749455467`) versus published baseline `0.6016`. Run82's fixed
all-causal alternate reached primary `0.6055212246527164`, but its
`+0.0001203396147427` gain missed the precommitted `+0.0002` promotion gate.
It passed every component and slice floor and is preserved as a safer-provenance
alternate without changing the protected artifact.

The strongest optional results are KuaiRand-1K primary
`0.6537467530366082` and KuaiRand-27K deterministic 1/32 development-sample
primary `0.6534977984044839`. These values are not comparable to Pure or to
each other, and neither is a hidden-test or leaderboard score. The official
primary oracle reference is about `0.8645`, so `0.99` is not a meaningful
target under the published metric.

## Third-person process audit

The process is strong on leakage controls, immutable commands, chronological
forward gates, fixed activity/date slices, exact rollback, seed replication,
hashing, resource receipts, and refusing to select public/hidden-test labels.
Through Run82 the ledgers record 294 executions, 285 successes, 9 failures,
`75,781.269` subprocess seconds, and maximum measured RSS
`45,375,324,160` bytes. Each individual campaign stayed below 50 attempts and
six hours. The current goal counter reports 12,500,758 combined tokens and
140,234 seconds; the product still does not expose a trustworthy input/output
split.

The largest strategic error is allocation: after establishing Pure at
`0.605400885`, much of the later research targeted optional 1K/27K branches.
The 27K branch produced real local progress, but only on a deterministic 1/32
development evaluation sample. It does not establish full-benchmark transfer
and cannot compensate for a weak required-benchmark hidden score. Several
judge-facing files also retained stale Run49 and 141-execution snapshots; the
README and solution report are corrected in this audit, while the detailed
resource/disclosure reports remain explicitly dated and require final refresh.

## Failure map and next decision

Extra depth, wider embeddings, DeepFM residuals, explicit listwise/Lambda and
BPR fine-tuning, extra categorical fields, multi-action targets, recent
sequence tails, time context, class balancing, routing, and tree residuals all
failed at least one frozen transfer, component, or slice gate. These failures
show that the current models overfit quickly: training loss continues to fall
after validation ranking deteriorates, and apparent nDCG gains often trade away
GAUC or high-activity/forward performance.

The next work should return exclusively to required Pure. First compare the
protected mixed ensemble and all-causal alternate on genuinely chronological
windows without tuning weights or subsets. Then test only a genuinely new
candidate-aware history/list mechanism with a frozen gate; do not spend another
run on minor capacity, learning-rate, seed, or blend variations. Preserve both
current Pure artifacts until hidden-test delivery is understood. In parallel,
refresh resource/human-intervention accounting and run the release/readiness
gates so model research cannot leave an unusable final package.
