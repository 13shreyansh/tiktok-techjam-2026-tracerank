# Run 11 strategic review 001

## Fresh-context verdict

Reject and stop. The metric-aware update did not improve the model it started
from. The apparent +0.000123 final change versus a separately trained paired
control is smaller than the fixed gate and comes entirely from ordinary MPS
training variation before LambdaLoss.

| Measurement | Paired parent | Restored result | Change |
|---|---:|---:|---:|
| Validation primary | 0.616858721 | 0.616981924 | +0.000123203 |
| Forward primary | 0.603960752 | 0.603981853 | +0.000021100 |
| Low-activity primary | 0.627429026 | 0.627571721 | +0.000142695 |
| Medium-activity primary | 0.615288915 | 0.615319107 | +0.000030192 |
| High-activity primary | 0.566792935 | 0.567114721 | +0.000321786 |
| Early-date primary | 0.613376257 | 0.613349259 | -0.000026999 |
| Late-date primary | 0.611074791 | 0.611176438 | +0.000101647 |

The internal causal comparison is decisive: pointwise checkpoint 0.616981924,
after one LambdaLoss epoch 0.616863608 (-0.000118315). The command returned
zero after 390.93 seconds and used 16,949,690,368 maximum resident bytes. No
public-test labels were evaluated.

Ordinary BPR, listwise softmax, tree LambdaRank, and now neural swap-weighted
LambdaLoss have all failed controlled tests. Further loss tuning on this window
is lower value than moving to a genuinely independent representation or
validation hypothesis.
