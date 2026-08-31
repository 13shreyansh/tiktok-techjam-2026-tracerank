# Run 21 protocol: KuaiRand-1K explicit user-content crosses

Started: **2026-08-29 20:45 SGT**.

## Independent question

Can exact low-cardinality preference tables improve ranking by removing the
rank-16 bottleneck for user-category relationships? The content FM represents
user-tag affinity through a low-rank dot product even though 1,000 users × 69
tags is small enough to learn directly.

The fixed family adds four explicit categorical crosses: user × primary tag,
user × upload type, user × video type, and user × duration decile. Cross IDs
exist only when both user and value were observed in training; validation never
creates a new learned identity.

## Fixed first candidate

- Exact Run 16 content fields plus all four predeclared crosses.
- Sparse FM, chronological `shadow_early`, rank 16, seed 2027, learning rate
  0.001, batch 65,536, at most 20 epochs, patience 4.
- Paired parent: Run 16 attempt 8 content sparse FM.
- No cross subset or parameter will be selected after viewing a score.

## Gates and limits

The encoder bounds/unseen-value test must pass first. The first shadow must
improve primary by at least 0.001, lose no more than 0.0005 forward, and avoid
an unexplained slice regression larger than 0.001. If it passes, repeat
unchanged on middle and late; require two of three windows before official
validation. Stop at the family gate, official epsilon `0.002` / `N=3`
convergence, 50 attempts, or six hours.

No public-test label evaluation, hidden-test access, submission, upload, push,
contact, credential use, registration change, or visibility change. Protected
KuaiRand-1K score `0.6537467530366082` remains immutable.
