# Run 42 protocol: full-density repeat-affinity latent capacity

Started: **2026-08-30 21:08 SGT**.

## Independent question

Does doubling only the sparse factorization-machine latent rank from 8 to 16
let the full-density repeat-affinity model use its 136-million-row early-shadow
training set better, without harming forward transfer or any fixed robustness
slice?

## Why this is not a repeat of Run 27

Run 27 tested rank 16 on Run 24's much smaller residue-0-modulo-32 training
sample and pre-repeat `history_item` representation. It improved early primary
by only `+0.000217721`, below that run's fixed `+0.001` gate. Since then,
training density increased 32-fold and four causal user-author/user-video
repeat-affinity fields produced a confirmed three-seed gain. The interaction
capacity question has therefore changed materially.

## Frozen change

- Parent: exact Run 38 `history_item_repeat` early-shadow configuration and
  its fixed Run 34 full-training cache, evaluator, seed, BCE objective,
  optimizer, learning rate `0.001`, 20-epoch cap, patience 4, batching, and
  robustness definitions.
- Change only `--rank 8` to `--rank 16`. Do not sweep rank 12, 24, 32, learning
  rate, regularization, optimizer, or seed after seeing the first score.
- Later rejected creator-behavior and recency code is dormant for the selected
  `history_item_repeat` path. A source diff against protected commit `21af016`
  confirmed that this active encoder/model path is unchanged.
- First score: `shadow_early`, seed 2027, compared with
  `run38-001-repeat-affinity-shadow-early`.

## Gates and limits

1. Continue only if early validation primary gains `>= +0.0005`, forward is
   `>= -0.0005`, and every fixed activity/date slice is `>= -0.001` versus
   the exact repeat-affinity parent.
2. A pass repeats rank 16 unchanged on middle and late shadows; at least two
   of three shadows must pass without a material transfer failure.
3. Only then open official-development seeds 2027-2029. Promotion requires a
   paired mean gain `>= +0.0005`, no seed delta below `-0.0005`, and primary
   score span `<= 0.002`.
4. Stop this bounded run at family failure, declared convergence, 50 counted
   attempts, or six hours. Closing Run 42 does not stop the 72-hour campaign.

The protected seed-2029 score `0.6492243384881571` and its artifacts remain
untouched. All metrics are deterministic development-sample evidence, not the
full benchmark, hidden test, leaderboard, or submission. Public-test labels
and external actions remain locked.
