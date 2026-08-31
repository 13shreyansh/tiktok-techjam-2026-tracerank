# Run 23 protocol: KuaiRand-1K regularized additive user crosses

Started: **2026-08-29 20:52 SGT**.

## Independent question

Can direct L2 shrinkage on the four additive user-cross weights preserve Run
22's broad validation benefit while reducing its small forward regression?
The penalty applies only to active cross linear weights; the proven content FM
representation and optimization remain unchanged.

This is a separately declared regularized model family, not a retroactive
promotion of Run 22. The standard moderate coefficient `0.01` is fixed before
any Run 23 score and is not searched.

## Fixed first candidate

- Exact Run 22 `wide_cross_fm` architecture and cross encoder.
- Active-cross mean-square penalty coefficient 0.01.
- Chronological `shadow_early`, rank 16, seed 2027, base learning rate 0.001,
  batch 65,536, at most 20 epochs, patience 4.
- Paired parent: Run 16 attempt 8 content sparse FM; Run 22 is diagnostic
  context, not the promotion baseline.

## Gates and limits

The first shadow must improve primary by at least 0.001, lose no more than
0.0005 forward, and avoid an unexplained slice regression larger than 0.001.
If it passes, repeat unchanged on middle and late; require two of three windows
before official validation. No penalty sweep is allowed. Stop at the family
gate, official epsilon `0.002` / `N=3` convergence, 50 attempts, or six hours.

No public-test label evaluation, hidden-test access, submission, upload, push,
contact, credential use, registration change, or visibility change. Protected
KuaiRand-1K score `0.6537467530366082` remains immutable.
