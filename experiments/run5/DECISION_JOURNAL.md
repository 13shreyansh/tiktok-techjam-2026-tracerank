# Run 5 decision journal

## 2026-08-29 14:35 SGT — campaign start

- Protected fallback: Run 2 six-seed within-user rank ensemble at 0.605400885.
- Public-test evaluations: zero.
- First action: reproduce the early-window parent under the current source,
  then test one bounded listwise configuration against it.

## 2026-08-29 14:42 SGT — first sampled listwise configuration rejected

- Fresh parent: validation 0.616920352, forward 0.603989244.
- Candidate's own pointwise checkpoint: 0.616809249.
- Listwise epoch 1: 0.616766393; epoch 2: 0.616428733.
- Final validation: 0.616809249 (**-0.000111103** versus paired parent).
- Forward validation: 0.604060888 (**+0.000071645** versus parent).
- Runtime was 239.94 seconds with 17,984,192,512 bytes maximum RSS. The bounded
  design solved the prior timeout but is expensive and did not improve ranking.
- Next configuration: one gentler listwise epoch at learning rate 1e-5 with
  three positives and twelve negatives per user. This tests overshoot with
  substantially fewer sampled rows; no broader tuning follows without a gain.

## 2026-08-29 14:46 SGT — gentle listwise configuration rejected

- Final validation: 0.616773009 (**-0.000147343** versus paired parent).
- Forward validation: 0.603764594 (**-0.000224650** versus parent).
- The listwise epoch moved its own pointwise checkpoint only +0.000014186,
  still far below the +0.001 gate. Runtime was 181.95 seconds.
- Decision: stop sampled softmax tuning. Lower learning rate and fewer samples
  did not reveal a useful effect.
- Final ranking-loss configuration: one hard-negative neural BPR epoch. Restrict
  each user's negative pool to its top-scored 20% so updates directly target
  false positives most likely to damage nDCG@5.

## 2026-08-29 14:48 SGT — hard-negative BPR and Run 5 stopped

- Candidate pointwise checkpoint: 0.616930127.
- Hard-negative BPR checkpoint: 0.616700888, so the ranking update was rejected
  by automatic best-checkpoint restoration.
- Final validation: 0.616930127 (**+0.000009775** versus paired parent).
- Forward validation: 0.603959978 (**-0.000029266** versus parent).
- Runtime was 37.78 seconds; maximum RSS was 3,926,278,144 bytes.
- Decision: reject. Random BPR had already failed in Run 1; top-20% hard
  negatives also move validation in the wrong direction.
- Run decision: three ranking-loss configurations failed the material-gain
  threshold. Stop Run 5 under its convergence rule. Next campaign: add missing
  time/context fields under the same multi-window gates.
