# Run 28 report: KuaiRand-27K cross-capacity rank consensus

Run 28 rejected a fixed equal within-user rank blend of the protected rank-8
model and an unchanged rank-16 model. The blend passed the early chronological
window, but middle and late failed the predeclared validation, forward, or
slice gates; no official score or blend-weight search followed.

| Window | Validation change | Forward change | Decision |
|---|---:|---:|---|
| Early | +0.000513685 | +0.000677662 | Pass |
| Middle | +0.000096446 | -0.000141666 | Fail |
| Late | +0.000340783 | +0.000265401 | Fail |

The late blend improved high-activity primary by `0.001852990`, but regressed
medium activity by `0.000413005`; selecting that subgroup result would violate
the fixed robustness rule. Five counted executions—two support models and
three blend evaluations—used 151.323 subprocess seconds. Peak subprocess RSS
was 3,752,869,888 bytes.

The first ledger receipt contains a disclosed negative campaign age because
the initial state time was mistakenly set 79.677 seconds after the actual
command start. The append-only receipt is preserved and the state/protocol were
corrected to the observed `2026-08-29T23:49:40.323426+08:00` start. No public-
test or hidden labels, upload, submission, or release occurred. Run 24's
`0.630624629` 27K development-sample checkpoint remains protected.
