# Strategic audit — 2026-08-31 08:00 SGT

Runs 57 and 58 reject recent categorical sequence fields in both full FM
interactions and an additive-only tail. Repeating sequence subsets would now be
post-hoc search. The protected Run52 representation remains the right base.

Run53's rank-64 comparison changed two properties at once: interaction capacity
and initial interaction scale. For independent zero-mean latent components with
standard deviation `s`, an FM dot product has variance proportional to
`rank * s^4`. Reusing `s = 0.01` therefore doubled initial dot-product variance
when rank changed from 32 to 64. Preserving Run52's initial interaction variance
requires `s = 0.01 * (32 / 64)^(1/4) = 0.008408964152537145`.

Run59 tests exactly that correction with the otherwise unchanged Run53 rank-64
configuration. It is not a rank sweep: no other rank, initialization, optimizer,
learning rate, feature, objective, or rescue configuration is allowed. The
source was committed before scoring, SHA-256 is
`b353ab49d78199ec5c6b2b8032a6ce968a8920bb3a729178afeca97cddd49915`,
and all 58 tests pass. Run52 remains protected.
