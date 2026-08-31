# Run 4 unbiased-validation protocol

Run tag: `run4-exposure-debias`
Branch: `codex/run4-exposure-debias`
Started: 2026-08-29 14:25 SGT

## Objective

Use the organizer-identified random-exposure log as an additional unbiased
validation set to find a model that generalizes beyond the production system's
selection bias. The standard public test remains locked, and the exact Run 2
0.605400885 candidate remains the fallback.

## Evidence boundary

- Train models only on the standard April 8-21 training split.
- Use standard April 22-28 labels and the separate random-exposure log only for
  validation and robustness selection.
- Do not train on random-log labels in this campaign. The starter explicitly
  describes that file as an additional unbiased validation set.
- Do not evaluate standard April 29-May 8 public-test labels.
- Preserve the organizer evaluator unchanged.

## Promotion gates

A family is eligible for replication only if it:

1. improves random-validation primary by at least 0.002 over its paired parent;
2. does not reduce standard-validation primary by more than 0.0005;
3. does not create a material low/high-activity or late-date regression; and
4. survives seeds 2026, 2027, and 2028 before joining an ensemble.

Small standard-validation gains without random-validation improvement are not
promotion evidence. A family with useful independent prediction diversity may
be retained only after a documented ensemble ablation.

## Limits and stopping

1. Count every launched attempt, including failures and timeouts, up to 50.
2. Stop no later than six hours after this run starts.
3. Stop after three completed families fail to improve random validation by
   more than 0.002, or another organizer convergence condition is reached.
4. Write a fresh strategic review after every family or eight attempts.
5. Keep a ten-minute timeout per attempt and record exact commands, outputs,
   hashes, return codes, elapsed time, and peak RSS.
6. Do not upload, submit, push, contact organizers, change registration, expose
   secrets, or alter repository visibility.
