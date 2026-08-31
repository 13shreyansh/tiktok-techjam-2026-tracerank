# Run87 decision journal

## 2026-08-31 18:09 SGT — family frozen

- Test a chronological cross-fit LambdaMART residual on top of the frozen
  causal rank ensemble, not a replacement representation.
- Train the residual model on 12–14 April predictions made by a parent trained
  only through 11 April; use 15–17 April only for early stopping.
- Require `+0.0005` on that meta window and then independently require
  `+0.0005` on 18–21 April, component/slice floors, and at most `-0.0002` on
  22–28 April. One failed transfer gate closes the family without tuning.
- Load no official final-test outcomes. Keep Run84 protected.

## 2026-08-31 18:12 SGT — implementation verification passed

- Ten targeted chronology, grouping, restoration, and archive tests passed;
  the full suite passed 100/100; Python compilation and `git diff --check`
  passed.
- A two-query synthetic LambdaMART fit completed successfully.
- The exact code, protocol, and strategic audit were committed as `b8d57f5`
  before the first counted execution.
- No model score was produced during implementation verification.

## 2026-08-31 18:18 SGT — independent transfer gate closes the family

- The only counted execution succeeded in `77.076746` seconds with peak RSS
  `6,446,383,104` bytes. It loaded no official-test outcomes and did not score
  public final-test labels.
- The meta window passed strongly: primary changed from `0.6048954350` to
  `0.6091704938`, or `+0.0042750588`.
- The independent target window reversed the gain: primary changed from
  `0.5928855989` to `0.5900456759`, or `-0.0028399230`. GAUC fell
  `-0.0038069995` and nDCG@5 fell `-0.0018728466`.
- The forward window fell `-0.0019162860`. Cold/low, medium, high, early-date,
  and late-date slices all regressed; medium activity was worst at
  `-0.0062311486`.
- This is not a marginal miss: the correction learned a time-specific error
  pattern that did not transfer. Close Run87 after one execution. Do not tune
  tree depth, learning rate, residual coefficient, feature subset, date
  boundary, or seed; do not apply it to the official candidate.
- Run84 remains protected at primary `0.605374519999571`.
