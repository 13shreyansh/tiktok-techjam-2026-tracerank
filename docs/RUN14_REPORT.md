# Run 14 report: median-rank consensus

## Decision

Rejected after eight successful attempts. Median within-user rank did not meet
the fixed +0.0003 validation-and-forward gate in either the early or middle
chronological window. Two failures made the required two-of-three result
impossible, so the late-window compute and official-validation check were
stopped. Public-test labels were not evaluated.

## Results

| Window | Mean-rank validation | Median validation | Change | Mean-rank forward | Median forward | Change |
|---|---:|---:|---:|---:|---:|---:|
| Early | 0.617463599 | 0.617297647 | -0.000165952 | 0.604844990 | 0.604891859 | +0.000046870 |
| Middle | 0.612474178 | 0.612524009 | +0.000049831 | 0.590173913 | 0.590387874 | +0.000213961 |

The early median regressed low activity, high activity, early dates, and late
dates; only medium activity improved. The middle median improved four slices by
small amounts but reduced low activity by 0.000139384. Neither window approached
the fixed gate.

## Accounting and conclusion

Four missing seed models and four paired aggregation checks used 539.56
subprocess seconds. Maximum recorded RSS was 3,898,982,400 bytes. Exact commands,
metrics, subgroup slices, hashes, return codes, and resource readings are in
`experiments/run14/ledger.jsonl`.

This family supports keeping mean within-user rank, not adding a new candidate.
The protected Run 2 six-member fallback remains official validation primary
0.605400885 with its original hashes and organizer-format-checked CSV.
