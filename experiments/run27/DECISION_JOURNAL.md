# Run 27 decision journal

## 2026-08-29 23:47 SGT — capacity family opened after fresh audit

- Run 24 established that causal user plus item history is the strongest 27K
  sampled representation. Runs 25 and 26 rejected added behavior rates and
  short-window trend fields, so no further temporal-field tuning is warranted.
- Rank 8 was never compared with rank 16 on the winning representation. The
  first Run 27 candidate changes only this interaction bottleneck and retains
  the exact chronological and robustness gates.
- The Run 24 seed-2029 development-sample score `0.630624629` remains protected.
  The required Pure candidate and 1K candidate also remain untouched.

## 2026-08-29 23:49 SGT — rank 16 was stable but below the materiality gate

- Attempt `001-history-item-rank16-shadow-early` completed in 51.363 seconds
  with peak RSS 3,205,283,840 bytes and selected epoch 6.
- Validation moved from `0.614459200` to `0.614676921` (`+0.000217721`), below
  the fixed `+0.001` requirement. Forward moved `+0.000837268`.
- Slice changes were cold/low `+0.000019029`, medium `+0.000072460`, high
  `+0.000987446`, early dates `+0.001599440`, and late dates `+0.000468069`.
- The result is stable but too small relative to observed seed variation. Close
  the capacity family without ranks 12/24/32, optimizer changes, or seed search.
