# Run 18 protocol: KuaiRand-1K field-aware interactions

Started: **2026-08-29 20:23 SGT**.

## Independent question

Can field-aware factorization improve KuaiRand-1K ranking by giving the same
feature a different representation for each interaction partner, instead of
forcing user-video, user-tag, video-author, and all other pairs to share one FM
embedding space?

This is an independent architecture-family run, not a width or learning-rate
retry of failed Run 17. It is declared before any field-aware benchmark score.
Per-run and cumulative resources will both be disclosed because the official
statement does not define restart boundaries.

## Fixed first candidate

- Exact Run 16 label-free `content` fields and chronological `shadow_early`.
- Rank-8 field-aware FM: each active feature has a distinct 8-dimensional
  vector for each of eight target fields; all 28 field pairs are scored.
- Native long-view BCE, seed 2027, sparse learning rate 0.001, batch 65,536,
  at most 20 epochs, patience 4.
- Paired parent: Run 16 attempt 8 content sparse FM.
- Official validation remains locked.

## Gates and limits

The synthetic sparse-gradient test must pass first. The shadow candidate must
improve validation by at least 0.001, lose no more than 0.0005 forward, and
avoid an unexplained slice collapse larger than 0.001. If it passes, repeat
unchanged on middle and late; require two-of-three windows before official
validation. Promotion then requires fixed seeds 2026-2028 and the predeclared
equal within-user-rank ensemble. Stop this run at its family gate, official
epsilon `0.002` / `N=3` convergence, 50 attempts, or six hours.

No public-test label evaluation, hidden-test access, submission, upload, push,
contact, credential use, registration change, or visibility change. The
protected `0.6537467530366082` candidate remains immutable.
