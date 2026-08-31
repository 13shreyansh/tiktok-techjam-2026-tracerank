# Run 20 report: KuaiRand-1K causal recent-interest profile

## Decision

Rejected after two counted executions. Attempt 1 failed before training because
the encoder field declaration omitted three content fields; the defect and its
incorrect negative elapsed receipt are preserved. A regression test was added,
and the unchanged attempt 2 completed but regressed validation, forward
validation, and the minimum robustness slice. No public-test labels were
evaluated.

| Measure | Paired content FM | Sequence-profile FM | Change |
|---|---:|---:|---:|
| Early validation primary | 0.636106651 | 0.633099226 | -0.003007425 |
| Forward primary | 0.641647569 | 0.640281128 | -0.001366442 |
| Minimum robustness slice | 0.573007340 | 0.570044071 | -0.002963269 |

The repaired command completed in 54.812 seconds with 3,799,302,144-byte
maximum RSS. The failed command consumed 5.244 seconds with 1,008,140,288-byte
peak RSS. Exact commands, output/error tails, code hashes, metrics, return
codes, and resource readings are in `experiments/run20/ledger.jsonl`.

The ignored early/middle/late/official profile hashes and the zero-inversion
causal contract are recorded in the decision journal. The protected Run 16
candidate remains `0.6537467530366082`.
