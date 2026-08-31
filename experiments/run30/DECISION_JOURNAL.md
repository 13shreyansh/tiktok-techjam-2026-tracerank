# Run 30 decision journal

## 2026-08-29 23:57 SGT — expanded-density family opened

- Run 24's causal item-quality fields produced the only large 27K gain. Runs
  25–29 show diminishing returns from extra rates, short trends, capacity,
  cross-capacity blending, and loss weighting.
- Training still uses only one of every 32 eligible events. Increase only
  trainable row density to one of every 8 while keeping every scored row fixed
  to residue 0 modulo 32. Any row-order/equality mismatch blocks scoring.
- Run 24 seed 2029 at `0.630624629` remains protected during the longer build.

## 2026-08-30 00:06 SGT — deterministic 1/8 sample completed

- The sampling command completed successfully in 410.98 seconds with maximum
  RSS 12,910,592 bytes. It retained 25,927,452 of 207,446,146 eligible April
  8–28 rows (`0.124984014`), including 17,035,578 early and 8,891,874 later
  rows.
- It skipped 114,832,239 post-April-28 rows after reading only their date.
- SHA-256: manifest `cc195747…2af43`, early CSV `46ae794d…d720f`, later CSV
  `828f110a…e943d`. These ignored files are preprocessing artifacts only.
- Build the compact expanded cache and a modulo-32 remainder sidecar. Scoring
  remains blocked until the selected remainder-0 rows exactly match Run 24.

## 2026-08-30 00:12 SGT — expanded cache completed; evaluation identity passed

- Cache construction completed in 310.60 seconds with maximum RSS
  3,908,616,192 bytes. It contains 25,927,452 rows, 6,706,543 observed videos,
  and 2,310,477 authors.
- Cache manifest SHA-256 is `a6ed2d9d…2e7b6`; the modulo-32 remainder array is
  `35119eca…e3dc5`.
- Filtering residue 0 selected exactly 6,481,138 rows. Every ordered user,
  original video ID, timestamp, date, and label matched Run 24, including all
  21 per-date counts. The comparison digest is `e929a02c…02fe9`.
- The mandatory identity gate passes. Build causal user and item histories; no
  model score has occurred.

## 2026-08-30 00:27 SGT — expanded causal user histories completed

- User-history construction completed successfully in 792.20 seconds with
  maximum RSS 4,204,412,928 bytes. All four arrays have shape
  `(25,927,452, 8)` and dtype `int16`; each occupies 414,839,360 bytes.
- SHA-256: official `bf00fc0a…e65af`, early `808edd51…b81e`, middle
  `1bdf1abb…2c12`, late `fcc59738…ce818` (independently rechecked with
  `shasum -a 256`). Output timestamp inversions are zero for every view after
  the required chronological sort.
- Observed column ranges remain plausible: count-like fields are nonnegative,
  smoothed-rate buckets stay within 0–20, the prior-watch indicator stays
  within 0–1, and age stays within -1–68.
- Before item-history construction, four working reuse symlinks were found to
  have an extra parent-directory component. The error was detected by an
  explicit `test -e` gate before the item builder or any model ran. The four
  broken links were replaced with resolving links to the already validated
  Run 24 raw full-corpus arrays; no dataset, history artifact, attempt, or
  score was affected.

## 2026-08-30 00:33 SGT — expanded causal item histories completed and audited

- Item-history construction completed successfully in 296.76 seconds with
  maximum RSS 3,259,219,968 bytes. It reused the validated raw video work and
  matched 178,319,581 full-corpus events.
- All four output arrays have shape `(25,927,452, 4)` and dtype `int16`.
  Independent SHA-256 checks matched the manifest: official
  `d467515d…f771f`, early `cf031dec…88e1b`, middle `f40f228b…afc1e`, and late
  `3eeb2377…b6cd52`.
- Independent range checks passed. Video and author count buckets stay within
  0–13 and 0–15 respectively; both smoothed long-view-rate buckets stay within
  0–19. Daily raw count/positive work arrays have shape `(21, 6,706,543)`,
  dtype `uint32`, and manifest-matching hashes `10fad14b…c4c28` and
  `1b2925e0…e64db`.
- The first independent hash command looked for the daily arrays in the cache
  root and stopped after correctly hashing the four histories because the
  daily work files live under `full_history_work/`. The corrected exact paths
  passed; this verification-command path error did not alter any artifact.
- Preprocessing gates are complete. Run tests before the first measured model
  attempt; no model score has occurred yet.

## 2026-08-30 00:35 SGT — attempt 1 passes the early temporal gate

- Attempt `001-expanded-history-item-shadow-early` completed successfully in
  94.95 seconds with maximum RSS 3,916,775,424 bytes. It trained on 5,127,894
  expanded-cache rows and evaluated the exact 865,586 Run 24 validation rows.
- Validation primary is `0.621415726`, improving over the exact Run 24 parent
  `0.614459200` by `+0.006956526`. Forward primary is `0.624109641`, improving
  over `0.616513924` by `+0.007595717`.
- Every protected slice improved: cold/low `+0.005713341`, medium
  `+0.007949055`, high `+0.008171202`, early dates `+0.008896397`, and late
  dates `+0.006850461`. The precommitted early gate passes without an
  exception or threshold reinterpretation.
- This is deterministic development-sample evidence only, not the full 27K
  benchmark, organizer hidden test, submission, or leaderboard score. Repeat
  the exact frozen density change on the middle temporal split.

## 2026-08-30 00:40 SGT — attempt 2 improves middle metrics; activity audit blocks acceptance

- Attempt `002-expanded-history-item-shadow-middle` completed successfully in
  186.38 seconds with maximum RSS 3,992,731,648 bytes. Validation primary is
  `0.632284788`, `+0.005913660` over the exact Run 24 middle parent. Forward is
  `0.622608564`, `+0.005591293`; early- and late-date slices improve by
  `+0.005918770` and `+0.005765215`.
- Audit found that activity cutpoints changed from Run 24's `[79, 167]` to
  `[313, 662]`. The scorer used all denser training rows to define activity,
  so the candidate activity groups did not contain the same rows as the
  parent. Primary, forward, and date metrics remain valid because their
  evaluation rows are fixed, but activity-slice deltas from attempts 1–2 are
  not comparable. The activity claims in the previous journal entry are
  withdrawn pending corrected reruns.
- Correct the scorer so model fitting still uses every expanded training row,
  while robustness activity is computed from the locked residue-0 training
  subset. Ordinary caches remain unchanged. A focused unit test plus the full
  suite pass (30 tests). Re-run early and middle under the corrected source;
  do not grandfather either attempt into the two-of-three gate.

## 2026-08-30 00:42 SGT — corrected attempt 3 is the first valid temporal pass

- Attempt `003-expanded-history-item-shadow-early-fixed-slices` completed
  successfully in 81.54 seconds with maximum RSS 3,920,838,656 bytes. Overall
  validation and forward scores exactly reproduce attempt 1.
- Activity cutpoints now exactly match the Run 24 parent at `[49, 106]`.
  Candidate and parent activity-slice row counts also match exactly: 293,332
  cold/low, 287,598 medium, and 284,656 high.
- With like-for-like groups, all protected slices improve: cold/low
  `+0.005600873`, medium `+0.008467439`, high `+0.008090939`, early dates
  `+0.008896397`, and late dates `+0.006850461`. Validation and forward remain
  `+0.006956526` and `+0.007595717` over Run 24.
- The corrected early gate passes and counts as one of three temporal tests.
  Repeat the corrected scorer on the middle window; attempt 2 remains logged
  but does not count.

## 2026-08-30 00:44 SGT — corrected attempt 4 passes the middle temporal gate

- Attempt `004-expanded-history-item-shadow-middle-fixed-slices` completed
  successfully in 114.86 seconds with maximum RSS 4,089,872,384 bytes. It
  trained on 8,591,300 rows while using the exact 2,147,993 Run 24 rows only
  as the robustness activity reference.
- Cutpoints `[79, 167]` and all activity/date slice row counts exactly match the
  parent. Validation improves `+0.005913660`; forward improves `+0.005591293`.
  Slice deltas are cold/low `+0.004702091`, medium `+0.007378629`, high
  `+0.008399044`, early dates `+0.005918770`, and late dates `+0.005765215`.
- The corrected middle gate passes. Two of three temporal passes are now
  established, but run the frozen late window before official-seed promotion
  to measure the longest forward horizon rather than stopping at the minimum.

## 2026-08-30 00:47 SGT — corrected attempt 5 passes late; three-for-three shadow promotion

- Attempt `005-expanded-history-item-shadow-late-fixed-slices` completed in
  159.19 seconds with maximum RSS 4,664,442,880 bytes. It trained on
  12,436,275 rows and used the exact 3,108,516 Run 24 activity-reference rows.
- Cutpoints `[118, 244]` and every slice row count exactly match the parent.
  Validation improves `+0.005437530`; the April 22–28 forward window improves
  `+0.005931331`. Slice deltas are cold/low `+0.005082282`, medium
  `+0.004976040`, high `+0.007939836`, early dates `+0.005551483`, and late
  dates `+0.005158189`.
- The frozen density change passes all three temporal windows without a slice
  regression. Promote unchanged to official-development seeds 2027, 2028, and
  2029, paired against the matching Run 24 history-item seeds. Hidden/public
  test outcomes and submission remain locked.

## 2026-08-30 00:48 SGT — audited shadow gate opened; first official command blocked safely

- The first official-seed command exited before model execution because the
  run state still had `shadow_gate_passed: false`; the campaign wrapper does
  not infer promotion from ledger scores. No result file, model training,
  iteration, or score was produced.
- After manually auditing the three corrected passing ledgers, set only
  `shadow_gate_passed` to true. Iterations remain 5, public-test access remains
  locked, and the official seed-2027 command may now be retried unchanged.

## 2026-08-30 00:52 SGT — official-development seed 2027 passes

- Attempt `006-expanded-history-item-official-seed2027` completed in 214.23
  seconds with maximum RSS 4,716,986,368 bytes. It trained on 17,035,578 rows
  and evaluated the exact 2,222,628 Run 24 official-development validation
  rows; no forward/public-test score was requested.
- Primary is `0.635680029`, `+0.005636777` over the matching Run 24 seed.
  Cutpoints and all slice row counts match exactly. Slice deltas are cold/low
  `+0.004902963`, medium `+0.007250077`, high `+0.005029011`, early dates
  `+0.005212674`, and late dates `+0.004776545`.
- Best epoch is 1 versus the Run 24 parent's 3, consistent with faster fitting
  on denser data but also a reason not to extrapolate from one seed. Preserve
  the frozen configuration and run seeds 2028 and 2029.

## 2026-08-30 00:55 SGT — official-development seed 2028 confirms the gain

- Attempt `007-expanded-history-item-official-seed2028` completed in 183.97
  seconds with maximum RSS 4,734,566,400 bytes. Primary is `0.636251719`,
  `+0.006155003` over the matching Run 24 seed; best epoch remains 1.
- Fixed slice deltas are cold/low `+0.005839295`, medium `+0.005940839`, high
  `+0.007482158`, early dates `+0.006007559`, and late dates `+0.005334662`.
  All cutpoints and row counts match the parent.
- Two official-development seeds agree. Run the unchanged seed 2029 against
  the strongest Run 24 parent before calculating mean gain and convergence.

## 2026-08-30 00:59 SGT — three official seeds converge; Run 30 closed

- Attempt `008-expanded-history-item-official-seed2029` completed in 185.32
  seconds with maximum RSS 4,690,493,440 bytes. Primary is `0.636103351`,
  `+0.005478722` over the strongest Run 24 parent. All identical slices improve
  by `+0.004797240` to `+0.006552502`; best epoch is again 1.
- Candidate scores for seeds 2027/2028/2029 are `0.635680029`, `0.636251719`,
  and `0.636103351`. Their mean is `0.636011700`, paired mean gain is
  `+0.005756834`, and span is `0.000571690`, below epsilon `0.002`.
- Close Run 30 at eight counted successful attempts. Protect seed 2028 at
  `0.636251719`. Checkpoint SHA-256 is `6349cc5d…56eb` (334,657,829 bytes);
  prediction SHA-256 is `ef7f3f26…3014` (8,004,876 bytes). Both remain ignored
  local artifacts.
- This is the deterministic 1/32 development evaluation with denser 1/8
  training, not a full 27K benchmark, hidden test, submission, or leaderboard
  score. Open any further model hypothesis as a separately disclosed run.
