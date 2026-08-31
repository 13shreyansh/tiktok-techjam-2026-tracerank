# Strategic audit: Run88 majority pairwise rank consensus

## Fresh-context diagnosis

The clean six-causal Run84 candidate remains the only eligible Pure artifact at
primary `0.605374519999571`. Run85 and Run86 added behavioral channels but
missed materiality; Run87's strong meta-window residual correction reversed on
both independent future windows. Further tuning those families would optimize
observed dates rather than address a stable error.

The selected ensemble currently averages each member's within-user percentile
rank. That is a positional Borda-style consensus: a sufficiently extreme
outlier member can move the mean even when most members agree on every relevant
pair. Run14 showed that taking the median position is not better, but it did not
test majority pairwise preference.

## Frozen independent hypothesis

For each user and each pair of candidate videos, count which candidate is
ranked higher by more independent members. Give a candidate one point per
majority win and half a point per tied vote; use mean member rank only as a
negligible deterministic tie-breaker. This Copeland-style rule uses the whole
candidate list, has no fitted parameter, threshold, member weight, or label-
derived calibration, and is insensitive to the magnitude of one dissenting
member's position.

## Third-person winning-goal check

This is worth one bounded family because it directly tests list-level consensus
using already frozen, diverse predictions and costs almost no training compute.
It is not worth adaptive aggregation search. Require chronological validation
and forward transfer in at least two of three predeclared windows before one
official-validation application. If two windows fail, or any hard component or
slice floor fails, close immediately. Run84 remains untouched; official final-
test outcomes remain unavailable to evaluation.
