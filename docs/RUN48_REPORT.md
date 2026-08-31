# Run 48 report: multi-tag topic history below gate

## Decision

Run 48 closed after one successful frozen early-shadow model attempt. It kept
the repeat-affinity FM unchanged except for two causal fields describing the
candidate primary tag from all unique prior tag positions.

| Measure | Repeat parent | Multi-tag history | Change |
|---|---:|---:|---:|
| Early primary | 0.632885873 | 0.633212949 | +0.000327075 |
| Early GAUC | 0.701268679 | 0.700928883 | -0.000339796 |
| Early nDCG@5 | 0.564503067 | 0.565497014 | +0.000993947 |
| Forward primary | 0.634753164 | 0.635010962 | +0.000257798 |
| High activity | 0.556729141 | 0.558188019 | +0.001458879 |
| Late dates | 0.630940766 | 0.630685280 | -0.000255485 |

Both aggregate movements were positive but below the predeclared `+0.0005`
gate, GAUC declined, and the late-date slice was negative. No middle, late,
official, seed, bucket, current-tag, capacity, or ensemble variant was run.
The protected Run 43 consensus remains `0.6501881386335703`.

## Causality and accounting

The ignored early artifact has 207,446,146 rows, is 829,784,712 bytes, and has
SHA-256
`7809e65724a42a249480bbafac035334f1078ded58588d85a23728e048bcdadd`.
The builder emitted a complete manifest after 1,399.211 seconds and reported
7,748,534,272-byte peak RSS. Its outer timing wrapper returned 1 only because
the sandbox denied the wrapper's final clock-rate query; an independent
artifact verifier subsequently exited zero.

One counted model attempt exited zero in 523.473 seconds with peak subprocess
RSS 16,137,142,272 bytes. Its ignored model SHA-256 is
`609f3c7a5b52125ddab93d7666c62779c1b5499f1703381da127a94e6d7f2bc7`;
its ignored prediction SHA-256 is
`2db39eea87d939e6683e8b2945354650818d3961e673d845a752d051c69b6457`.

These are deterministic development-sample metrics, not a full KuaiRand-27K
benchmark, hidden-test, submission, or leaderboard result. No public-test or
hidden labels, upload, submission, push, organizer contact, registration
change, or public release occurred. Closing Run 48 does not stop the overall
72-hour campaign.
