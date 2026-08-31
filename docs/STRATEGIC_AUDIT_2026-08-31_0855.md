# Strategic audit — 2026-08-31 08:55 SGT

Run66 decisively rejected strict interaction masking, so all-pairs FM remains
the protected architecture. The next independent question is whether the
pointwise loss underweights the less common positive outcome. The full cache's
development long-view rate is `0.2622618981`; unweighted BCE still gives every
row equal loss contribution even though the judged metrics depend on ordering
positives above negatives within each user.

Run67 uses standard class-balanced BCE: the positive loss multiplier is derived
once from the training split as `negative_rows / positive_rows`. There is no
hand-selected coefficient, focal exponent, clipping rule, user weighting, or
auxiliary label. Inference, model, data, and evaluator remain exact Run52.

The implementation is separately committed, source SHA-256 is
`cbe53f97359126b602c5b87575b3811527b50cb644cb99639904cc0a792ffac1`,
and all 62 tests pass. Run52 remains protected.
