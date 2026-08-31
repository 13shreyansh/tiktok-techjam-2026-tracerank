# Run 19 report: KuaiRand-1K within-user ranking

## Decision

Rejected after one successful, predeclared attempt. Comparing positives and
negatives across each user's full training history improved the later forward
window, but slightly regressed paired validation and materially regressed the
medium-activity slice. No public-test labels were evaluated.

| Measure | Paired content FM | Within-user BPR | Change |
|---|---:|---:|---:|
| Early validation primary | 0.636106651 | 0.635773882 | -0.000332769 |
| Forward primary | 0.641647569 | 0.642856239 | +0.001208670 |
| Medium-activity primary | 0.618670000 | 0.616692189 | -0.001977811 |

The one ranking epoch used 377,382 pairs from 944 usable users. The command
completed in 67.434 seconds with 3,964,895,232-byte maximum RSS. Exact command,
output tail, code hash, metrics, slices, return code, and resource reading are
in `experiments/run19/ledger.jsonl`.

Run 19 is reported separately and inside cumulative accounting. The positive
forward result is evidence that user-wide ranking is better aligned than
same-impression ranking, but the predeclared gate forbids promotion or tuning
from this mixed result. The protected Run 16 candidate remains
`0.6537467530366082`.
