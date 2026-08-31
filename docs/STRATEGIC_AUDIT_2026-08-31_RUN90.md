# Strategic audit: Run90 dual-timescale positive history

## Fresh-context diagnosis

Run89 showed that wholesale normalization-heavy sequence encoding destroys the
selected representation. The successful parent instead learns a
candidate-conditioned profile over the last 20 positive long-view events. A
fixed attention-decay heuristic and a GRU failed earlier, but the campaign has
not explicitly preserved the full profile while adding a separate recent
profile.

## Frozen hypothesis

Keep the exact 20-event parent profile. From the same already causal positive
history and the same attention logits, independently normalize attention over
only the five most recent slots. Concatenate that recent profile, candidate ×
recent-profile interaction, and absolute difference alongside the unchanged
long profile. Five is frozen before scoring; it matches the compact recent
history used elsewhere in the repository and is not searched.

This adds no label, action, loss, target statistic, timestamp feature, sequence
encoder, or final-test access. It gives the downstream MLP an explicit choice
between stable interests and immediate positive interests without forcing a
recency coefficient.

## Third-person winning-goal check

This is lower risk than Run89 because the selected long-history path remains
verbatim and the recent path is additive. It is still a new representation and
must earn compute. Begin with paired seed 2027 on the early chronological
window. Require `+0.0005` validation and nonnegative forward transfer. A miss
closes the family without changing the recent length, dimensions, weights,
loss, seed, or blending. Run84 remains protected.
