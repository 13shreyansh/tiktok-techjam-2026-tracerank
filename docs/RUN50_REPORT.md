# Run 50 report: pure rank-16 seed consensus rejected at official gate

## Decision

Run 50 tested one frozen hypothesis: equal within-user percentile-rank
aggregation of rank-16 repeat-affinity seeds 2027, 2028, and 2029. The same
model, features, seed set, equal weights, member order, and gates were fixed
before training. No subset, weighting, normalization, feature, or parameter
search occurred.

| Window | Seed-2027 primary | Consensus primary | Change | Forward change |
|---|---:|---:|---:|---:|
| Early | 0.633297062 | 0.634420280 | +0.001123218 | +0.001663388 |
| Middle | 0.644492597 | 0.646045954 | +0.001553357 | +0.000611963 |
| Late | 0.641995759 | 0.643335634 | +0.001339875 | +0.000895370 |

Every fixed validation, forward, activity, and date slice improved in all
three chronological windows. The official seed-stability prerequisite then
failed: seed 2028 scored `0.6505381497088332` (`-0.0003942855924383` versus
seed 2027) and passed, but seed 2029 scored `0.6501438334379509`
(`-0.0007886018633205`) and failed the `-0.0005` floor. Seed 2029 also missed
the slice floor for cold/low activity (`-0.0015195199439885`) and late dates
(`-0.0010147527030016`). Therefore the preregistered official consensus was
not scored and Run 50 was not promoted. Run49 remains protected at
`0.6509565751074728`.

## Artifacts and accounting

The ignored official seed-2028 model and prediction SHA-256 values are
`1922fc19689333179debe94d92a8438b2e8467d2cdf813f129b4b9fc0a0be81c` and
`b1e11232f1646d92a74692805c070e2136290906d27d852204bd2ebf91ce86f4`.
The seed-2029 values are
`a2ddd01a3e9cda0e62e4ff6aa8b79a8bb7b9dd07a0c45e0fb4605e838a10ee23` and
`42f5f5bd8f793c9d0d04d03b520283629e674126ce5864c4130c93d5af3af364`.
All shadow artifact hashes are preserved in the decision journal.

Eleven counted attempts completed with return code zero in
`7814.537985` subprocess seconds. Peak subprocess RSS was
`28,542,648,320` bytes. Run 50 began at 01:50 SGT and reached its terminal
gate at about 04:09 SGT, below both 50 attempts and six elapsed hours. The
required attempt-8 fresh strategic review was completed before attempt 9.

## Validity boundary

These scores use full eligible training rows and a fixed deterministic 1/32
development evaluation sample. They are not the full KuaiRand-27K benchmark,
organizer hidden test, submission, or leaderboard. No public-test or hidden
labels, upload, submission, push, organizer contact, registration change, or
public release occurred. Closing Run 50 is a run checkpoint, not the end of
the 72-hour optimization campaign.
