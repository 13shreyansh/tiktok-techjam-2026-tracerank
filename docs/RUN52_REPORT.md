# Run 52 report: rank-32 consensus promoted

## Decision

Run 52 promoted the fixed equal within-user percentile-rank consensus of three
rank-32 repeat-affinity sparse-FM seeds. Rank 32 was frozen as the exact
doubling of the confirmed rank-16 architecture before the first score; model,
features, optimizer, seed order, windows, evaluator, and gates did not change.
No rank sweep, subset search, weight search, calibration, route search, or
post-hoc member selection occurred.

The early and middle chronological shadows improved both validation and
forward scores. The late shadow improved validation by `+0.0005381104313232`
and missed the matching rank-16 forward score by `-0.0002924166628117`, inside
the frozen `-0.0005` guard; every late fixed slice improved. This satisfied the
predeclared two-of-three shadow gate.

All three official rank-32 seeds improved over their matching rank-16 seeds:

| Seed | Rank-32 primary | Paired gain |
|---:|---:|---:|
| 2027 | 0.651738405 | +0.000805969 |
| 2028 | 0.651522086 | +0.000983937 |
| 2029 | 0.651469956 | +0.001326122 |

The seed span is `0.0002684491083153`. The frozen consensus reached GAUC
`0.7066506868398097`, nDCG@5 `0.6003449099691580`, and primary
`0.6534977984044839`. Versus protected Run49, this is `+0.0018695671245460`
GAUC, `+0.0032128794694759` nDCG@5, and `+0.0025412232970110` primary.
Official primary gains were cold/low `+0.0018444591766053`, medium
`+0.0041558441321636`, high `+0.0023557141149478`, early dates
`+0.0021444564027909`, and late dates `+0.0023425318802298`.

## Artifacts and accounting

The ignored consensus prediction archive is 6,725,014 bytes with SHA-256
`12e4652ef8b3636936b6bc310b500d3ad11714cfa25e3a0775c1c8e5e9696b96`.
The three member checkpoints and prediction archives are recorded with exact
hashes and sizes in the candidate manifest and immutable ledger.

Seven counted attempts completed successfully in `8566.915009` subprocess
seconds; peak subprocess RSS was `35,985,244,160` bytes. The observed first
command began at `2026-08-31T04:14:41.383105+08:00`; an initially declared
04:15 timestamp was corrected after the immutable first receipt exposed the
18.616895-second discrepancy. The final score arrived around 06:42 SGT, below
both the 50-attempt and six-hour limits. No failed subprocess or public-test
evaluation occurred.

## Validity boundary

This score uses full eligible training rows and a fixed deterministic 1/32
development evaluation sample. It is not the full KuaiRand-27K benchmark,
organizer hidden test, submission, or leaderboard. Promotion protects the best
local candidate; it neither estimates a hidden score nor ends the 72-hour
campaign. No upload, submission, push, organizer contact, registration change,
or public release occurred. Run49 remains available as a lower-memory fallback.
