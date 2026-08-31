# Run 45 report: causal user-topic affinity below gate

## Decision

Run 45 closed after one successful, frozen early-shadow attempt. It added two
strictly causal fields to the repeat-affinity FM: the user's prior exposure
count and beta-smoothed long-view rate for the current primary tag.

| Measure | Repeat parent | Topic affinity | Change |
|---|---:|---:|---:|
| Early primary | 0.632885873 | 0.633231060 | +0.000345186 |
| Early GAUC | 0.701268679 | 0.701053660 | -0.000215020 |
| Early nDCG@5 | 0.564503067 | 0.565408460 | +0.000905392 |
| Forward primary | 0.634753164 | 0.635135101 | +0.000381937 |
| High activity | 0.556729141 | 0.558385333 | +0.001656192 |

Both aggregate movements were positive, and every fixed slice remained inside
the guard. The late-date slice changed only `-0.000042402`. However, both
aggregate gains were below the predeclared `+0.0005` materiality gate, so no
middle, late, official, seed, bucket, secondary-tag, or capacity variation was
attempted. The protected Run 43 ensemble remains `0.6501881386335703`.

## Causality and accounting

The early archive covers all 207,446,146 cache rows, is 829,784,712 bytes, and
has SHA-256
`9e16654f699d1e27e8ee5e39095f89fdf9d08292812d608c83cdd4a513b62e68`.
Its build completed in 1,215.340 seconds with 6,021,070,848-byte peak RSS.
Same-timestamp rows share their prior state, outcomes after April 11 are masked
from updates, and scoring state is frozen.

One counted model attempt completed in 593.445 seconds with peak subprocess RSS
15,711,371,264 bytes. Its ignored checkpoint SHA-256 is
`075b148f37def21804dc9a0ed463c098eb80b63227b697ff0a01d7dc2e262f4c`;
its ignored prediction SHA-256 is
`9028fb0b68252ddbb86592a32a02e92f76e7a9ba2b97852bfcc4d96be5fa6d48`.

These are deterministic development-sample metrics, not a full KuaiRand-27K
benchmark, hidden-test, submission, or leaderboard result. No public-test or
hidden labels, upload, submission, push, organizer contact, registration
change, or public release occurred. Closing Run 45 does not stop the overall
72-hour campaign.
