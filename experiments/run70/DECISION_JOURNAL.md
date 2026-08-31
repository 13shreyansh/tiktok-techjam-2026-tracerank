# Run 70 decision journal

## 2026-08-31 09:36 SGT — recurring time context frozen

- Revisit only the exact hour-plus-weekday pair that previously improved all
  chronological shadow blends but failed official promotion.
- The current 27K rank-32 repeat-affinity parent is materially different; do
  not reuse the old score as evidence of a current gain.
- Begin with seed-2027 early only. Preserve Run52.
- All 67 tests and bytecode compilation passed before opening the run.

## 2026-08-31 10:49 SGT — first launch interrupted before a result

- The first frozen launch was interrupted by a turn/user interruption after
  approximately six minutes of observed wall time. The detached session handle
  disappeared before a terminal resource receipt could be recovered.
- No ranker process remained when checked with the host process list. No model,
  prediction, experiment result, ledger row, or iteration increment exists.
- This is disclosed as an interrupted, unscored launch rather than a completed
  experiment. Restart the exact frozen attempt unchanged; do not use the
  interruption to alter the hypothesis, configuration, gate, or parent.

## 2026-08-31 11:05 SGT — recurring time context gate fails

- Attempt 1 completed successfully in `874.084590` seconds with
  `27,723,776,000`-byte peak RSS.
- Validation primary regressed `-0.0001767074512381006`, GAUC regressed
  `-0.00027586647815647236`, and nDCG@5 regressed
  `-0.00007754842431983988` versus exact Run52.
- Forward primary improved `+0.00036272161371619926`, but forward GAUC
  regressed `-0.00016697906000517904`.
- Fixed-slice primary deltas were cold/low `-0.0003417592563320637`, medium
  `+0.0009003861241702049`, high `-0.0019364014300199406`, early dates
  `+0.0004874349505157305`, and late dates `-0.00075877785841727`.
- The ignored 3,786,956,725-byte checkpoint SHA-256 is
  `126f683f8ba82810ff60033953c4b7a34f50499a39ac8ce94e090ba2816cf449`;
  the ignored 6,617,418-byte prediction SHA-256 is
  `95da5fb49a9be61b19b2208b86252cb0387a2f902d1c4b941e4f257be16c05e5`.
- Stop the recurring time-context family: it misses the validation gain gate
  and exceeds the high-activity regression limit. Do not test alternate bins,
  timezones, raw dates, later windows, official seeds, or blends.

## 2026-08-31 11:40 SGT — retrospective parent-drift correction

- Run72 proved that Run70 inherited rejected Run60 neutral unknown-row
  initialization and therefore did not isolate time context on exact Run52.
- Versus Run60, Run70 gained `+0.00020590151731225692` validation and
  `+0.0006832696785779024` forward, while high activity still changed
  `-0.0013046239845939667`.
- Keep Run70 historically closed and unpromoted. Permit one fresh exact-Run52
  compatibility retest; this is defect correction, not a time-feature sweep.
