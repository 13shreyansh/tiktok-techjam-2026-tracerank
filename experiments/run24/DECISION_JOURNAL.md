# Run 24 decision journal

## 2026-08-29 21:29 SGT — verified 27K anchor opened

- Official archive acquisition, MD5, safe-entry inspection, extraction, and
  schema inspection all succeeded before this run opened.
- KuaiRand-1K families through Run 23 failed their fixed forward gates; 27K is
  the highest-value independent benchmark family still explicitly authorized
  by the organizer.
- HSTU and FuXi-Linear provide long-history design evidence but their published
  CUDA stacks and task definitions are not directly comparable here.
- The first run is intentionally a simple memory-bounded anchor. Sampling and
  cache preparation are included in Run 24 wall time but are not mislabeled as
  scored model iterations.
- This is an autonomous transition under the already active goal; no new human
  model configuration or score was supplied.

## 2026-08-29 21:35 SGT — deterministic sample succeeded

- Command completed in 336.04 seconds with 12,697,600-byte `/usr/bin/time -l`
  maximum resident set size (the script-reported value was 12,664,832 bytes).
- Early logs: 136,296,576 eligible rows and 4,258,510 sampled rows.
- April 22-28: 71,149,570 eligible rows and 2,222,628 sampled rows.
- The date gate rejected 114,832,239 post-April-28 rows. No model score or
  iteration was produced.
- Every retained date landed near the fixed 1/32 rate. Continue to verified
  cache construction; do not alter the modulus after seeing these counts.

## 2026-08-29 21:40 SGT — sampled cache succeeded

- Cache command completed in 244.37 seconds with 2,550,398,976-byte maximum
  resident set size.
- Exact cache size: 6,481,138 rows; 4,258,510 training and 2,222,628
  post-training development rows; date range April 8-28.
- All 27,285 users remain. Observed sample spaces are 2,726,849 videos and
  1,090,713 authors, reversibly mapped from the official 32,038,725-video and
  8,839,735-author spaces.
- Independent array checks confirmed equal lengths, date bounds, and mapping
  counts. Development long-view rate is 0.2620154053.
- Run 24 remains at zero scored iterations. The fixed five-field rank-8
  `shadow_early` anchor is now allowed to run.

## 2026-08-29 21:49 SGT — content/context FM passed all shadow gates

- The unchanged five-field anchor completed on all three chronological
  windows. Validation primary scores were 0.594730056, 0.605278517, and
  0.602965662; forward scores were 0.599259633, 0.598919166, and 0.606065166.
- Adding only the available content/context fields (play-time bucket,
  production type, and device type) raised paired validation primary by
  0.011591585, 0.010301627, and 0.011701503.
- Paired forward primary rose by 0.010598458, 0.011088723, and 0.011681900.
  The minimum activity-slice primary also rose on every window by 0.013733334,
  0.009876229, and 0.013097147. There was no gate-breaking slice regression.
- The family therefore passed three of three chronological shadows, exceeding
  the protocol's two-of-three threshold. `shadow_gate_passed` is now true.
- These are deterministic sampled-development results, not the full 27K
  benchmark, organizer hidden score, or a submission. The next family must add
  a behavior/history signal and retain the same paired-window discipline.

## 2026-08-29 21:50 SGT — first history-cache command failed safely

- The first causal-history preparation command exited 1 in 0.13 seconds with
  maximum RSS 327,401,472 bytes because sampled source rows contained
  within-user timestamp inversions. It produced no model score and is not a
  scored iteration.
- The cache contained every required history array; its independent format
  version was not a valid reason to reject it. Compatibility is now checked by
  explicit schema and the locked April 8-28 date range.
- Recovery was restricted to a causal ordering repair: sort by user, timestamp,
  and original row. Equal timestamps remain simultaneous and update state only
  after the complete impression batch.

## 2026-08-29 21:58 SGT — causal history cache succeeded

- The repaired command completed in 448.43 seconds with maximum RSS
  1,025,196,032 bytes. Seventeen tests passed, including a deliberately
  nonchronological source-row fixture.
- Depending on cutoff, source order contained 23,951 to 26,362 within-user
  timestamp inversions. All four emitted histories report zero inversions after
  sorting and retain 106,719 to 361,332 simultaneous multirow batches.
- Each history array is 103,698,336 bytes and is kept in ignored output storage.
  Its manifest binds the arrays to cache-manifest SHA-256
  `59acbfad49abe61d1c51864afb3f85b587ffd58e47a50c32cee638ec39153d99`.
- These preprocessing commands consumed Run 24 wall time but did not increment
  the scored-iteration count. The first paired history shadow is now allowed.

## 2026-08-29 22:01 SGT — causal history passed three shadow windows

- Paired against the promoted content FM, history improved validation primary
  by 0.001654371, 0.003696349, and 0.002728785 across early, middle, and late
  windows. Forward primary improved by 0.002533846, 0.003613652, and
  0.002801495.
- Every paired window passed the fixed family gate. The early high-activity
  slice was the closest call at -0.000824802, still inside the 0.001 tolerance;
  all middle and late slices improved.
- The family therefore advanced to paired official-development seeds. This is
  still sample-local evidence and not an organizer hidden result.

## 2026-08-29 22:12 SGT — three official seeds completed; ensemble rejected

- Content/history paired primary scores were 0.620511378/0.624713481 for seed
  2027, 0.616492449/0.626141456 for seed 2028, and
  0.622782827/0.625046341 for seed 2029. History's mean paired gain was
  0.005371542 and both GAUC and nDCG@5 improved for every seed.
- Seed 2029 nevertheless failed the robustness rule: high-activity primary
  fell from 0.549641475 to 0.547504035 (-0.002137440). Thus three aggregate
  wins do not establish three fully gate-passing seeds.
- The fixed three-history-seed within-user rank ensemble scored 0.625972142.
  It exceeded the mean history member but not seed 2028's 0.626141456, and its
  high-activity primary 0.549920554 did not beat seed 2028's 0.551184728.
- Reject the ensemble as a promotion. Preserve seed 2028 as the strongest 27K
  sample checkpoint, explicitly conditional on this development scope. Do not
  select a post-hoc two-seed subset.

## 2026-08-29 22:13 SGT — rich current-item metadata rejected

- Adding music type, visibility, aspect, and causal item age to the content FM
  changed early validation primary from 0.606321641 to 0.606198569
  (-0.000123071). Forward improved by 0.001231096, but high-activity primary
  regressed by 0.002630128.
- This fails both the +0.001 validation requirement and the slice guard. Close
  the rich-field family after one scored attempt; do not tune field subsets.
- The next independent hypothesis is denser history: preserve the fixed scored
  sample but update user history from every prior official development event.

## 2026-08-29 22:22 SGT — full-history launch import failed safely

- The first full-history preprocessing launch exited 1 in 0.05 seconds with
  maximum RSS 23,625,728 bytes because its package import worked under tests
  but not under direct script execution.
- No source scan, output cache, model score, or scored iteration occurred.
  Recovery adds an explicit direct-execution import fallback and verifies both
  invocation modes before restart.

## 2026-08-29 22:37 SGT — full-history emission stopped on date ambiguity

- Both raw-log passes and exact sample/cache alignment completed, but the first
  feature-emission attempt exited 1 after 834.37 seconds with maximum RSS
  4,080,992,256 bytes. Some identical epoch timestamps carry adjacent local
  date labels and therefore straddled a split cutoff.
- No model score or scored iteration occurred. The complete user-partitioned
  working set remains ignored and is reused only after validating its lengths,
  dtypes, monotonic offsets, and an exact one-to-one mapping of all 6,481,138
  sampled row indices.
- Safe rule: all rows sharing a user/timestamp are emitted simultaneously, but
  only rows whose declared date is within the training cutoff update state.
  Validation-side outcomes at the same timestamp remain excluded. A targeted
  cross-date same-timestamp test now guards this rule.

## 2026-08-29 22:51 SGT — full-history cache completed and verified

- The validated-resume command completed in 1,257.13 seconds with maximum RSS
  4,203,937,792 bytes. It reused only the independently validated
  user-partitioned work set and did not reread the 23 GB raw logs.
- The cache retains all 207,446,146 official events and exactly matches all
  6,481,138 fixed sampled rows. User-level state uses every causal earlier
  official event; sampled tag-level state remains unchanged.
- Independent SHA-256 checks matched the manifest for all four 103,698,336-byte
  arrays: official `e3408211…5256b`, early `5b1f08a8…180ba`, middle
  `4eb973e2…eecd3`, and late `a39c9930…b4a6`.
- These are ignored preprocessing artifacts, not a model result. Run 24 remains
  at 17 scored iterations. The full-history family now enters the same paired
  chronological gates, beginning with early versus iteration 7.

## 2026-08-29 22:55 SGT — full-history family rejected at the first gate

- Iteration 18 scored 0.608224277 on early validation versus the promoted
  sampled-history parent's 0.607976012, a gain of only 0.000248265 against the
  predeclared +0.001 requirement.
- Forward primary improved by 0.000684246 and all tracked slices improved by
  0.000112253 to 0.000773250, so there is no regression signal. The effect is
  nevertheless too small to justify the preprocessing cost or additional
  window/seed searches.
- Close the full-corpus-history family after one scored attempt. Preserve the
  sampled-history seed-2028 checkpoint; do not run middle, late, or official
  full-history variants.

## 2026-08-29 22:58 SGT — within-user ranking objective declared

- The organizer metric ranks each user's candidates and gives half its weight
  to nDCG@5. Pointwise binary cross-entropy does not directly compare a user's
  positive and negative items.
- Test one bounded ranking-stage objective: reproduce the exact sampled-history
  parent, then apply one pairwise epoch over training-only long-view/non-long-
  view pairs from the same user. Use the existing fixed learning rate 0.0002
  and cap of five positives per usable user; no pair-count or rate sweep.
- This differs from Run 16's rejected same-impression pairs: the evaluator
  groups the scored list by user, not by impression timestamp. It remains a
  per-item scorer and does not add forbidden re-ranking logic.
- First gate is early versus iteration 7, with the unchanged +0.001 validation,
  -0.0005 forward, and -0.001 slice rules. Close immediately on failure.

## 2026-08-29 23:00 SGT — first pairwise launch failed before scoring

- Attempt 19 reproduced the pointwise parent but exited 1 before pair training
  or final evaluation because the pair constructor assumed cache rows were
  grouped by user. The 1K cache satisfied that incidental layout; the fixed
  27K sample does not.
- This attempt consumed 95.05 subprocess seconds, peaked at 1,764,605,952-byte
  RSS, produced no candidate score, and remains counted in the run ledger.
- Recovery stable-sorts a local index view by user while returning original
  cache row indices. An interleaved-row regression test is required before the
  unchanged hypothesis may retry; no model parameter or gate changes.

## 2026-08-29 23:03 SGT — within-user ranking objective rejected

- The corrected attempt 20 used 109,324 training-only pairs from 24,206 usable
  users. Validation moved from 0.607976012 to 0.607992189 (+0.000016177), far
  below the +0.001 gate; forward moved +0.000112468.
- GAUC rose by 0.000110129 while nDCG@5 fell by 0.000077775. Slice movements
  were between -0.000034 and +0.000184, with no material robustness benefit.
- Close pairwise objectives without tuning pair count, rate, or epochs. Preserve
  the pointwise history checkpoint.

## 2026-08-29 23:05 SGT — causal item-quality family declared

- Full user-history aggregates were marginal, but the raw logs contain many
  additional exposures of the sampled videos. A video's and author's earlier
  exposure count and long-view rate are a distinct signal for item quality and
  cold-item confidence that the current FM omits.
- Build four categorical fields from every official event for sampled videos:
  prior-day video count/rate and prior-day author count/rate. Training rows see
  only earlier calendar days; scoring rows freeze at the split cutoff. No
  same-day, validation, post-April-28, or full-month statistic is used.
- Use fixed log2 count buckets (cap 15) and the existing Beta(1,3) 21-bin rate
  buckets. Test the unchanged rank-8 sparse FM against iteration 7 on early;
  close on the existing validation, forward, or slice gate failure.

## 2026-08-29 23:15 SGT — causal item-quality cache verified

- The command completed in 550.75 seconds with 2,506,522,624-byte maximum RSS.
  It matched 149,177,950 full-corpus events for the fixed sampled-video set.
- Daily count and positive arrays independently matched manifest SHA-256 values
  `9bc1fac4…86cdc` and `426bc40a…384f4`; the aligned raw-video work array matched
  `0f1de841…5a6dcf`.
- All four 6,481,138-row feature arrays independently matched their manifest
  hashes. Count buckets lie in 0-15 and rate buckets in 0-20 as declared.
- The model test combines these four fields with the exact eight causal user-
  history fields, rather than replacing the promoted history representation.
  Twenty-two tests pass before the first score.

## 2026-08-29 23:18 SGT — causal item quality passed the early gate

- Iteration 21 improved early validation from 0.607976012 to 0.614459200
  (+0.006483188) and forward from 0.612391937 to 0.616513924
  (+0.004121988).
- GAUC improved +0.006027571 and nDCG@5 improved +0.006938804. Every date and
  activity slice improved by 0.004938 to 0.007421; the weakest high-activity
  slice rose +0.004937640.
- This clears all gates by a wide margin. Run the unchanged middle and late
  windows against iterations 8 and 9 before any official-development score.

## 2026-08-29 23:23 SGT — causal item quality passed all shadows

- Middle validation/forward improved +0.007094634/+0.003395730; late improved
  +0.004750812/+0.002872807. Both component metrics rose in both windows.
- Fourteen of fifteen slice comparisons improved. Late high-activity changed
  by -0.000038036, far inside the -0.001 guard; every other slice rose by at
  least 0.003270.
- The family is three-for-three and advances to unchanged official seeds. The
  mandatory fresh-context review is recorded in `STRATEGIC_REVIEW_024.md`
  before attempt 24 executes.

## 2026-08-29 23:31 SGT — three official seeds promoted; Run 24 closed

- Paired parent/candidate primary scores were 0.624713481/0.630043252 for seed
  2027, 0.626141456/0.630096716 for seed 2028, and
  0.625046342/0.630624629 for seed 2029. Mean gain was +0.004954439.
- GAUC, nDCG@5, and every one of fifteen activity/date slice comparisons
  improved. The smallest slice gain was +0.002234925.
- The three candidate scores span 0.000581378, inside the fixed 0.002
  convergence epsilon. Close Run 24 at iteration 26 and protect seed 2029 at
  0.630624629. This is a deterministic 27K development-sample result, not a
  full 27K, hidden, submitted, or organizer-leaderboard score.
- The 72-hour search continues only through a new, separately declared and
  cumulatively disclosed run; Run 24 will not accept further attempts.
