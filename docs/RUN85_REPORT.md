# Run85 report: strict-skip history gate

Run85 tested one frozen hypothesis: preserve the causal positive long-view
history and add a separate causal history of prior non-clicked, non-long-view
impressions watched for at most 5% of their duration. The training-only audit,
protocol, code, and unit tests were committed before scoring at `724a042`.

## Result

The only counted attempt was
`001-dual-history-seed2027-shadow-early`. It completed successfully on MPS in
46.96 s with peak RSS 3,443,834,880 bytes. It did not load or evaluate official
final-test outcomes.

| Evidence | Run83 parent | Run85 | Delta |
|---|---:|---:|---:|
| early-shadow validation GAUC | 0.6738564372 | 0.6738381386 | -0.0000182986 |
| early-shadow validation nDCG@5 | 0.5599591136 | 0.5602073073 | +0.0002481937 |
| early-shadow validation primary | 0.6169077754 | 0.6170227528 | +0.0001149774 |
| forward primary | 0.6040810347 | 0.6045639515 | +0.0004829168 |
| cold/low-activity primary | 0.6274745515 | 0.6283126561 | +0.0008381046 |
| high-activity primary | 0.5669689051 | 0.5660796475 | -0.0008892577 |

The predeclared first gate required at least `+0.0005` validation primary. The
candidate missed that gate despite forward improvement, and its benefit was
activity-dependent. The family therefore closed after one counted execution;
no seeds, thresholds, history lengths, or blends were searched after seeing
the result.

## Decision

Run85 is not promoted. The immutable clean Run84 candidate remains protected
at official-validation primary `0.605374519999571`. The experiment result and
model/prediction files remain ignored local evidence. Nothing was submitted,
uploaded, pushed, or made public.
