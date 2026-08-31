# Run88 report: majority pairwise rank consensus rejected

Run88 tested one parameter-free list-level aggregation rule on the frozen Run83
causal seed predictions. Rather than average each candidate's rank, it awarded
points for defeating other candidates in a majority of members. Exact code,
protocol, and tests were committed as `fccc74d` before scoring. Ten targeted and
102 complete tests passed.

## Results

| Window | Mean-rank parent | Pairwise majority | Delta | Forward parent | Pairwise forward | Delta |
|---|---:|---:|---:|---:|---:|---:|
| Early | 0.6175101512 | 0.6173602999 | -0.0001498512 | 0.6048488365 | 0.6048242878 | -0.0000245488 |
| Middle | 0.6121450621 | 0.6120988983 | -0.0000461638 | 0.5899162903 | 0.5900481425 | +0.0001318523 |

The frozen gate required at least `+0.0002` on both validation and forward in
two of three chronological windows. Early failed both; middle regressed
validation and missed the forward threshold. Two-of-three was therefore
impossible, so the family closed after two successful executions without a
late-window or official-validation application. No voting, tie-break, member,
weight, threshold, or calibration alternative was tried.

Both attempts loaded no official final-test outcomes and took `23.851929`
subprocess seconds in total; maximum peak RSS was `2,199,683,072` bytes. The
ignored early prediction archive is 587,639 bytes with SHA-256
`854f73b30468e387ab8bb2c780357c4bf06333c3094bd72c772e7f6451422eed`;
the middle archive is 264,729 bytes with SHA-256
`3673cd69cc0ca4a590feb0f25e92dc2af4ccb8f9226f0609f503ae2413671927`.

The initial state mistakenly used a rounded future `18:30` start although the
authoritative pre-score commit occurred at `18:26:25`; raw negative campaign
offsets remain preserved and the correction is disclosed in the journal.
Run84 remains protected at primary `0.605374519999571`. Nothing was submitted,
uploaded, pushed, or made public.
