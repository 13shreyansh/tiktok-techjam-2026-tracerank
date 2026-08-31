# Strategic audit: Run92 hard target-match history expert

## Fresh-context diagnosis

Run91 closes the remaining separate action-history question: its forward gain
did not survive validation and it harmed high-activity users. More broadly,
recent additive history channels repeatedly become fragile as histories grow.
The protected model uses candidate-conditioned softmax attention, but it still
averages all attended positive-history vectors into one profile. For users with
several interests, that average can dilute the one earlier item that best
matches the current candidate.

The untested question is therefore not another history source, length, loss, or
capacity. It is whether a parameter-free hard target match complements the
unchanged soft profile. This directly reflects the workshop clue that the
current candidate should be interpreted using what the user watched before.

## Frozen hypothesis

Keep the exact Run83 seed-2027 parent. Reuse its last-20 causal long-view video
and tag history and its candidate-to-history dot logits. In addition to the
unchanged soft attention profile, select the single valid history vector with
the highest dot logit. Append that vector, its elementwise candidate product,
and absolute difference to the MLP input. Empty histories contribute zeros.

There is no temperature, top-k, threshold, new event type, label, auxiliary
loss, or final-test statistic. The neural FM term remains unchanged and uses
the original soft profile only.

## Third-person winning-goal check

This is a genuinely different multi-interest mechanism and costs one bounded
opening attempt. It may help high-activity users, where an average profile is
most likely to blur interests, but hard selection can also amplify noise.
Require `+0.0005` validation primary, nonnegative forward primary, component
losses no worse than `-0.0005`, and every fixed slice no worse than `-0.001`.
A miss closes the family without top-k, temperature, seed, or blend rescue.
Run84 remains protected.
