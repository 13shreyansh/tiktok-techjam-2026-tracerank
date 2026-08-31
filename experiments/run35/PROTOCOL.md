# Run 35 protocol: full-density hard within-user ranking

## Hypothesis

Starting from each protected Run 34 full-density causal user-item FM checkpoint,
a conservative hard-negative within-user pairwise fine-tune can improve the
ordering metric without sacrificing the pointwise GAUC signal. The ranking
pairs use only training rows: up to five lowest-scored positives and five
highest-scored negatives per user under the frozen parent checkpoint.

## Frozen implementation and parameters

- Load the exact matched Run 34 checkpoint; do not repeat or alter pointwise
  BCE training.
- Require checkpoint feature set, model type, field dimensions, offsets, split,
  and seed to match the requested experiment before training.
- Build deterministic within-user hard pairs only from the declared training
  interval and its labels. Validation, forward, and public/hidden rows are
  forbidden during pair construction.
- Fine-tune with BPR/softplus pair loss for at most three epochs, sparse Adam,
  learning rate `0.00005`, batch size `32768`, and at most five pairs per user.
- Treat the loaded pointwise checkpoint as pairwise epoch 0. Retain only the
  best validation checkpoint, with patience 2 and a minimum `0.00001` primary
  improvement; otherwise restore the parent byte-equivalent weights.
- Keep Run 34 rank 8, `history_item` fields, cache, encoder, evaluation rows,
  evaluator, prediction batching, thread count, and seed fixed.

## Promotion and stopping gates

1. Run `shadow_early` first against the exact Run 34 parent. Continue only if
   validation improves at least `+0.0005`, forward is no worse than `-0.0005`,
   and no fixed slice is worse than `-0.001`.
2. If early passes, repeat unchanged on middle and late shadows. At least two
   of three windows must pass and none may show a material transfer failure.
3. Only then run official seeds 2027, 2028, and 2029. Promote only if paired
   mean gain is at least `+0.0005`, no seed regresses below `-0.0005`, and the
   score span is at most `0.002`.
4. Stop the family immediately on a failed first gate or after six successful
   scored attempts. Run 35 is additionally hard-limited to 50 attempts and six
   wall-clock hours by the existing campaign wrapper.

All metrics remain deterministic development-sample evidence, not organizer
hidden-test, full-benchmark, submission, or leaderboard scores. No upload,
submission, push, organizer contact, or public release is authorized.
