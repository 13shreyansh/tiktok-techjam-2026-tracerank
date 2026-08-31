# Run 18 report: KuaiRand-1K field-aware interactions

## Decision

Rejected after one successful, predeclared attempt. Giving every feature a
different embedding for every interaction partner regressed validation,
forward validation, and every robustness slice, so the family was closed
without hyperparameter tuning. No public-test labels were evaluated.

| Measure | Paired content FM | Field-aware FM | Change |
|---|---:|---:|---:|
| Early validation primary | 0.636106651 | 0.623862295 | -0.012244356 |
| Forward primary | 0.641647569 | 0.625255762 | -0.016391807 |
| Minimum robustness slice | 0.573007340 | 0.554531866 | -0.018475474 |

The command completed in 103.717 seconds with 9,652,256,768-byte maximum RSS.
The unchanged evaluator SHA-256 was
`ecfde28392eb14fec4f488083251df50624e1af2b86278b962daecfb42d195de`.
Exact command, output tail, code hash, metrics, slices, return code, and resource
reading are in `experiments/run18/ledger.jsonl`.

Run 18 is reported separately and inside cumulative accounting. The official
statement says the limits apply per benchmark run but does not define restart
boundaries, so this is not represented as an organizer-approved reset. The
protected Run 16 candidate remains `0.6537467530366082`.
