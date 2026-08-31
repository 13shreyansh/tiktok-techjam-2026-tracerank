# Strategic audit — 2026-08-31 12:13 SGT

## Evidence after Run74

Stable chronological minibatches regressed validation, forward time, both
component metrics, and every fixed slice by roughly `0.0022`–`0.0039` versus
exact Run52. The result closes global row-order changes. Along with the recent
negative capacity, time, objective, interaction-mask, and post-pass-refinement
tests, it argues against another optimizer or FM hyperparameter change.

## Largest remaining representation gap

Run52 contains raw user/video/author identities, causal aggregate user and item
history, and exact user-video/user-author repeat affinity. It can learn that a
user repeats the same entity, but it has no explicit candidate-aware signal for
a *different* video that resembles videos the user previously watched. The
earlier sequence and topic runs used raw tags or coarse tag counts; they did not
test collaborative similarity in the protected model's learned video space.

Run75 will use the already-fitted Run52 video latent vectors as a frozen
collaborative representation. For each user, it will average unit-normalized
video vectors from that split's long-view-positive training rows, with one vote
per observed positive exposure, then normalize the resulting user profile. A
candidate's profile score is cosine similarity between its frozen video vector
and that training-only profile. No validation outcome enters the profile.

To avoid inventing a score scale or mishandling videos unseen in training, the
profile does not globally replace the parent rank. Within each user, only
candidates with learned video identities are reordered by cosine similarity,
using exactly the percentile-rank slots those candidates occupied under the
parent. Unsupported candidates retain their parent slots. The final score is
one equal vote from the parent ranks and one from this slot-preserving profile
vote. There is no blend coefficient, history-length choice, decay, negative
sampling, extra training, or nearest-neighbour cutoff.

## Gates and third-person check

Start with exact Run52 seed-2027 early checkpoint and stored predictions.
Require validation and forward primary each `>= +0.00025`, both component
deltas `>= -0.0005`, every fixed slice `>= -0.001`, deterministic repeat, and
peak RSS below 60 GB. A pass repeats unchanged on middle and late and then on
the three exact official seeds before one fixed three-seed equal-rank
consensus. A first-gate failure closes video-profile similarity without cosine,
weight, author, positive-definition, or routing variants.

An independent reviewer should prefer this test over another local FM tweak:
it introduces a materially new recommender mechanism, uses only training
labels and a frozen parent representation, protects unseen candidates, and is
fully falsifiable. The deterministic 1/32 score remains local selection
evidence, never a hidden/full-benchmark or leaderboard claim.
