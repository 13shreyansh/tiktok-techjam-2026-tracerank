# Strategic review 013 — official non-promotion

## Outcome

The fixed equal-rank blend improved validation and forward scores across early,
middle, and late chronological windows, with no robustness-slice regression.
Nevertheless, the three-seed official nine-member ensemble scored 0.605206580,
below the protected six-member fallback at 0.605400885.

## Long-horizon interpretation

This is a useful negative result. Hour and weekday create complementary signal
inside the training-period shadow windows, but that signal does not improve the
already diversified official ensemble. Possible explanations include changing
calendar/traffic composition, redundancy with seed diversity, and the fact that
the fallback includes both legacy and strictly causal history constructions.

Searching temporal weights after observing the official result would convert a
replication failure into validation tuning. The magnitude is also smaller than
the observed neural-run variance. The autoresearch keep/discard rule therefore
requires discarding the candidate, even though its internal story is attractive.

## Decision

Retain the exact 0.605400885 fallback and stop Run 8 after 13 attempts. Preserve
the temporal models and score arrays as ignored evidence, not as the final
candidate. Return to independent hypothesis generation; do not tune ensemble
weights, time bins, or seeds on official validation.
