# Strategic audit — 2026-08-31 08:42 SGT

Runs 61–65 found modest capacity-diversity signal but no configuration passed
both chronological and slice gates. That prediction-mixing family is closed.
The next independent lever is the structure of FM interactions, not their rank.

The protected FM forms every pair among 24 fields, including history–history
and candidate–candidate pairs. Run66 instead applies the recommender structure
described in the workshop: model how the person and their history match the
candidate video. User/context fields `(user, tab, user histories, user-entity
repeat histories)` form one side; candidate fields `(video, author, duration,
tag, upload/video type, item histories)` form the other. Only cross-side latent
dot products remain, while all 24 fields keep trainable linear effects.

The groups cover every field exactly once and are frozen before scoring. No
alternate grouping, within-side residual, rank, optimizer, feature, or loss
variation is allowed. The implementation is separately committed, source
SHA-256 is
`4be1d0c1be3ba6ca4cede2a3fffcb5f2c9ee781acef45f2a95e834a7160a3bec`,
and all 61 tests pass. Run52 remains protected.
