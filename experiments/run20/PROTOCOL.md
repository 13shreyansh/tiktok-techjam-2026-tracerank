# Run 20 protocol: KuaiRand-1K causal recent-interest sequence profile

Started: **2026-08-29 20:40 SGT**.

## Independent question

Can a strictly causal memory of a user's recent positive, strong-feedback, and
hated content categories improve ranking beyond the content FM, especially for
the repeated-interest pattern described in the organizer workshop?

This is not the rejected Run 16 aggregate-history table. It represents the
ordered last five long-view tags, the last strong-positive tag, the last hated
tag, explicit current-tag matches, and time since the last positive event.
Training rows see only earlier timestamps; same-timestamp rows are emitted
before outcomes update memory; validation and forward memory freezes at the
training cutoff.

## Fixed first candidate

- Exact Run 16 `content` fields plus the 11 predeclared sequence-profile fields.
- Sparse FM, chronological `shadow_early`, rank 16, seed 2027, learning rate
  0.001, batch 65,536, at most 20 epochs, patience 4.
- Paired parent: Run 16 attempt 8 content sparse FM.
- No parameter or field subset will be chosen from benchmark results.

## Gates and limits

Unit tests must prove simultaneous rows cannot see each other's outcomes and
scoring rows cannot update the frozen profile. The first shadow must improve
primary by at least 0.001, lose no more than 0.0005 forward, and avoid an
unexplained slice regression larger than 0.001. If it passes, repeat unchanged
on middle and late; require two of three windows before official validation.
Stop at the family gate, official epsilon `0.002` / `N=3` convergence, 50
attempts, or six hours.

No public-test label evaluation, hidden-test access, submission, upload, push,
contact, credential use, registration change, or visibility change. Protected
KuaiRand-1K score `0.6537467530366082` remains immutable.
