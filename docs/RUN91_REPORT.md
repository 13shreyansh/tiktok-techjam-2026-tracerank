# Run91 result: separate explicit-engagement history rejected

Run91 preserved the selected causal long-view video/tag history and added one
independently attended history containing only strictly earlier likes, follows,
comments, or forwards. This isolated the workshop's strong-action clue without
mixing it into the parent sequence or using it as an auxiliary label.

## Opening paired gate

| Metric | Run83 parent | Run91 | Delta |
|---|---:|---:|---:|
| early validation GAUC | 0.6738564372 | 0.6736089587 | -0.0002474785 |
| early validation nDCG@5 | 0.5599591136 | 0.5596889853 | -0.0002701283 |
| early validation primary | 0.6169077754 | 0.6166489720 | -0.0002588034 |
| forward GAUC | 0.6495336890 | 0.6501308084 | +0.0005971193 |
| forward nDCG@5 | 0.5586284399 | 0.5589382648 | +0.0003098249 |
| forward primary | 0.6040810347 | 0.6045345068 | +0.0004534721 |

The forward direction was encouraging, but the frozen opening gate required at
least `+0.0005` validation primary. Validation instead regressed, and the
high-activity slice also changed `-0.0012313562`, beyond its `-0.001` floor.
The family therefore closed after one attempt. No alternate action set,
history length, second window, seed, blend, or official build was attempted.

## Accounting and artifacts

- Attempt: `001-explicit-engagement-shadow-early-seed2027`
- Wall time: `36.42805314064026` seconds
- Campaign elapsed at start: `82.31248` seconds
- Maximum RSS: `3,425,894,400` bytes
- Result JSON SHA-256:
  `f0c6f672ad55402d6003618e9f18c5b32d5b7b516a51fb22b4cc6c38d4279fea`
- Saved checkpoint SHA-256:
  `b01422598825e163e12b82d5f3ae094886cdb33cb7cd373292a1c45027ae6ae2`
- Prediction archive SHA-256:
  `4f2e8a98b7a7daec41cf1a7d34943ded52acddc018885358a7e1ee34ef260396`
- Pre-run committed `solution/ranker.py` SHA-256:
  `a7849d0057793a5ffd1aafa92cefe18040c25a08a761dd3b02a2f879f71a5476`
- Organizer evaluator SHA-256:
  `ecfde28392eb14fec4f488083251df50624e1af2b86278b962daecfb42d195de`
- Official final-test outcomes loaded: `false`
- Fitted preprocessing and behavior-history splits: training only

Run84 remains the clean protected candidate at GAUC `0.6725210738`, nDCG@5
`0.5382279662`, and primary `0.6053745200`. Nothing was submitted, uploaded,
pushed, or evaluated on official final-test outcomes.
