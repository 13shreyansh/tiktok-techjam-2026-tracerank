# Run 81 protocol: exact-parent primary-aligned LambdaLoss

Started: **2026-08-31 14:57:00 SGT**.

## Frozen candidate

- Parent: exact Run52 rank-32 seed-2027 `shadow_early` checkpoint and prediction
  archive, feature set `history_item_repeat`, legacy Run52 initialization.
- Training groups: every eligible training user with both labels. Use at most
  five positives selected by the seed-2027 generator and the twenty
  highest-parent-score negatives. Rank positions and nDCG swap deltas are
  computed against each user's complete parent-scored training list.
- Loss: one half positive-count-weighted per-user pairwise softplus (GAUC proxy)
  plus one half equally weighted per-user nDCG@5 swap-weighted softplus. Update
  the exact sparse latent and linear tables with SparseAdam learning rate
  `0.00002`, 64 users per batch, one epoch, 16 threads. No other setting varies.

## Gates and stopping

- Before training, stored validation predictions must reproduce with maximum
  absolute error `<= 1e-6` and all constructed rows, weights, and outputs must
  be aligned and finite.
- Continue only if the trained epoch improves validation and forward primary
  each `>= +0.0003`, keeps GAUC and nDCG@5 deltas each `>= -0.0005`, keeps every
  fixed activity/date slice primary delta `>= -0.001`, and peaks below
  60,000,000,000 bytes RSS.
- A pass repeats unchanged on middle and late; at least two of three windows
  must pass before the three official seeds and a fixed equal within-user-rank
  consensus. A first-gate failure closes this loss without rate, pair-cap,
  sampling, component-weight, epoch, blend, route, feature, or rank search.
- Stop at the first failed gate, artifact/resource failure, 50 attempts, or six
  hours. Closing Run81 does not stop the 72-hour campaign.

Public-test/hidden labels and all external actions remain locked.
