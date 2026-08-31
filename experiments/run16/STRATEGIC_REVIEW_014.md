# Run 16 fresh-context review — attempt 14

## Is the gain real enough to keep?

Yes. The content FM improved the base 1K ensemble from `0.644227425` to a
best-seed primary of `0.653746753` (`+0.009519328`). The same fixed fields
improved validation and forward evaluation in all three chronological shadow
windows, both official metrics, and every activity slice. All three official
seeds selected the same epoch and scored between `0.649990205` and
`0.653746753`.

The fixed ensemble did not improve the best seed or its weakest activity slice,
so seed 2028—not the ensemble—is the promoted 1K candidate.

## Leakage and overfitting audit

- Primary tag, upload type, and video type come only from the official
  label-free item table and are available when candidates are scored.
- Values absent from each training window map to explicit unknown identities.
- Every field, seed, and ensemble rule was declared before its family result.
- Only April 8–28 development rows are cached. Later rows were discarded by
  date before `long_view` was accessed; public-test labels remain locked.
- No hidden or held-out test result was used to select this candidate.

## Long-horizon failure audit

- The published bonus weight and hidden delivery route remain unknown, so a
  1K gain may not dominate the protected Pure score in final judging.
- The validation population is logged exposure data, not a random catalogue
  sample. Offline gains can inherit the previous recommender's exposure bias.
- Seed 2028 wins mainly through nDCG@5; GAUC is stable across seeds. The top-five
  ordering is therefore the less certain part of the gain.
- High-activity users remain the weakest primary slice because their candidate
  lists are much longer and nDCG@5 is harder, even though their GAUC is strong.
- Content identity helps cold videos but does not yet represent the user's
  ordered viewing history, the central information advantage of KuaiRand-1K.

## Next action

Preserve and hash the content candidate before further research. The next
bounded family, if the run remains within its limits, should test strictly
causal history features built only from events earlier than each scored event.
It must pass all three shadow/forward windows before official validation. Do
not spend attempts on seed searches, ensemble weights, or micro-tuning.
