# Run 17 report: KuaiRand-1K DeepFM interactions

## Decision

Rejected after one successful, predeclared attempt. A compact nonlinear tower
over the exact content sparse-FM fields regressed validation, forward
validation, and every robustness slice, so the family was closed without
hyperparameter tuning. No public-test labels were evaluated.

| Measure | Paired content FM | DeepFM | Change |
|---|---:|---:|---:|
| Early validation primary | 0.636106651 | 0.626560563 | -0.009546088 |
| Forward primary | 0.641647569 | 0.631056253 | -0.010591317 |
| Minimum robustness slice | 0.573007340 | 0.551010503 | -0.021996837 |

The command completed in 67.127 seconds with 3,157,721,088-byte maximum RSS.
The unchanged evaluator SHA-256 was
`ecfde28392eb14fec4f488083251df50624e1af2b86278b962daecfb42d195de`.
Exact command, output tail, code hash, metrics, slices, return code, and resource
reading are in `experiments/run17/ledger.jsonl`.

Run 17 was opened only after a live source re-read confirmed that the official
limits are worded per benchmark run. The statement still does not define when
a restart is legitimate. This run is therefore reported both separately and
inside cumulative Track 2 accounting; it is not represented as an
organizer-approved reset. The protected Run 16 candidate remains
`0.6537467530366082`.
