# Run90 result: dual-timescale positive history

Run90 tested one frozen change to the selected causal sequence-NFM: retain its
candidate-attended last-20 positive-history profile and append a separately
normalized profile over the last five history slots. The exact implementation
and protocol were committed before scoring.

## Opening paired gate

| Metric | Run83 parent | Run90 | Delta |
|---|---:|---:|---:|
| early validation GAUC | 0.6738564372 | 0.6740555763 | +0.0001991391 |
| early validation nDCG@5 | 0.5599591136 | 0.5608751774 | +0.0009160638 |
| early validation primary | 0.6169077754 | 0.6174653769 | +0.0005576015 |
| forward GAUC | 0.6495336890 | 0.6493378878 | -0.0001958013 |
| forward nDCG@5 | 0.5586284399 | 0.5588054061 | +0.0001769662 |
| forward primary | 0.6040810347 | 0.6040716171 | -0.0000094175 |

Slice-primary deltas were `+0.0013057374` cold/low activity,
`+0.0005169563` medium activity, `-0.0012083505` high activity,
`+0.0003230447` early dates, and `-0.0003148116` late dates.

The validation magnitude passed, but forward primary was negative and the
high-activity slice crossed the frozen `-0.001` floor. The protocol therefore
closes the family after one successful attempt. No tuning, second seed, later
window, official build, or promotion was performed.

## Accounting and artifacts

- Attempt: `001-dual-timescale-shadow-early-seed2027`
- Wall time: `44.5845160484314` seconds
- Campaign elapsed at start: `3763.898483` seconds
- Maximum RSS: `3,424,583,680` bytes
- Result JSON SHA-256: `e7ed0dfa68e1d00825c3371085e74fedd8c17742360f8267dfc7a430dcb61007`
- Saved checkpoint SHA-256:
  `160a412cad925815d3833f2417f9ef374de82a05e8bcc20c53d674aadbdae64c`
- Prediction archive SHA-256: `3aa46d501b6ded0f2dee9d5ca61a1a812d3be7b86b39096bac4d17cfa881f82f`
- Pre-run committed `solution/ranker.py` SHA-256:
  `41f0395368d1173097cdec6c436f02b5fbbf5529d6d9e5e5ddde35c40b882721`
- Organizer evaluator SHA-256:
  `ecfde28392eb14fec4f488083251df50624e1af2b86278b962daecfb42d195de`
- Official-test outcomes loaded: `false`

The immutable raw ledger omitted structured `forward_valid` because of a
projection defect in `scripts/run_pure_campaign_experiment.py`. The
authoritative ignored result JSON and captured stdout contain the forward
metrics. The raw ledger is preserved unchanged; the wrapper now records every
evaluation surface prospectively and has regression tests.

Run84 remains the clean protected candidate at GAUC `0.6725210738`, nDCG@5
`0.5382279662`, and primary `0.6053745200`. Nothing was submitted, uploaded,
pushed, or evaluated on official final-test outcomes.
