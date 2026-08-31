# Run 47 report: high-activity topic route rejected

## Decision

Run 47 closed after two counted early-shadow executions. The first completed
with an implementation defect: it used the upper tertile across unique
training users (`52`) rather than the existing validation-row-weighted
robustness boundary (`106`). That result remains in the ledger but is excluded
from decisions. The defect was corrected, tested, committed, and the otherwise
unchanged route was rerun.

The corrected route used the four-member topic-diverse consensus only for
users above training-activity count 106 and the exact Run 43 consensus for all
others. It routed 284,656 validation rows from 2,686 users. Cold/low and medium
slice scores were prediction-identical to Run 43; high activity improved
`+0.0015700308002025`.

Despite that local benefit, aggregate validation gained only
`+0.0001789779986697` and forward changed `-0.0000502042058407`, failing the
frozen `+0.0003` gates. No threshold, quantile, soft route, middle/late build,
or official evaluation followed. Run 43 remains protected at
`0.6501881386335703`.

## Accounting and validity boundary

Both counted executions succeeded technically, totaling 14.737 subprocess
seconds; peak RSS was 3,462,070,272 bytes. Sixteen targeted tests passed after
the cutoff repair, including a regression test for row-weighted versus
unique-user quantiles. Public-test and hidden labels remained locked. No
upload, submission, push, organizer contact, registration change, or public
release occurred.

These are deterministic development-sample metrics, not a full KuaiRand-27K
benchmark, hidden-test, submission, or leaderboard result. Closing this route
does not stop the 72-hour campaign.
