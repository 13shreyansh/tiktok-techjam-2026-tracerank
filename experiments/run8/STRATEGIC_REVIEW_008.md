# Strategic review 008 — multi-window evidence before final confirmation

## Evidence through attempt 8

- Early equal-rank ensemble: +0.001438329 validation, +0.000121698 forward,
  and all five slices improved.
- Middle equal-rank ensemble: +0.000585882 validation, +0.000459553 forward,
  and all five slices improved. This is positive but below the independent
  +0.001 magnitude gate.
- Late temporal member before blending: +0.000062764 validation and
  -0.000028968 forward versus its fresh parent, with mixed slice changes.
- The member's standalone effect changes across windows, confirming that it
  must never replace the stable parent by itself.

## Fresh-context risk audit

The early result may be larger because hour/weekday align especially well with
that split. The middle result shows smaller but directionally consistent blend
benefit. The late member provides no evidence for a strong standalone temporal
effect. Selecting a new blend weight now would use the confirmation windows as
tuning data and is prohibited by the protocol.

The fixed equal-rank blend remains worth evaluating on late predictions because
diversity can improve ordering even when a member is individually tied. This is
the ninth and final chronological confirmation attempt. Official-seed promotion
requires a nonnegative, forward-safe late result and an aggregate positive
pattern across all three windows; any material late regression stops the design.

## Decision

Run only the predeclared equal-weight within-user rank late ensemble. Do not
change features, weights, normalization, epochs, or seed. Keep public-test
labels locked.
