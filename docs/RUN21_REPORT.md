# Run 21 report: KuaiRand-1K explicit user-content crosses

## Decision

Rejected after one successful, predeclared attempt. Exact user × tag/type/
duration crosses improved nearby validation but substantially regressed the
later forward window and high-activity users. This is evidence of temporal
memorization, not a promotable gain. No public-test labels were evaluated.

| Measure | Paired content FM | Explicit-cross FM | Change |
|---|---:|---:|---:|
| Early validation primary | 0.636106651 | 0.638983659 | +0.002877008 |
| Forward primary | 0.641647569 | 0.635062470 | -0.006585099 |
| High-activity primary | 0.573007340 | 0.564250744 | -0.008756595 |

The command completed in 85.816 seconds with 3,339,239,424-byte maximum RSS.
Exact command, output tail, code hash, metrics, slices, return code, and resource
reading are in `experiments/run21/ledger.jsonl`. The protected Run 16 candidate
remains `0.6537467530366082`.
