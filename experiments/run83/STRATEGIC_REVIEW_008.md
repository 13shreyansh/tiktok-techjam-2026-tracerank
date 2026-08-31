# Run 83 strategic review after attempt 8

Reviewed: **2026-08-31 16:23 SGT**.

## Question and evidence boundary

Run83 asks only whether strictly chronological per-user histories transfer more
reliably than the legacy source-row traversal for the already frozen Pure
sequence-FM architecture. The first eight counted attempts cover the complete
`shadow_early` window: three paired seeds and one fixed equal within-user rank
consensus per side. All eight attempts exited zero. No official validation,
public test, hidden test, adaptive subset, member, weight, or hyperparameter was
used or selected.

## Early-window result

| Measure | Source consensus | Causal consensus | Causal - source |
|---|---:|---:|---:|
| validation primary | 0.6172166108 | 0.6175101512 | +0.0002935404 |
| validation GAUC | 0.6738987531 | 0.6740351348 | +0.0001363817 |
| validation nDCG@5 | 0.5605344684 | 0.5609851675 | +0.0004506991 |
| forward primary | 0.6045709776 | 0.6048488365 | +0.0002778589 |
| forward GAUC | 0.6500035867 | 0.6504594651 | +0.0004558784 |
| forward nDCG@5 | 0.5591383685 | 0.5592382080 | +0.0000998395 |

The paired validation-primary changes at seeds 2026, 2027, and 2028 are
`+0.0006642342`, `+0.0002731085`, and `+0.0001647472`; the paired mean is
`+0.0003673633`, with three of three positive. Paired forward-primary changes
are `+0.0000081062`, `+0.0002478361`, and `+0.0006400347`.

The fixed causal-consensus slice-primary changes are: cold/low activity
`+0.0002431965`, medium activity `+0.0001555422`, high activity
`+0.0008872666`, early dates `-0.0000919802`, and late dates
`-0.0000048463`. Every slice is within the frozen `-0.001` floor. Neither
component regresses on either aggregate period. The early window therefore
**supports causal selection** under every precommitted gate.

## Skeptical review

- The aggregate gains remain small, so one window is not enough evidence for
  final selection. The official Run82 gain can still be noise or specific to
  one time range.
- The causal and source histories differ only when file order and event time
  disagree. That makes the test targeted, but it cannot establish that the
  sequence architecture itself is optimal.
- The high-activity slice improves most, while two date slices are nearly flat
  and slightly negative. This is acceptable under the frozen floor but is a
  reason not to relax the two-of-three-window requirement.
- The comparator deliberately recreates a chronology flaw. It is audit-only
  and must never enter the candidate package, regardless of its score.
- Repeated shadow-window checks consume adaptive evidence. Run83 prevents
  mid-run tuning; after the frozen windows, these same results must not be used
  to invent a new architecture or weighting search.

## Decision

Continue unchanged to the predeclared `shadow_middle` paired audit. Do not
promote an artifact yet. The protected Run2 mixed fallback remains untouched;
the only possible later decision is whether the already frozen Run82
all-causal ensemble is a more defensible final Pure artifact.

Accounting at this checkpoint: 8/50 attempts, 8 successful, 228.251 summed
command-seconds, 3,749,429,248-byte maximum RSS, and zero public-test
evaluations.
