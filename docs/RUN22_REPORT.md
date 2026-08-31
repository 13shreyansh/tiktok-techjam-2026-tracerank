# Run 22 report: KuaiRand-1K additive wide user crosses

## Decision

Rejected after one successful, predeclared attempt. Restricting exact user
crosses to additive weights produced a large validation gain and improved every
validation slice, but the later forward window regressed beyond the fixed
transfer guard. No public-test labels were evaluated.

| Measure | Paired content FM | Additive wide-cross FM | Change |
|---|---:|---:|---:|
| Early validation primary | 0.636106651 | 0.642456707 | +0.006350056 |
| Forward primary | 0.641647569 | 0.639982868 | -0.001664701 |
| High-activity primary | 0.573007340 | 0.575959311 | +0.002951971 |

The command completed in 76.994 seconds with 3,153,231,872-byte maximum RSS.
Exact command, output tail, code hash, metrics, slices, return code, and resource
reading are in `experiments/run22/ledger.jsonl`. The result motivates an
independently predeclared shrinkage architecture but is not itself promoted.
The protected Run 16 candidate remains `0.6537467530366082`.
