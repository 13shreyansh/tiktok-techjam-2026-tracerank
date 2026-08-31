# Strategic audit — 2026-08-31 08:37 SGT

Run61 retained strong forward diversity but over-shifted high-activity users.
Run63's exact fallback repaired that cohort but narrowly lost the forward gate.
Run64's global shrinkage diluted forward diversity even more. The remaining
principled interpolation is localized midpoint shrinkage: preserve Run61 for
ordinary users and blend Run61 equally with Run52 only for high activity.

Run65 freezes that midpoint before scoring. This is not a threshold or weight
sweep: the cohort is the existing training-activity upper tertile and `0.5` is
the single symmetric midpoint between the observed useful base and protected
fallback. No other blend, cutoff, route, member, or aggregation may follow
inside the run.

The implementation is separately committed, source SHA-256 is
`aa17b2c2cabcd1659dc5a4c14002bff69dedef8d65f7bc49202d4e1b37deec40`,
and all 60 tests pass. Run52 remains protected.
