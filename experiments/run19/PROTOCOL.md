# Run 19 protocol: KuaiRand-1K within-user ranking

Started: **2026-08-29 20:35 SGT**.

## Independent question

Can the content sparse FM improve per-user GAUC and nDCG@5 when its pointwise
checkpoint is followed by one ranking-loss epoch that compares positive and
negative videos across each user's full training history, rather than only
inside one simultaneous impression?

This directly matches the evaluator's per-user grouping and the organizer
workshop's instruction to score and order candidates for each person. It uses
only training-split `long_view` labels. It does not use validation/test labels,
future rows, or list-level re-ranking at prediction time.

## Fixed first candidate

- Exact Run 16 `content` sparse FM and chronological `shadow_early` split.
- Pointwise parent settings unchanged: rank 16, seed 2027, learning rate 0.001,
  batch 65,536, 20 epochs maximum, patience 4.
- One BPR epoch over at most 1,024 sampled positive/negative pairs per user,
  one uniformly sampled training negative per positive, seed fixed from 2027.
- Pairwise learning rate 0.0002 and batch size 32,768, inherited from the
  earlier bounded pairwise test so no score-driven tuning occurs.
- Paired parent: Run 16 attempt 8 content sparse FM.

## Gates and limits

Unit tests must prove every pair shares a user, has positive left and negative
right labels, respects the per-user cap, and never reads outside training rows.
The first shadow must improve primary by at least 0.001, lose no more than
0.0005 forward, and avoid any unexplained slice regression larger than 0.001.
If it passes, repeat unchanged on middle and late; require two of three windows
before official validation. Stop this run at its family gate, official epsilon
`0.002` / `N=3` convergence, 50 attempts, or six hours.

No public-test label evaluation, hidden-test access, submission, upload, push,
contact, credential use, registration change, or visibility change. Protected
KuaiRand-1K score `0.6537467530366082` remains immutable.
