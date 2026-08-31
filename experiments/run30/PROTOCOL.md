# Run 30 protocol: KuaiRand-27K expanded training density

Started: **2026-08-29 23:57 SGT**.

## Independent question

Does four times denser deterministic training data improve the protected causal
history-item ranker when every validation and forward comparison uses the exact
same fixed 1/32 rows as Run 24?

## Locked data design

- Build one label-safe April 8–28 cache from SplitMix64 residue 0 modulo 8.
- Training indices use every retained 1/8 row. Validation and forward indices
  additionally require residue 0 modulo 32, making them exactly the original
  Run 24 evaluation sample. Verify ordered `(user, source video, time, date,
  label)` equality before any model score.
- Build the same eight causal user-history and four full-corpus prior-day
  video/author fields. The item statistics remain based on all official earlier
  development events; only the trainable row density changes.
- First candidate: exact Run 24 rank-8 sparse FM, optimizer, learning rate,
  epoch/patience limits, batching, seed 2027, and `shadow_early` split.

## Gates and limits

Require +0.001 validation primary, no more than -0.0005 forward, and no slice
regression beyond -0.001. A passing candidate repeats unchanged on middle and
late and must pass two of three before three paired official seeds. Stop at
family failure, official epsilon 0.002 / N=3 convergence, 50 attempts, or six
hours. Preprocessing is recorded separately from model iterations.

Run 30 is separately and cumulatively disclosed; no organizer-approved reset
is claimed. Rows after April 28 are rejected before outcome interpretation.
Public-test/hidden labels, submission, upload, push, contact, credentials,
registration change, and public release remain locked.
