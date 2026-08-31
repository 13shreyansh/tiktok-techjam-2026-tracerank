# Strategic audit — 2026-08-31 14:49 SGT

## Evidence after Run79

Chronological cross-fitting proved that Run76's tree learned genuine parent
error signal on a clean next day, but the correction missed protected
validation materiality, regressed forward primary, and harmed high-activity
users. Tree-based list correction is now closed in both equal-vote and
parent-aware residual forms. Recent tag/creator attention, collaborative cosine
profiles, extra FM fields, objectives, capacity beyond rank 32, and optimizer
changes have also failed frozen gates. Run52 remains protected.

## Remaining workshop-aligned mechanism

The workshop described industrial ranking models as large categorical
embedding tables followed by a shallow MLP. Run52 uses the same embeddings but
only a second-order FM head. KuaiRand-1K Run17 trained a DeepFM from scratch and
failed badly; that result confounded the nonlinear head with relearning every
sparse embedding. No 27K test has frozen the strong Run52 embedding geometry and
asked whether a small standard DeepFM tower adds higher-order interactions.

Run80 therefore loads exact Run52 seed-2027 `shadow_early`, freezes every sparse
latent and linear row, and trains only the existing standard 32/16 ReLU MLP over
the concatenated 24 × 32 field embeddings. Dropout remains 0.1 and learning rate
0.001, matching the repository's existing DeepFM defaults. The last layer starts
at exact zero, so epoch zero reproduces Run52 byte-for-byte and provides rollback.
No new feature, history, parent score, rank, width, dropout, optimizer, loss,
blend, or route is introduced or searched.

## Third-person goal check

This is a genuinely different representation test, not salvage of Runs76–79:
the residual can express higher-order interactions among the already-confirmed
causal fields while being unable to memorize new identity rows. The main risk
is that Run52 embeddings were optimized specifically for pairwise FM geometry,
or that a 32/16 tower is redundant. Start with one early attempt, require both
validation and forward transfer plus component and slice safety, and restore
the exact parent on failure. Scores remain fixed 1/32 local development
evidence, not hidden/full-benchmark or leaderboard results.
