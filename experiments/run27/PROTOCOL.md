# Run 27 protocol: KuaiRand-27K interaction capacity

Started: **2026-08-29 23:47 SGT**.

## Independent question

Does increasing the sparse factorization machine interaction rank from 8 to 16
improve the protected Run 24 causal user-item representation on a much larger
item vocabulary without sacrificing temporal transfer or activity slices?

## Fixed first candidate

- Exact Run 24 `history_item` fields, causal caches, split, optimizer, learning
  rate, epoch limit, early stopping, batching, and seed.
- Change only latent interaction rank from 8 to 16. This value is fixed before
  any Run 27 score and matches the organizer FM and successful 1K content-FM
  capacity; no intermediate ranks are searched.
- First score: `shadow_early`, seed 2027, paired to Run 24 attempt 21.

## Gates and limits

Require +0.001 validation primary, no more than -0.0005 forward, and no
unexplained slice regression beyond -0.001. A passing candidate repeats
unchanged on middle and late and must pass two of three before three paired
official seeds. Stop at family failure, official epsilon 0.002 / N=3
convergence, 50 attempts, or six hours.

Run 27 is separately declared and cumulatively disclosed; no organizer-approved
reset is claimed. No public-test/hidden label evaluation, submission, upload,
push, contact, credential use, registration change, or public release.
