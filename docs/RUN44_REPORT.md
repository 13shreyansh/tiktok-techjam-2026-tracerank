# Run 44 report: raw-logit consensus rejected

## Decision

Run 44 closed after two successful chronological shadow evaluations. It
replaced Run 43's within-user rank averaging with one fixed equal arithmetic
mean of the same three raw FM logits. No member, weight, calibration, clipping,
or transform search occurred.

| Window | Validation change | Forward change | Full `+0.0002` win? |
|---|---:|---:|---:|
| Early | +0.000238626 | -0.000048677 | No |
| Middle | +0.000121091 | +0.000148521 | No |

Every early and middle activity/date slice stayed inside the frozen guards;
the middle slices all improved. Nevertheless, after zero full wins on two
windows, the required two-of-three shadow gate was mathematically impossible.
The run stopped before the late archive and before official development. No
alternative raw/logit/rank aggregation was tried. Run 43's protected
`0.6501881386335703` rank-consensus candidate remains unchanged.

## Accounting and validity boundary

Two counted attempts completed successfully in 13.317 subprocess seconds with
peak subprocess RSS 3,838,738,432 bytes. The implementation added one explicit
`raw_mean` mode and two unit tests; fourteen targeted tests passed before
scoring. Public-test and hidden labels remained locked. No upload, submission,
push, organizer contact, registration change, or public release occurred.

These are deterministic chronological development-sample comparisons, not a
full KuaiRand-27K benchmark, hidden-test, submission, or leaderboard result.
Closing this aggregation family does not stop the 72-hour campaign.
