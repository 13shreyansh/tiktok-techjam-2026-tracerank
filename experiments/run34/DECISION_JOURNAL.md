# Run 34 decision journal

## 2026-08-30 04:02 SGT — full-density continuation opened

- A fresh review after Run 33 confirms the campaign must continue while Run 33
  remains correctly closed at convergence. Its paired mean gain was
  `+0.003664494`, and every temporal window, seed, and fixed slice improved.
- The final density doubling is higher-evidence than an unrelated architecture
  switch because it changes only training coverage and has two consecutive
  stable predecessors. It is still a hypothesis, not a guaranteed hidden-test
  improvement.
- Hardware audit: 64 GiB physical memory and 470 GiB free disk. The half
  sample/cache use about 25.4 GiB; a full sample/cache plus histories and model
  artifacts fits the available disk. Peak half preprocessing/model RSS was
  about 13.2 GiB/12.9 GiB, leaving substantial headroom for expected growth.
- Protect Run 33 seed 2028 (`0.642439836`) unchanged. Add only the exact
  full-training benchmark scope to the three allowlists and tests, then build
  and audit the full-density data before any scored attempt.

## 2026-08-30 04:13 SGT — deterministic full sample completed

- Sampling completed successfully in 605.63 seconds with maximum RSS
  12,763,136 bytes. It retained all 207,446,146 eligible April 8–28 rows:
  136,296,576 early and 71,149,570 later.
- It skipped 114,832,239 post-April-28 rows after interpreting only their date.
  Early/later CSV SHA-256 values are `4712bc9d…a389a` and
  `3f63f106…d27ca`; sample-manifest SHA-256 is `bf4df1db…65187`.
- Sampling modulus/residue are exactly 1/0; sampled count equals eligible count
  on all 21 dates. Build the compact cache with a modulo-32 evaluation sidecar;
  no scored attempt has occurred.

## 2026-08-30 04:31 SGT — full cache completed; evaluation identity passed

- Cache construction completed successfully in 1,046.01 seconds with maximum
  RSS 22,510,403,584 bytes. It contains 207,446,146 rows, 21,922,851 observed
  videos, and 6,522,683 authors. The source archive's 9,892,191,178 bytes and
  MD5 `3e3c799a24e2d23a4d2c757fbf9adf59` matched provenance.
- Cache-manifest SHA-256 is `977c5252…c9f31`; evaluation-remainder SHA-256 is
  `d853045e…33cdb`.
- Filtering remainder 0 selected exactly 6,481,138 rows. Every ordered user,
  original video ID, timestamp, date, and label matched the base cache; all 21
  per-date counts matched. Independently serialized base and full row digests
  both equal `1f375523f1f691c5b3ba59538350b98eef4450d28bb0bde0de4dde451d884cd8`.
- The mandatory evaluation-identity gate passes. Build sample-aligned causal
  user and item histories next; Run 34 remains at zero scored attempts.

## 2026-08-30 05:01 SGT — full causal user histories completed and audited

- User-history construction completed successfully in 1,801.14 seconds with
  maximum RSS 25,827,131,392 bytes. All four arrays have shape
  `(207,446,146, 8)` and dtype `int16`; output timestamp inversions are zero.
- Independent SHA-256 checks match the manifest: official
  `01dee13e…9f9e6`, early `fde59d6b…d881`, middle `8d8a8a5a…a263e`, and late
  `5f165019…d00b2`.
- Independent range checks pass. Count/feedback buckets stay within their
  declared caps, rate buckets are 0–20, match flags are 0–1, and last-positive
  tag is -1–68.
- Link only the four independently validated immutable raw full-corpus inputs
  into the full cache and build sample-aligned causal item histories; no scored
  attempt has occurred.

## 2026-08-30 05:08 SGT — full causal item histories completed and audited

- Item-history construction completed successfully in 357.29 seconds with
  maximum RSS 11,592,089,600 bytes. It reused the validated raw video work and
  matched all 207,446,146 full-development events.
- All four arrays have shape `(207,446,146, 4)` and dtype `int16`. Independent
  hashes match: official `98db3b71…c525`, early `da11e332…7659f`, middle
  `e279f312…d4732`, and late `344008b3…abe10`.
- Independent ranges pass: video/author count buckets remain 0–15 and rate
  buckets 0–19. Daily count/positive hashes are `c0ba4628…0e266` and
  `afae4b70…6e7a4`; the immutable raw video-work hash remains
  `0f1de841…a6dcf`.
- All preprocessing gates are complete and 42 tests pass. Run the first
  measured `shadow_early` comparison; Run 34 remains at zero scored attempts.

## 2026-08-30 05:14 SGT — attempt 1 early shadow passed

- Attempt 1 completed successfully in 374.54 seconds with maximum RSS
  14,551,072,768 bytes. It trained on 41,010,906 full-density rows and selected
  epoch 1, compared with the locked Run 33 parent's 20,507,537 rows and epoch 1.
- On the exact same 865,586 validation rows, primary improved from
  `0.6254254623053686` to `0.6296437130222816` (`+0.004218250716913063`).
  On the exact same 960,523 forward rows, primary improved from
  `0.6297643752865603` to `0.6320813514931201`
  (`+0.0023169762065597954`).
- Every fixed robustness slice improved: cold/low `+0.003454631`, medium
  `+0.005323787`, high `+0.005523028`, early-date `+0.003970524`, and
  late-date `+0.003384695`. This clears the precommitted early gate by a wide
  margin with no slice regression.
- This is one development shadow, not hidden-test evidence. Preserve the
  attempt artifact and run the unchanged middle shadow next; do not alter the
  model or thresholds between windows.

## 2026-08-30 05:27 SGT — attempt 2 middle shadow passed

- Attempt 2 completed successfully in 688.94 seconds with maximum RSS
  16,455,860,224 bytes. It trained on 68,733,893 full-density rows and selected
  epoch 1.
- On the exact same 960,523 validation rows, primary improved from
  `0.6387213578545639` to `0.6410410548830812`
  (`+0.002319697028517309`). On the exact same 1,149,994 forward rows, primary
  improved from `0.6268946449519104` to `0.6304888800927152`
  (`+0.0035942351408048134`).
- Every fixed slice improved: cold/low `+0.002294561`, medium `+0.001899140`,
  high `+0.002986696`, early-date `+0.002701414`, and late-date
  `+0.002649585`. The middle gate passes with no slice regression.
- Two of two temporal shadows now pass, but late-period evidence remains
  mandatory. Preserve attempt 2 and run the identical late shadow next.

## 2026-08-30 05:44 SGT — attempt 3 late shadow passed; temporal gate opens

- Attempt 3 completed successfully in 972.16 seconds with maximum RSS
  19,910,901,760 bytes. It trained on 99,488,135 full-density rows and selected
  epoch 1.
- On the exact same 1,149,994 validation rows, primary improved from
  `0.6332286187573829` to `0.6371920416305701`
  (`+0.0039634228731871834`). On the exact same 2,222,628 forward rows, primary
  improved from `0.6341933049455075` to `0.6376533462808371`
  (`+0.003460041335329622`).
- Every fixed slice improved: cold/low `+0.002192649`, medium `+0.005726855`,
  high `+0.008933986`, early-date `+0.004058572`, and late-date
  `+0.002745723`. The late gate passes with no slice regression.
- All three temporal windows pass under the frozen configuration. Set the
  shadow gate true and run official-development seeds 2027, 2028, and 2029.
  Promotion still requires paired mean gain of at least `+0.0005` over Run 33
  and no individual seed regression below `-0.0005`.

## 2026-08-30 06:08 SGT — attempt 4 official seed 2027 passed

- Attempt 4 completed successfully in 1,397.07 seconds with maximum RSS
  23,231,447,040 bytes. It trained on all 136,296,576 official-prefix rows and
  selected epoch 1.
- Primary improved from the paired Run 33 seed score `0.6415208243276544` to
  `0.6446150727413003` (`+0.003094248413645806`). GAUC improved
  `+0.002574203`; nDCG@5 improved `+0.003614294`.
- All fixed slices improved: cold/low `+0.002439235`, medium `+0.002664279`,
  high `+0.007460133`, early-date `+0.003423267`, and late-date
  `+0.002963829`.
- Model SHA-256 is
  `5ed2d55f3ec7173edbd547ef9ad4fedea6bbcd5c1f683091de059f23ec7910a4`
  (1,053,512,773 bytes). Prediction SHA-256 is
  `2d1ec4ee4c705e93cee536467bcb68d8512c5428ad7daf4a97b32fc0633eb6fc`
  (8,035,934 bytes).
- One seed passes but is insufficient for promotion. Run seed 2028 unchanged.

## 2026-08-30 06:30 SGT — attempt 5 official seed 2028 passed

- Attempt 5 completed successfully in 1,306.08 seconds with maximum RSS
  23,416,307,712 bytes. It trained on all 136,296,576 official-prefix rows and
  selected epoch 1.
- Primary improved from the paired Run 33 seed score `0.6424398358563015` to
  `0.6450834641517389` (`+0.0026436282954374057`). GAUC improved
  `+0.001975999`; nDCG@5 improved `+0.003311258`.
- All fixed slices improved: cold/low `+0.001717291`, medium `+0.002717118`,
  high `+0.007770916`, early-date `+0.002698614`, and late-date
  `+0.001990098`.
- Model SHA-256 is
  `0b473b20f570e64d46f68600432db21c047fb92ab2d2e97db59f08b7d5f26190`
  (1,053,512,773 bytes). Prediction SHA-256 is
  `e00a479ec967caa8b25264f14b3e14d872194d19845a50d3f4e43e3e9387cdb7`
  (8,034,023 bytes).
- Two seeds pass consistently. Run seed 2029 unchanged before computing the
  three-seed promotion statistics.

## 2026-08-30 06:53 SGT — attempt 6 passed; Run 34 converged and closed

- Attempt 6 completed successfully in 1,319.79 seconds with maximum RSS
  22,893,281,280 bytes. It trained on all 136,296,576 official-prefix rows and
  selected epoch 1.
- Primary improved from the paired Run 33 seed score `0.6421958821471199` to
  `0.6448042058583618` (`+0.0026083237112419777`). GAUC improved
  `+0.002508845`; nDCG@5 improved `+0.002707803`.
- All fixed slices improved: cold/low `+0.002076936`, medium `+0.003230091`,
  high `+0.004058811`, early-date `+0.002700466`, and late-date
  `+0.002029272`.
- Model SHA-256 is
  `04bc906944cb3d81e388a5377f0aa702149496fe3f9e1feff1f85f4661eeb456`
  (1,053,512,773 bytes). Prediction SHA-256 is
  `0a400ecfe7a9a525502e38b547a9e8f9084efadfb17f302c5ac22db45d7838b1`
  (8,032,499 bytes).
- Official scores are `0.6446150727413003`, `0.6450834641517389`, and
  `0.6448042058583618`; mean `0.6448342475838004`, paired mean gain over Run
  33 `+0.002782066806775063`, span `0.00046839141043863997`. Every seed and
  slice passes, and the span is below the predeclared `0.002` convergence
  epsilon. Protect seed 2028 and close Run 34 at attempt 6.
- This closure is only for the bounded run. The overall hackathon goal remains
  active; open a fresh hypothesis family after a strategic audit.
- Closure verification: `.venv/bin/python -m pytest -q` could not run because
  pytest is not installed (`No module named pytest`). The repository's
  standard-library suite then passed with `.venv/bin/python -m unittest
  discover -s tests -p 'test_*.py'`: 42 tests, zero failures, in 0.280 seconds.
