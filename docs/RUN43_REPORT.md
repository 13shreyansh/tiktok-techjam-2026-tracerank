# Run 43 report: repeat-affinity three-seed consensus

## Decision

Run 43 promoted the fixed equal within-user percentile-rank ensemble of the
confirmed repeat-affinity models at seeds 2027, 2028, and 2029. The members,
equal weights, rank normalization, chronological windows, and gates were fixed
before the first ensemble score. No member subset, weight, seed, or score-scale
search occurred.

All three chronological shadows improved validation, their later forward
periods, and every fixed activity/date slice. Their validation/forward primary
gains over the exact seed-2027 parent were `+0.001002013/+0.001345341`
(early), `+0.001368092/+0.000768397` (middle), and
`+0.001208622/+0.001187162` (late).

On the locked official development sample, the ensemble reached GAUC
`0.7042855267502036`, nDCG@5 `0.5960907505169369`, and primary
`0.6501881386335703`. This is `+0.0009638001454132` over the protected
seed-2029 single checkpoint. Official slice gains were cold/low
`+0.0008163503167191`, medium `+0.0010694992027233`, high
`+0.0016495388836237`, early dates `+0.0011038099504457`, and late dates
`+0.0004830305679897`. Every frozen promotion guard passed.

## Artifact and accounting evidence

The ignored 6,727,185-byte ensemble prediction archive has SHA-256
`4b90b0fd6b435da0ae969cebd118f72880a61bad3e764645f63154176a6c7a6c`.
Its three member prediction hashes, in fixed order, are
`28750178342e69dca1b44eaddd5715a931ce9fed78bbfdca3cf4819fc5e8881b`,
`7ec69a8fb701948f0397aa4946f9d1c8c0b91e39a6d4704c56704795c0012327`,
and `831b805d5c0aa7dadef5c940e09a7b364c75dc3c68300d5804c892fc91d7aeeb`.
The prior seed-2029 single checkpoint remains preserved as a fallback.

Ten counted attempts completed in 5,928.835 subprocess seconds. Peak
subprocess RSS was 22,484,992,000 bytes. Run 43 started at 2026-08-30 21:26
SGT and closed after the official evaluation at 23:11 SGT, below both the
50-attempt and six-hour limits. No public-test labels, hidden labels, upload,
submission, push, organizer contact, or public release occurred.

Artifact byte/hash verification succeeded for the ensemble, all three member
prediction archives, and all three member checkpoints. A direct
`.venv/bin/python -m pytest ...` check could not start because `pytest` is not
installed in the isolated environment. The dependency-free fallback command
`.venv/bin/python -m unittest -v tests.test_kuairand_27k_sample_ranker
tests.test_run_27k_campaign_experiment` ran six tests successfully.

## Validity boundary

The score uses full eligible training rows and the fixed deterministic 1/32
development evaluation sample. It is not the full KuaiRand-27K benchmark,
organizer hidden test, submission, or leaderboard. Promotion protects this
local candidate; it does not estimate a hidden score or end the 72-hour
campaign. Run 44 begins from a fresh strategic audit rather than modifying the
closed Run 43 search.
