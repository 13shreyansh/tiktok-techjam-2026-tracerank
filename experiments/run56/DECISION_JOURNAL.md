# Run 56 decision journal

## 2026-08-31 07:20 SGT — hard-pair update frozen

- Reuse the exact Run35 hard-pair algorithm and parameters on the changed
  Run52 rank-32 repeat-affinity representation.
- Epoch zero is the parent and rollback is mandatory if no improvement occurs.
- Begin with seed-2027 early only; preserve Run52 regardless of outcome.

## 2026-08-31 07:21 SGT — pairwise gain is noise-sized; branch closes

- Attempt 1 completed successfully in `45.352509` seconds with
  `42,110,435,328`-byte peak RSS and 128,765 training-only hard pairs.
- Pairwise epoch 1 improved validation by only `+0.0000582707474815`;
  epochs 2 and 3 deteriorated. Forward primary changed
  `-0.0001621568851012`.
- GAUC changed `-0.0000530960836893`, nDCG@5
  `+0.0001696375786523`; every slice stayed near zero, between
  `-0.0000462041496362` and `+0.0001079474280712`.
- The ignored 3,786,952,349-byte checkpoint SHA-256 is
  `331d6e70ae1724d9e12b533e38581b2b7f0c7e0e0fb3f4dc8fe1776f4fb6d602`;
  the 6,601,075-byte prediction archive SHA-256 is
  `3d95019d09cdd0ebce42efb188ff7de22f85586fc75863f72ed5aa46bdaa9d52`.
- Stop without later shadows, official seeds, pair sampler, loss, rate, epoch,
  pair-cap, or ensemble variants. Run52 remains protected.
