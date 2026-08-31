# Run90 protocol: dual-timescale positive history

Declared: **2026-08-31 18:40 SGT**, before any Run90 model score.

## Frozen architecture

Parent: Run83 causal `sequence_nn`, seed 2027, `shadow_early`; validation
primary `0.6169077754020691`, forward primary `0.6040810346603394`.

Retain the exact parent fields, causal 20-event positive long-view video/tag
history, dot attention, embedding 16, hidden 128, dropout 0.2, neural-FM term,
batch 4096, AdamW `0.0005`, weight decay `0.00001`, early stopping and seed.
Add exactly one path:

- reuse the same embedded history and candidate-attention logits;
- independently normalize attention over the five most recent history slots;
- append recent profile, candidate × recent profile, and absolute difference;
- retain the original 20-event profile and interactions unchanged.

No recent length, coefficient, gate, projection, normalization, label, action,
loss, optimizer, capacity, seed, or blend is searched.

## Gates

1. Targeted recent-mask/empty-history tests, full suite, compilation and CLI
   discovery must pass; commit exact code and protocol before scoring.
2. Run paired seed 2027 on `shadow_early`. Continue only if validation primary
   improves at least `+0.0005`, forward primary does not decline, neither
   component declines by more than `0.0005`, and no activity/date slice declines
   by more than `0.001`.
3. Only if step 2 passes, run seeds 2026 and 2028, require at least two positive
   paired gains and a three-seed consensus gain of `+0.0003` on validation and
   forward with the same floors.
4. Only then require two-of-three chronological windows before a clean official
   six-member build. Official promotion requires at least `+0.0003` over Run84,
   no component decline, no slice loss beyond `0.001`, and label-blind alignment.

Stop at a failed gate, convergence, 50 attempts, six hours, or any label /
alignment failure. Official final-test outcomes must not be loaded, evaluated,
summarized, or used for selection. No submission, upload, push, public release,
organizer contact, registration change, or visibility change is authorized.
