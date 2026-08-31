# Run 5 sampled-listwise protocol

Run tag: `run5-sampled-listwise`
Branch: `codex/run5-sampled-listwise`
Started: 2026-08-29 14:35 SGT

## Objective

Test the organizer's highest-ranked unexplored direction: align training with
the user-level ranking metrics. Replace the prior unbounded listwise pass with
bounded per-user positive/negative samples and mini-batches. Preserve Run 2's
exact 0.605400885 fallback and keep public-test labels locked.

## Evaluation and promotion

1. Re-establish the unchanged parent on the early shadow window after the data
   loader refactor.
2. Fine-tune the pointwise parent with at most five positives and twenty
   negatives per user per listwise epoch.
3. Promote only if paired primary gain is at least 0.001, forward loss is no
   worse than 0.0005, and no material activity/date segment regresses.
4. A promoted configuration must pass middle and late windows, then official
   seeds 2026, 2027, and 2028.
5. Use the organizer's unchanged GAUC/nDCG@5 evaluator; optimize no proxy metric
   in place of primary.

## Limits and stopping

- Count every launched attempt, failure, and timeout, up to 50.
- Stop within six hours and cap every subprocess at ten minutes.
- Stop after three completed ranking-loss configurations fail to improve the
  paired parent by more than 0.002.
- Write a fresh strategic review after every family or eight attempts.
- Do not upload, submit, push, contact organizers, use credentials, change
  registrations, or alter repository visibility.
