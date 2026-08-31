# Run 29 protocol: KuaiRand-27K user-balanced objective

Started: **2026-08-29 23:54 SGT**.

## Independent question

Can aligning row-wise BCE more closely with per-user-averaged GAUC and nDCG@5
improve the protected causal history-item model without over-amplifying sparse,
noisy users?

## Fixed first candidate

- Exact Run 24 `history_item` representation, rank 8, caches, optimizer,
  learning rate, epoch limit, batching, split, and seed.
- Weight each training row by its training user's row count to power `-0.5`,
  normalized to mean one. The square-root compromise is fixed before scoring;
  no alpha or clipping sweep is allowed.
- First score: `shadow_early`, paired to Run 24 attempt 21.

## Gates and limits

Require +0.001 validation primary, no more than -0.0005 forward, and no slice
regression beyond -0.001. A passing candidate repeats unchanged on middle and
late and must pass two of three before three paired official seeds. Stop at
family failure, official epsilon 0.002 / N=3 convergence, 50 attempts, or six
hours. Run 29 is separately and cumulatively disclosed; public-test/hidden
labels, submission, upload, push, contact, credentials, and release are locked.
