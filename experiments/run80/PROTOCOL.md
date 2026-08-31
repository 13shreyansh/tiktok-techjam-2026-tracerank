# Run 80 protocol: frozen-embedding DeepFM residual

Started: **2026-08-31 14:49:03 SGT**.

## Frozen candidate

- Parent: exact Run52 rank-32 seed-2027 `shadow_early` checkpoint and stored
  predictions. All sparse latent and linear rows stay frozen.
- Residual input: concatenation of the parent's 24 field embeddings, each width
  32. No raw IDs outside those frozen vectors and no additional features.
- Tower: linear 768→32, ReLU, dropout 0.1, linear 32→16, ReLU, dropout 0.1,
  linear 16→1. The final layer starts at zero; output is parent logit plus tower.
- Adam learning rate 0.001, batch 65,536, prediction batch 262,144, seed 2027,
  16 CPU threads, maximum three epochs, patience one. Pointwise binary logloss
  matches the exact parent objective. No setting may change after scoring.

## Gates and stopping

- A pre-score smoke test and full epoch-zero pass must reproduce stored parent
  validation predictions with maximum absolute error `<= 1e-6`.
- First trained epoch must improve validation and forward primary each
  `>= +0.0003`, keep both GAUC and nDCG@5 deltas each `>= -0.0005`, keep every
  fixed slice primary delta `>= -0.001`, peak below 60,000,000,000 bytes RSS,
  and produce finite hashed artifacts.
- A pass repeats unchanged on middle and late; at least two of three windows
  must pass before three official seeds and a fixed equal within-user rank
  consensus. A first-gate failure closes this tower without width, dropout,
  rate, epoch, loss, feature, unfreezing, blend, or route search.
- Stop at convergence, first failed gate, resource/artifact failure, 50
  attempts, or six hours. Closing Run80 does not stop the 72-hour campaign.

Public-test/hidden labels and all external actions remain locked.
