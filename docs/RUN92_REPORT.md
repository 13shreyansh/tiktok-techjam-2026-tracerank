# Run92 result: hard target-match history expert rejected

Run92 preserved the selected soft candidate-attended positive-history profile
and appended the single valid history vector with the largest existing
candidate-dot-history score. This parameter-free hard expert tested whether
soft pooling diluted a user's most relevant earlier interest.

## Opening paired gate

| Metric | Run83 parent | Run92 | Delta |
|---|---:|---:|---:|
| early validation GAUC | 0.6738564372 | 0.6731455922 | -0.0007108450 |
| early validation nDCG@5 | 0.5599591136 | 0.5594589114 | -0.0005002022 |
| early validation primary | 0.6169077754 | 0.6163022518 | -0.0006055236 |
| forward GAUC | 0.6495336890 | 0.6491834521 | -0.0003502369 |
| forward nDCG@5 | 0.5586284399 | 0.5587339401 | +0.0001055002 |
| forward primary | 0.6040810347 | 0.6039587259 | -0.0001223087 |

Cold/low-activity primary improved `+0.0006573314`, but medium activity changed
`-0.0010512503`, high activity `-0.0035825570`, and late dates
`-0.0010522298`. The validation, forward, and three slice gates failed. The
family closed after one attempt without top-k, temperature, another window,
seed, blend, or official build.

## Accounting and artifacts

- Attempt: `001-hard-target-match-shadow-early-seed2027`
- Wall time: `42.736050844192505` seconds
- Campaign elapsed at start: `69.889253` seconds
- Maximum RSS: `3,439,919,104` bytes
- Result JSON SHA-256:
  `163966d6136b11908f7928a8017199e07b26e182c9f592e9735ae61be93c3eb1`
- Saved checkpoint SHA-256:
  `4dbf2f7f83cfccdd9bb04fa15c706b0176e46578bce7c11242ac81a0cd3089b1`
- Prediction archive SHA-256:
  `ad99b1bf30815a713366fcf19b49ffc65591bf60528d87cdd9d93a4f4e39f065`
- Pre-run committed `solution/ranker.py` SHA-256:
  `c9e6553d4f43858efe980ad844f58d58583b96ffb8fe04db8f263de2ff599ef8`
- Organizer evaluator SHA-256:
  `ecfde28392eb14fec4f488083251df50624e1af2b86278b962daecfb42d195de`
- Official final-test outcomes loaded: `false`
- Fitted preprocessing and behavior-history splits: training only

Run84 remains the clean protected candidate at GAUC `0.6725210738`, nDCG@5
`0.5382279662`, and primary `0.6053745200`. Nothing was submitted, uploaded,
pushed, or evaluated on official final-test outcomes.
