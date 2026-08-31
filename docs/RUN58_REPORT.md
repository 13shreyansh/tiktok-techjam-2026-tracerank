# Run 58 report: additive recent-sequence tail rejected

Run58 tested the only architecture correction unlocked by Run57. The exact
protected 24-field rank-32 FM interaction path was retained, while all eleven
verified recent-sequence fields were restricted to sparse additive weights.
Forty targeted tests passed before the run opened.

The single attempt completed successfully, but early primary was
`0.6316654090484246`, a `-0.0034999299842905` regression versus exact Run52.
GAUC regressed `-0.0029737837727527`, nDCG@5 regressed
`-0.0040260761958284`, and forward primary regressed
`-0.0011815746015321`. Every fixed slice also regressed: cold/low
`-0.0035704596217806`, medium `-0.0035895747252990`, high
`-0.0028887693988795`, early dates `-0.0007289192442849`, and late dates
`-0.0027939835610252`.

The counted subprocess took `623.637632` seconds and peaked at
`31,456,198,656` bytes RSS. The ignored 3,787,021,709-byte checkpoint SHA-256
is `8fec6ff4e5298c0e1991cdb2318ded4f2829f7c1ef10b7420e41c23c8d20357e`;
the ignored 6,619,983-byte prediction SHA-256 is
`bba5ac50a354dd4cf32d01417948a8bf627231b7bd24663ad7ab204aa81b936e`.

The result rules out recent categorical sequence fields in both dense FM
interaction and additive-tail forms under this representation. No middle or
late sequence archive, subset search, tail-weight tuning, ensemble, official
seed, hidden test, submission, or external action followed. Run52 remains
protected at local primary `0.6534977984044839`. These scores are fixed 1/32
development-sample results, not the full benchmark, hidden test, submission,
or leaderboard. The 72-hour optimization campaign continues in a new bounded
run.
