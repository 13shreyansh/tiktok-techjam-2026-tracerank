# Run 75 protocol: frozen collaborative video-profile consensus

Started: **2026-08-31 12:14:00 SGT**.

## Independent question

Does a training-only user profile in the exact Run52 learned video space add
candidate-aware similarity signal to the protected repeat-affinity FM?

## Frozen construction

- Start with the exact Run52 checkpoint and stored prediction archive matched
  to each split and seed. Do not retrain or modify the parent.
- Use only rows inside that parent's training dates with `long_view == 1`.
- Unit-normalize every frozen learned video latent; average one vector per
  positive exposure for each user; unit-normalize the resulting user profile.
- Score a supported candidate by cosine similarity to that profile.
- Within each user, similarity may reorder only the parent percentile-rank
  slots occupied by candidates whose videos were learned in training and whose
  user has a positive profile. Every unsupported candidate keeps its exact
  parent slot.
- Final score is the equal mean of the parent rank vote and the slot-preserving
  profile vote. No coefficient, decay, cap, deduplication, negative event,
  author vector, tag vector, nearest-neighbour cutoff, or route.

## Gates and stopping

- Begin with exact Run52 seed-2027 `shadow_early` only.
- It must improve validation and forward primary each `>= +0.00025`, keep both
  GAUC and nDCG@5 deltas `>= -0.0005`, keep every fixed slice delta
  `>= -0.001`, reproduce its prediction archive bit-for-bit on one unchanged
  repeat, and peak below 60,000,000,000 bytes RSS.
- A pass repeats unchanged on `shadow_middle` and `shadow_late`; at least two
  of three windows must meet the same aggregate and safety gates.
- Only then evaluate exact official checkpoints for seeds 2027–2029. Require
  paired mean primary gain `>= +0.00025`, no seed below `-0.0005`, score span
  `<= 0.002`, and every fixed official slice `>= -0.001`.
- Only after seed stability, form one fixed equal within-user rank consensus of
  the three profile-enhanced seed predictions. Promote over Run52 only at
  primary `>= +0.0003`, both components `>= -0.0003`, and every slice
  `>= -0.0005`.
- Stop at the first failed gate, convergence, artifact/resource failure,
  50 attempts, or six hours. Closing Run75 does not stop the 72-hour campaign.

Source SHA-256 before scoring:
`c35143fd5a6c23d3596d7c676edee238fcb938b4be8cabe42d84faeada1307b8`.
All 75 tests, isolated-cache bytecode compilation, and `git diff --check`
passed. Scores remain deterministic 1/32 development-sample evidence, not the
full benchmark, hidden test, submission, or leaderboard. Public-test labels
and external actions remain locked.
