# Run 33 decision journal

## 2026-08-30 02:17 SGT — half-density continuation opened

- A fresh review after Run 32 confirms the campaign should continue, while the
  bounded Run 32 search remains correctly closed at convergence.
- The same density direction has produced stable gains twice: +0.005756834
  paired mean for 1/8 training and +0.002375987 for 1/4 training. Run 32 also
  improved every time window, seed, and fixed slice.
- The marginal gain is diminishing, so Run 33 precommits a smaller +0.0005
  promotion threshold and will stop this density branch quickly if temporal or
  slice evidence fails. This avoids confusing more rows with guaranteed hidden
  transfer.
- Hardware audit: 64 GiB physical memory and 500 GiB free disk. A half-sample
  is expected to require roughly twice Run 32's 13 GiB sample/cache footprint
  plus histories and temporary artifacts, within the observed local capacity.
- Protect Run 32 seed 2029 (`0.638563195`) unchanged. Add only the exact
  half-training benchmark scope to the three existing allowlists, test the real
  CLI path, then sample and rebuild causal features before any scored attempt.

## 2026-08-30 02:25 SGT — deterministic half sample completed

- Sampling completed successfully in 405.88 seconds with maximum RSS
  13,090,816 bytes. It retained 103,722,500 of 207,446,146 eligible April
  8–28 rows: 68,152,306 early and 35,570,194 later.
- It skipped 114,832,239 post-April-28 rows after interpreting only their date.
  Early/later CSV SHA-256 values are `1a7604e4…3310` and `79dbae0c…5c72c`;
  sample-manifest SHA-256 is `aa8a7863…e91e`.
- Sampling modulus/residue are exactly 2/0 and all 21 dates are populated.
  Build the compact cache with a modulo-32 evaluation sidecar; no scored
  attempt has occurred.

## 2026-08-30 02:35 SGT — half cache completed; evaluation identity passed

- Cache construction completed successfully in 613.43 seconds with maximum
  RSS 11,779,227,648 bytes. It contains 103,722,500 rows, 15,056,686 observed
  videos, and 4,672,924 authors. The source archive's 9,892,191,178 bytes and
  MD5 `3e3c799a24e2d23a4d2c757fbf9adf59` matched provenance.
- Cache-manifest SHA-256 is `a525aba3…e8a0`; evaluation-remainder SHA-256 is
  `a3b71916…5dd4`.
- Filtering remainder 0 selected exactly 6,481,138 rows. Every ordered user,
  original video ID, timestamp, date, and label matched the base cache; all 21
  per-date counts matched. Independently serialized base and half row digests
  both equal `1f375523f1f691c5b3ba59538350b98eef4450d28bb0bde0de4dde451d884cd8`.
- The mandatory evaluation-identity gate passes. Build sample-aligned causal
  user and item histories next; Run 33 remains at zero scored attempts.

## 2026-08-30 03:01 SGT — half causal user histories completed and audited

- User-history construction completed successfully in 1,555.56 seconds with
  maximum RSS 13,186,596,864 bytes. All four arrays have shape
  `(103,722,500, 8)` and dtype `int16`; output timestamp inversions are zero.
- Independent SHA-256 checks match the manifest: official
  `ccbc0a84…ccf3`, early `8b470964…8ad9`, middle `d20d699b…3b11`, and late
  `fb4d4982…3218`.
- Independent range checks pass. Count/feedback buckets stay within their
  declared caps, rate buckets are 0–20, match flags are 0–1, and last-positive
  tag is -1–68.
- The validated raw full-corpus work arrays for video ID, date, user offsets,
  and label remain unchanged in the base cache. Link only these four immutable
  inputs into the half cache and build sample-aligned item histories; no scored
  attempt has occurred.

## 2026-08-30 03:07 SGT — half causal item histories completed and audited

- Item-history construction completed successfully in 320.66 seconds with
  maximum RSS 7,575,453,696 bytes. It reused the validated raw video work and
  matched 199,061,600 full-corpus events.
- All four arrays have shape `(103,722,500, 4)` and dtype `int16`. Independent
  hashes match: official `6690e23e…8da0`, early `b7a17f34…038f`, middle
  `330bd421…9c21`, and late `c569da04…8eb4`.
- Independent ranges pass: video/author count buckets remain 0–15 and rate
  buckets 0–19. Daily count/positive hashes are `ef2dd08c…c80f` and
  `10188eb9…f879`; the immutable raw video-work hash remains
  `0f1de841…a6dcf`.
- All preprocessing gates are complete and 39 tests pass. Run the first
  measured `shadow_early` comparison; Run 33 remains at zero scored attempts.

## 2026-08-30 03:11 SGT — attempt 1 passes the early temporal gate

- Attempt `001-half-history-item-shadow-early` completed successfully in
  194.25 seconds with maximum RSS 8,934,227,968 bytes. It trained on
  20,507,537 rows and evaluated the exact fixed 865,586 rows.
- Validation primary is `0.625425462`, `+0.001311673` over Run 32. Forward is
  `0.629764375`, `+0.002503947`. Cutpoints and all slice row counts match.
- Slice deltas are cold/low `+0.001923047`, medium `+0.000505118`, high
  `+0.000315121`, early dates `+0.000750873`, and late dates `+0.001832522`.
  Every precommitted gate passes.
- The marginal density gain is smaller but positive and forward-safe. Repeat
  the exact frozen half-density change on the middle temporal window.

## 2026-08-30 03:17 SGT — attempt 2 passes the middle temporal gate

- Attempt `002-half-history-item-shadow-middle` completed successfully in
  320.74 seconds with maximum RSS 9,549,004,800 bytes. It trained on
  34,370,048 rows and evaluated the exact fixed 960,523 rows.
- Validation primary is `0.638721358`, `+0.002881399` over Run 32. Forward is
  `0.626894645`, `+0.001900112`. Cutpoints and all slice row counts match.
- Slice deltas are cold/low `+0.002301834`, medium `+0.003712865`, high
  `+0.004507434`, early dates `+0.001623091`, and late dates `+0.002830662`.
  Every precommitted gate passes.
- Two temporal windows pass. Run the unchanged late window and its April
  22–28 forward horizon before opening the audited official gate.

## 2026-08-30 03:26 SGT — attempt 3 passes late; audited official gate opened

- Attempt `003-half-history-item-shadow-late` completed successfully in
  495.42 seconds with maximum RSS 11,847,041,024 bytes. It trained on
  49,749,222 rows.
- Validation improves `+0.002777282`; the April 22–28 forward horizon improves
  `+0.002290829`. Fixed slice deltas are cold/low `+0.003287652`, medium
  `+0.001226643`, high `+0.003049501`, early dates `+0.002051077`, and late
  dates `+0.001697082`.
- Cutpoints and all slice row counts match. Half density passes all three
  temporal windows, forward horizons, and slices. After this manual audit, set
  `shadow_gate_passed` true.
- Promote the unchanged model to paired official-development seeds
  2027/2028/2029 against Run 32. Public/hidden outcomes remain locked.

## 2026-08-30 03:38 SGT — official-development seed 2027 passes

- Attempt `004-half-history-item-official-seed2027` completed successfully in
  701.17 seconds with maximum RSS 12,922,470,400 bytes. It trained on
  68,152,306 rows and evaluated the exact fixed 2,222,628 rows.
- Primary is `0.641520824`, `+0.003181578` over matching Run 32 seed 2027.
  Cutpoints and all slice row counts match exactly.
- Slice deltas are cold/low `+0.002890559`, medium `+0.004404674`, high
  `+0.002160747`, early dates `+0.003149451`, and late dates `+0.002292976`.
- Preserve the unchanged configuration for seeds 2028 and 2029; one seed is
  insufficient for promotion even though every fixed group improved.

## 2026-08-30 03:49 SGT — official-development seed 2028 confirms the gain

- Attempt `005-half-history-item-official-seed2028` completed successfully in
  660.23 seconds with maximum RSS 12,179,030,016 bytes. Primary is
  `0.642439836`, `+0.004179215` over the matching Run 32 seed.
- Fixed slice deltas are cold/low `+0.004457463`, medium `+0.004254804`, high
  `+0.002336714`, early dates `+0.003424995`, and late dates `+0.003297742`.
  Cutpoints and row counts match exactly.
- Two official-development seeds agree. Run unchanged seed 2029 before
  calculating paired mean gain and convergence.

## 2026-08-30 04:00 SGT — three official seeds converge; Run 33 closed

- Attempt `006-half-history-item-official-seed2029` completed successfully in
  602.93 seconds with maximum RSS 12,938,035,200 bytes. Primary is
  `0.642195882`, `+0.003632687` over the matching Run 32 seed.
- Fixed slice deltas are cold/low `+0.003455336`, medium `+0.003498966`, high
  `+0.004711562`, early dates `+0.003137789`, and late dates `+0.002668707`.
  Every like-for-like slice improved again.
- Candidate scores for seeds 2027/2028/2029 are `0.641520824`, `0.642439836`,
  and `0.642195882`. Their mean is `0.642052181`, paired mean gain is
  `+0.003664494`, and span is `0.000919012`, below epsilon `0.002`.
- Close Run 33 at six counted successful attempts. Protect seed 2028 at
  `0.642439836`. Checkpoint SHA-256 is `3b5a7009…1ebe` (731,023,621 bytes);
  prediction SHA-256 is `4b93fb64…56c3` (8,032,460 bytes). Both remain ignored
  local artifacts.
- This closes only the bounded Run 33 hypothesis, not the hackathon campaign.
  The score is deterministic 1/32 development evaluation with 1/2 training,
  not a full 27K benchmark, hidden test, submission, or leaderboard score.
