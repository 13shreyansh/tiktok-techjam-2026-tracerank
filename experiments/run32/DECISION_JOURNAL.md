# Run 32 decision journal

## 2026-08-30 01:03 SGT — quarter-density family opened

- Run 30's fourfold density increase produced a stable paired mean gain of
  `+0.005756834`; Run 31 showed that optimizer micro-tuning did not explain or
  extend it.
- The next highest-evidence intervention is another density increase, not a
  new architecture. Use twice Run 30's training rows while preserving every
  scored/reference row and all model settings.
- Disk audit shows 516 GiB free. Run 30 sample/cache consume 6.8 GiB combined;
  expected quarter-density artifacts fit safely. The protected Run 30
  seed-2028 checkpoint at `0.636251719` remains untouched.

## 2026-08-30 01:10 SGT — deterministic quarter sample completed

- Sampling completed successfully in 365.42 seconds with maximum RSS
  12,845,056 bytes. It retained 51,858,724 of 207,446,146 eligible April 8–28
  rows: 34,074,737 early and 17,783,987 later.
- It skipped 114,832,239 post-April-28 rows after interpreting only their date.
  Early/later CSV SHA-256 values are `74cfc95f…a7945` and
  `03e695c5…daa2b`; sample-manifest SHA-256 is `6b61257e…a0335`.
- The first hash command looked for `manifest.json`; sampling correctly writes
  `sample_manifest.json`. The corrected manifest path passed and no artifact
  was changed. Build the compact cache with a modulo-32 evaluation sidecar;
  no score has occurred.

## 2026-08-30 01:10 SGT — first cache command blocked by explicit scope allowlist

- The first cache command exited 2 in 0.06 seconds before cache construction
  because the CLI benchmark-name choices did not yet include the new explicit
  quarter-training label. No partial cache, iteration, model, or score was
  produced.
- Add that exact label to the cache builder and its campaign wrapper, with
  focused tests. Do not loosen the allowlist to arbitrary strings. Retry the
  otherwise unchanged command only after the full test suite passes.

## 2026-08-30 01:11 SGT — second cache command exposed direct-execution test gap

- The retry exited 1 in 0.06 seconds before cache creation because the new
  constant had been placed after the script's `main()` call. Import-based tests
  passed because imports do not execute that call, but direct CLI execution
  raised `NameError`.
- Move the constant above `main` and add a subprocess test that invokes the
  real script with `--help`, covering the direct execution path. No partial
  cache, iteration, model, or score was produced.

## 2026-08-30 01:18 SGT — quarter cache completed; evaluation identity passed

- Cache construction completed successfully in 394.96 seconds with maximum
  RSS 6,657,130,496 bytes. It contains 51,858,724 rows, 10,158,935 observed
  videos, and 3,307,101 authors. Archive bytes and MD5 matched provenance.
- Cache-manifest SHA-256 is `6f543be6…1bea`; evaluation-remainder SHA-256 is
  `f855b97f…8a26`.
- Filtering residue 0 selected exactly 6,481,138 rows. Every ordered user,
  original video ID, timestamp, date, and label matched the base cache; all 21
  per-date counts also matched. Both independently computed row digests are
  `1f375523…4cd8`.
- The mandatory evaluation-identity gate passes. Build sample-aligned causal
  user and item histories next; no model score has occurred.

## 2026-08-30 01:38 SGT — quarter causal user histories completed and audited

- User-history construction completed successfully in 1,161.44 seconds with
  maximum RSS 6,574,456,832 bytes. All four arrays have shape
  `(51,858,724, 8)` and dtype `int16`; output timestamp inversions are zero.
- Independent SHA-256 checks match the manifests: official
  `9752813b…d3cc`, early `4f87020c…a5a`, middle `6b41cc33…202d`, and late
  `98539ef5…3f58`.
- Independent range checks remain valid: rate buckets are 0–20, match flags
  are 0–1, age is -1–68, and count buckets are nonnegative within the expected
  expanded ranges. Build sample-aligned item histories next using only the
  already validated raw full-corpus work arrays; no score has occurred.

## 2026-08-30 01:39 SGT — first item-history command blocked by scope check

- The first item-history command exited 1 in 0.05 seconds before output
  construction because that builder's explicit benchmark allowlist also lacked
  the quarter-training label. The four validated reuse links remain intact; no
  item history, iteration, model, or score was produced.
- Centralize that builder's three exact permitted scopes in a validation
  helper. Add acceptance/rejection tests and a direct CLI subprocess test;
  retain rejection of arbitrary labels. Retry only after the full suite passes.

## 2026-08-30 01:43 SGT — quarter causal item histories completed and audited

- Item-history construction completed successfully in 215.26 seconds with
  maximum RSS 4,100,472,832 bytes. It reused the validated raw video work and
  matched 189,554,993 full-corpus events.
- All four arrays have shape `(51,858,724, 4)` and dtype `int16`. Independent
  hashes match: official `125bb10c…cbbc`, early `9c8f55cf…9a32`, middle
  `81d31480…f69b`, and late `527a7efd…fc39`.
- Independent ranges pass: count buckets stay within 0–15 and rate buckets
  within 0–19. Daily count/positive tables have shape `(21, 10,158,935)`,
  dtype `uint32`, hashes `1ea512f8…39bb` and `8de8f22e…25c2`, and plausible
  raw ranges.
- Preprocessing gates are complete. Run the full test suite, then the first
  measured `shadow_early` comparison; Run 32 remains at zero scored attempts.

## 2026-08-30 01:45 SGT — attempt 1 passes the early temporal gate

- Attempt `001-quarter-history-item-shadow-early` completed successfully in
  121.18 seconds with maximum RSS 5,902,270,464 bytes. It trained on
  10,253,494 rows and evaluated the exact fixed 865,586 rows.
- Validation primary is `0.624113789`, `+0.002698063` over Run 30. Forward is
  `0.627260428`, `+0.003150787`. Cutpoints and all slice row counts match.
- Slice deltas are cold/low `+0.002458408`, medium `+0.002022780`, high
  `+0.005597851`, early dates `+0.002581775`, and late dates `+0.001811384`.
  Every precommitted gate passes.
- This remains sampled-development evidence only. Repeat the exact frozen
  quarter-density change on the middle window.

## 2026-08-30 01:49 SGT — attempt 2 passes the middle temporal gate

- Attempt `002-quarter-history-item-shadow-middle` completed successfully in
  192.05 seconds with maximum RSS 6,220,038,144 bytes. It trained on
  17,184,689 rows.
- Validation improves `+0.003555171`; forward improves `+0.002385969`.
  Like-for-like slice deltas are cold/low `+0.003954523`, medium
  `+0.002524258`, high `+0.004392633`, early dates `+0.003614213`, and late
  dates `+0.002821468`.
- The middle gate passes, establishing two of three. Run the frozen late window
  and its April 22–28 forward horizon before opening official seeds.

## 2026-08-30 01:54 SGT — attempt 3 passes late; audited official gate opened

- Attempt `003-quarter-history-item-shadow-late` completed successfully in
  270.37 seconds with maximum RSS 7,113,785,344 bytes. It trained on
  24,874,458 rows.
- Validation improves `+0.002867044`; the April 22–28 forward horizon improves
  `+0.002549778`. Fixed slice deltas are cold/low `+0.002189250`, medium
  `+0.005410555`, high `+0.001196234`, early dates `+0.002460524`, and late
  dates `+0.003130572`.
- Quarter density passes all three temporal windows. After auditing the exact
  groups and gates, set `shadow_gate_passed` true. Promote the unchanged model
  to paired official-development seeds 2027/2028/2029; public/hidden outcomes
  remain locked.

## 2026-08-30 02:00 SGT — official-development seed 2027 passes

- Attempt `004-quarter-history-item-official-seed2027` completed in 309.13
  seconds with maximum RSS 7,712,899,072 bytes. It trained on 34,074,737 rows.
- Primary is `0.638339246`, `+0.002659217` over matching Run 30 seed 2027.
  Slice deltas are cold/low `+0.002189190`, medium `+0.002227693`, high
  `+0.005516529`, early dates `+0.001724008`, and late dates `+0.003398462`.
- Preserve the unchanged configuration for seeds 2028 and 2029; one seed is
  insufficient for promotion even though every fixed group improved.

## 2026-08-30 02:05 SGT — official-development seed 2028 confirms the gain

- Attempt `005-quarter-history-item-official-seed2028` completed in 312.76
  seconds with maximum RSS 7,720,288,256 bytes. Primary is `0.638260620`,
  `+0.002008902` over the matching Run 30 seed.
- Fixed slice deltas are cold/low `+0.001359570`, medium `+0.003276326`, high
  `+0.002409709`, early dates `+0.002419437`, and late dates `+0.002560186`.
- Run unchanged seed 2029 before computing paired mean gain and convergence.

## 2026-08-30 02:14 SGT — three official seeds converge; Run 32 closed

- Attempt `006-quarter-history-item-official-seed2029` completed successfully
  in 487.55 seconds with maximum RSS 7,710,982,144 bytes. Primary is
  `0.638563195`, `+0.002459844` over the matching Run 30 seed.
- Fixed slice deltas are cold/low `+0.001860792`, medium `+0.002501391`, high
  `+0.005143390`, early dates `+0.002745741`, and late dates `+0.002410869`.
  Every like-for-like slice improved again.
- Candidate scores for seeds 2027/2028/2029 are `0.638339246`, `0.638260620`,
  and `0.638563195`. Their mean is `0.638387687`, paired mean gain is
  `+0.002375987`, and span is `0.000302575`, below epsilon `0.002`.
- Close Run 32 at six counted successful attempts. Protect seed 2029 at
  `0.638563195`. Checkpoint SHA-256 is `0575c4fa…b6386` (499,271,389 bytes);
  prediction SHA-256 is `1db163a4…cc6f` (8,024,460 bytes). Both remain ignored
  local artifacts.
- This closes only the bounded Run 32 hypothesis. It does not stop the
  hackathon campaign. The result is deterministic 1/32 development evaluation
  with 1/4 training, not a full 27K benchmark, hidden-test, submission, or
  leaderboard score. Open the next hypothesis as a separately disclosed run.
