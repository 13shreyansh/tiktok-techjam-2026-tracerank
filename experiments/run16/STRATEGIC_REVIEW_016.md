# Run 16 fresh-context review — attempt 16

## Is current work still on the winning path?

Yes, because the two most obvious workshop-derived hypotheses were tested with
strong leakage controls and stopped immediately when they failed. The current
1K candidate remains the materially stronger content seed at `0.653746753`;
neither a fragile validation bump nor a narrative preference displaced it.

## Full failure audit

- Causal user/tag history did not survive its forward window.
- Same-impression pairwise training produced only noise-sized movement and
  traded nDCG for GAUC on validation.
- Reparameterizing either failed family would now be local validation tuning.
- The task requires per-item prediction at the ranking stage; the workshop
  explicitly says list-level re-ranking is outside this challenge. The current
  experiments respect that boundary while evaluating user-grouped order.
- The largest remaining 1K-specific official signal is the item-statistics
  table, but it is dangerous: any statistic computed after an impression or
  over the full collection period could leak future outcomes.

## Next action

Audit the official statistic table's schema, date semantics, and missingness
without training. Proceed only if features can be joined using information
strictly earlier than the scored date and built without reading post-April-28
outcomes. If that contract cannot be proven, skip the family. Preserve the
current content checkpoint and Pure fallback unchanged.
