# Run 23 report: KuaiRand-1K regularized additive user crosses

## Decision

Rejected after one successful, predeclared attempt. The fixed 0.01 active-cross
L2 penalty barely changed Run 22 and still failed the forward transfer guard.
No coefficient sweep or public-test label evaluation followed.

| Measure | Paired content FM | Regularized wide-cross FM | Change |
|---|---:|---:|---:|
| Early validation primary | 0.636106651 | 0.642455467 | +0.006348816 |
| Forward primary | 0.641647569 | 0.640082951 | -0.001564619 |
| High-activity primary | 0.573007340 | 0.575959048 | +0.002951708 |

The command completed in 71.142 seconds with 3,119,480,832-byte maximum RSS.
Exact command, output tail, code hash, metrics, slices, return code, and resource
reading are in `experiments/run23/ledger.jsonl`. The 1K cross branch is closed;
the protected Run 16 candidate remains `0.6537467530366082`.
