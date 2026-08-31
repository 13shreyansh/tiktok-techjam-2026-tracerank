# Run89 report: causal self-attentive history encoder rejected

Run89 tested one compact SASRec-inspired mechanism on the Pure causal
sequence-NFM: a single causal Transformer layer encoded the ordered last 20
positive video/tag events before the existing candidate-conditioned attention.
No upstream code was copied; the mechanism used installed PyTorch primitives.
The exact implementation and protocol were committed as `4dcebff` before
scoring. The primary concept source is the original SASRec paper:
https://arxiv.org/abs/1808.09781.

## Result

| Evidence | Run83 seed-2027 parent | Run89 | Delta |
|---|---:|---:|---:|
| early validation GAUC | 0.6738564372 | 0.5453112125 | -0.1285452247 |
| early validation nDCG@5 | 0.5599591136 | 0.4771830738 | -0.0827760398 |
| early validation primary | 0.6169077754 | 0.5112471581 | -0.1056606174 |
| forward primary | 0.6040810347 | 0.5251098275 | -0.0789712071 |

Every activity/date slice also regressed; the worst was medium activity at
`-0.1328274981`. The opening gate required `+0.0005` validation and
nonnegative forward transfer, so this was a catastrophic failure rather than a
near miss. A plausible explanation is that normalized Transformer outputs
overwhelmed the small embedding geometry used by candidate/history dot
attention, but this is an inference, not a separately proven cause. The family
closed after one execution without scaling, normalization, layer, head, width,
position, history, optimizer, loss, seed, window, or blend tuning.

The attempt completed on MPS in `84.690969` seconds with peak RSS
`7,821,934,592` bytes and no official final-test outcomes loaded. The ignored
checkpoint is 3,383,491 bytes with SHA-256
`098cb464ddb603901a3b10e4c814960a5d10d838cbc8f109d28903cf91f78108`;
the prediction archive is 536,373 bytes with SHA-256
`3ac491e34dbb526bc7f4785c914f165556213c7b93525c26d42c22993b962a4f`.
Run84 remains protected at primary `0.605374519999571`. Nothing was submitted,
uploaded, pushed, or made public.
