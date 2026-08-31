# Run 4 decision journal

## 2026-08-29 14:25 SGT — campaign start

- Protected fallback: exact Run 2 six-seed within-user rank ensemble,
  validation primary 0.605400885.
- Public-test evaluations: zero.
- First action: score the unchanged causal-history parent on the standard and
  random validation sets; no family will be judged before that paired control.

## 2026-08-29 14:27 SGT — paired parent established

- Standard validation primary: 0.604725242.
- Random validation primary: 0.388761997, versus five random-score diagnostics
  spanning 0.309854-0.311760 and an oracle of 0.837328.
- The model does learn real signal under random exposure, but much of its
  standard-traffic advantage does not transfer.
- Ledger attempt 1 records a negative campaign-elapsed-at-start because the
  initial state timestamp was accidentally seven minutes in the future. The
  immutable attempt start time and 49.13-second subprocess time are correct;
  the state timestamp was corrected to 14:25 before attempt 2.
- Next action: remove the explicit FM interaction term as a controlled test of
  whether raw ID crosses cause exposure overfitting. Promote only through a
  later blend if standard validation can remain within the safety gate.

## 2026-08-29 14:29 SGT — removing FM crosses rejected

- Standard validation primary: 0.604783297 versus 0.604725242 parent,
  **+0.000058055**.
- Random validation primary: 0.385598212 versus 0.388761997 parent,
  **-0.003163785**.
- Decision: reject and stop this exact family. The explicit FM term was not the
  source of the random-traffic weakness; removing it harmed both random GAUC
  and random nDCG@5.
- Next family: regularize user/video identity during training with controlled
  embedding dropout while retaining all inference-time information. This tests
  reliance rather than deleting a useful interaction mechanism.

## 2026-08-29 14:31 SGT — ID embedding dropout rejected

- Standard validation primary: 0.604929268 versus 0.604725242 parent,
  **+0.000204027**.
- Random validation primary: 0.387089133 versus 0.388761997 parent,
  **-0.001672864**.
- Decision: reject the family. Both deleting FM crosses and regularizing raw ID
  embeddings reduced unbiased-validation performance, so the evidence does not
  support an ID-overreliance diagnosis.
- Next family: use continuous watch-ratio auxiliary supervision. It supplies
  richer information than the binary long-view label and had only a tiny
  standard shadow cost in Run 2, making it a stronger unbiased-generalization
  hypothesis than further identity regularization.

## 2026-08-29 14:35 SGT — watch-ratio auxiliary stopped

- Standard validation primary: 0.605053663 versus 0.604725242 parent,
  **+0.000328422**.
- Random validation primary: 0.388188183 versus 0.388761997 parent,
  **-0.000573814**.
- Decision: reject. The candidate improved standard nDCG@5 but weakened both
  random GAUC and random nDCG@5, and took 185.61 seconds.
- Run decision: stop Run 4 after three failed families under its convergence
  rule. Preserve the Run 2 fallback. The next campaign will address the
  organizer's top stated headroom—ranking-aligned loss—with bounded sampled
  listwise batches rather than the prior unbounded implementation.
