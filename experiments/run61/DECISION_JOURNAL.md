# Run 61 decision journal

## 2026-08-31 08:27 SGT — capacity-group consensus frozen

- Give rank 16 and rank 32 one equal group vote each.
- Use only the exact pre-hashed source archives in the protocol.
- Begin with early only. Preserve Run52.

## 2026-08-31 08:28 SGT — aggregate gain, high-activity guard fails

- Attempt 1 completed successfully in `6.087807` seconds with
  `3,333,341,184`-byte peak RSS.
- Validation primary improved `+0.0003645742050721`, GAUC
  `+0.0001391450849392`, nDCG@5 `+0.0005900033252050`, and forward primary
  `+0.0003768823102682` versus exact Run52.
- Cold/low improved `+0.0005202436494594`, medium improved
  `+0.0008203908215714`, early dates improved `+0.0000111016652409`, and late
  dates improved `+0.0000394274233159`; high activity regressed
  `-0.0013542772549110`, crossing the frozen `-0.001` floor.
- The ignored 4,446,671-byte prediction SHA-256 is
  `c621cddf7c46af11e5bc1f3841a018c15167d4a0dd9a56d878bd44bf281980e4`.
- Stop Run61 at its gate. No middle, late, official, weight, subset, or route
  is added inside this run.
