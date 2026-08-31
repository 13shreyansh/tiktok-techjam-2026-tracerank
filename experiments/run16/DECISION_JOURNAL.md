# Run 16 decision journal

## 2026-08-29 17:22 SGT — family selection

- Question: does this action improve the probability of winning rather than
  merely generate another Pure micro-experiment?
- Answer: potentially. KuaiRand-1K is explicitly an optional bonus benchmark,
  the Pure track has plateaued across independent families, and the 1K data is
  designed for long sequential recommendation. Bonus scoring weight and hidden
  delivery remain unknown, so the first gate is bounded feasibility rather
  than an open-ended port.
- Main failure modes: an in-memory Pure loader would exhaust memory; dense FM
  gradients would make each batch prohibitively expensive; millions of cold
  items may make ID embeddings weak; and an unspecified bonus formula may make
  the effort low-value.
- Safeguards: streaming train/validation-only cache, sparse updates, three
  chronological windows, strict attempt/time/convergence guards, and protected
  Pure fallback unchanged.

## 2026-08-29 17:22 SGT — engineering verification

- The first `py_compile` command failed because macOS attempted to write bytecode
  under a sandbox-disallowed user cache path. This was not a model iteration and
  did not read data.
- The independent synthetic metric-equivalence test passed exactly for random
  cases including tied scores: the fast 1K evaluator matched the unchanged
  organizer evaluator within `1e-12` for GAUC, nDCG@5, and primary.
- Recovery: direct future compilation uses `PYTHONPYCACHEPREFIX=/tmp`.

## 2026-08-29 17:24 SGT — cache contract mismatch

- The first cache build stopped after four seconds before reading interaction
  labels because the checksum-verified archive contains 4,371,868 basic video
  rows with maximum reindexed ID 4,371,899. The project page instead publishes
  4,369,953 items, and a contiguous-ID assertion therefore failed.
- This was an engineering command, not a model iteration. It yielded material
  provenance evidence: the 2025 archive's catalogue count differs from the
  paper/project-page summary, and its ID space has 32 holes.
- Recovery: preserve observed and published counts separately; allocate the
  observed max-ID space; and map the 32 missing metadata IDs to the explicit
  unknown author slot. No model or split choice changed.

## 2026-08-29 17:25 SGT — cache materialized

- The repaired cache command materialized 7,580,964 development rows: 5,055,984
  on April 8–21 and 2,524,980 on April 22–28. It skipped 4,132,081 later rows
  by date without accessing or retaining their `long_view` field.
- The script itself completed and wrote its manifest in 40.57 seconds. The
  surrounding macOS `/usr/bin/time -l` wrapper then returned status 1 because
  its private `sysctl kern.clockrate` query was sandbox-denied. That wrapper
  failure is not misreported as a cache failure.
- Recovery: record `RUSAGE_SELF` inside the cache builder and rerun the same
  deterministic materialization directly for an exit-zero receipt and maximum
  RSS. This remains engineering preparation, not a learned-model attempt.

## 2026-08-29 17:31 SGT — sparse-FM shadow family passed

- Early validation/forward primary: `0.621936720 / 0.626362731`.
- Middle validation/forward primary: `0.633581124 / 0.625855279`.
- Late validation/forward primary: `0.632952862 / 0.625044702`.
- All three commands succeeded in 56–107 seconds with 2.89–2.94 GB peak RSS.
  Both metrics remained meaningful in every window; no forward window
  collapsed. The high-activity slice has lower nDCG because those users have
  much longer candidate lists, but its GAUC is the strongest slice and its
  primary improves as more history becomes available (`0.5356`, `0.5541`,
  `0.5744`).
- Decision: the fixed model passes the bounded feasibility and temporal gate.
  Open official validation for exactly seeds 2026, 2027, and 2028. Do not tune
  rank, learning rate, batch size, or epoch count from these results.

## 2026-08-29 17:32 SGT — output-only artifact repair

- Before official seeds, the ranker was extended to serialize the training-only
  seen-value masks and validation predictions alongside its existing weights,
  offsets, dimensions, duration edges, split, and seed.
- This changes the recorded source hash but not model construction, optimizer,
  data, metrics, training order, hyperparameters, or any shadow result. It is an
  engineering reproducibility repair, not a model attempt.

## 2026-08-29 17:37 SGT — three official seeds complete

- Seed 2026: GAUC `0.672622914`, nDCG@5 `0.611548342`, primary
  `0.642085628`.
- Seed 2027: GAUC `0.672149932`, nDCG@5 `0.614014423`, primary
  `0.643082177`.
- Seed 2028: GAUC `0.672717754`, nDCG@5 `0.607282588`, primary
  `0.640000171`.
- The primary range is `0.003082006`; GAUC is stable within `0.000568`, while
  most variance is top-five ordering. All three are coherent and materially
  above their first epochs, but no organizer 1K baseline is published.
- Decision: run the one predeclared equal mean within-user-percentile-rank
  ensemble from all three saved predictions. Do not select members or tune
  weights from their observed scores.

## 2026-08-29 17:38 SGT — fixed seed ensemble promoted

- Equal mean within-user percentile rank scored GAUC `0.673404099`, nDCG@5
  `0.615050750`, primary `0.644227425`.
- Gain over best seed 2027 is `+0.001145247`, with both GAUC and nDCG higher.
  The ensemble becomes the immutable KuaiRand-1K fallback; it does not replace
  the protected KuaiRand-Pure candidate.
- The last three seed attempts did not create an epsilon convergence stop
  because the predeclared ensemble then improved the current attempt sequence
  by more than `0.002`. The family is nevertheless closed after seven attempts.
- Next hypothesis: cold validation videos lose their video and often author ID
  embedding, but the official basic table supplies primary tag, upload type,
  and video type. Add exactly those three categorical fields to the same sparse
  FM and screen all three shadow windows against the recorded base FM. Do not
  add music or tune a subset after observing results.

## 2026-08-29 17:41 SGT — content cache extension verified

- Cache format 2 added label-free primary-tag, upload-type, and video-type
  identities from the official basic item table: 69, 32, and 3 values.
- Deterministic rebuild succeeded in 73.45 seconds with 480,706,560-byte peak
  RSS. All seven base arrays retained their exact prior SHA-256 hashes, proving
  the 0.644227425 fallback's row order and inputs were unchanged.
- This was an engineering cache extension, not a learned-model attempt.

## 2026-08-29 17:42 SGT — content early window passed

- Validation primary improved from base `0.621936720` to `0.636106651`
  (`+0.014169931`). Forward improved from `0.626362731` to `0.641647569`
  (`+0.015284838`). Both GAUC and nDCG@5 improved in both windows.
- Low-, medium-, and high-activity validation primary improved by
  `+0.009258871`, `+0.014173894`, and `+0.037444783`, respectively. This is not
  a fragile cold-user-only effect.
- Attempt 8 triggered the mandatory fresh-context guard. Decision: after the
  review, run the unchanged middle and late windows. No field subset,
  learning-rate, rank, or epoch adjustment is allowed.

## 2026-08-29 17:46 SGT — content shadow family passed

- Middle validation/forward gains over base: `+0.013056742 / +0.012104090`.
- Late validation/forward gains over base: `+0.010053997 / +0.014907130`.
- All three chronological windows improved validation and forward by more than
  five times the fixed `0.002` gate. Both metrics improved throughout, and no
  activity slice regressed.
- Decision: run official seeds 2026, 2027, and 2028 unchanged, then one equal
  mean user-rank ensemble. Preserve `0.644227425` until that ensemble is
  verified.
- Before official seeds, content-seen masks were added to checkpoint
  serialization. This is output-only engineering and does not alter the model.

## 2026-08-29 17:55 SGT — content official family closed

- Seed 2027: GAUC `0.688554039`, nDCG@5 `0.611426370`, primary
  `0.649990205`.
- Seed 2026: GAUC `0.689090119`, nDCG@5 `0.615028804`, primary
  `0.652059461`.
- Seed 2028: GAUC `0.688786149`, nDCG@5 `0.618707357`, primary
  `0.653746753`.
- All three selected epoch 4. Their primary range is `0.003756548`; GAUC is
  stable within `0.000536080`, while most variance remains in top-five order.
- The predeclared equal mean within-user-percentile-rank ensemble scored GAUC
  `0.689452389`, nDCG@5 `0.617017354`, primary `0.653234872`. It is
  `0.000511881` below seed 2028 and its minimum activity-slice primary
  (`0.587982539`) is also below seed 2028 (`0.591205474`).
- Decision: promote the seed-2028 content FM as the current KuaiRand-1K
  candidate and reject the ensemble. This is a validation decision only; it
  does not replace or alter the protected KuaiRand-Pure candidate.
- The family is closed. No ensemble weighting, seed selection beyond the
  predeclared three, rank, learning-rate, or content-subset tuning follows.

## 2026-08-29 18:07 SGT — causal sequence-history family rejected

- A cache-format extension added only prior feedback fields; every previously
  used base/content/date/label array retained its exact SHA-256. Four ignored
  split-specific histories were then precomputed with zero timestamp
  inversions. Same-user/same-timestamp rows were emitted before batch outcomes
  updated state, and validation/forward state was frozen at the train cutoff.
- The causal-history unit test passed. The real precomputation found 809,272
  simultaneous multirow batches in the official training period, confirming
  that same-row-order updates would have created substantial leakage.
- On the early shadow, history scored validation `0.637327703` versus content
  `0.636106651` (`+0.001221052`, below the fixed `0.002` gate). Its forward
  score was `0.637897660` versus content `0.641647569` (`-0.003749910`). The
  high-activity validation slice also fell from `0.556469440` to `0.549024657`.
- Decision: reject and close this exact history family after one model attempt.
  Do not run middle/late or official validation and do not tune smoothing,
  buckets, or included feedback from this result. The content seed-2028 1K
  candidate remains unchanged.

## 2026-08-29 18:10 SGT — same-impression pairwise family rejected

- The pair sampler unit test proved that every positive/negative pair shares
  both user and timestamp. On the early split, 155,429 mixed-label impression
  batches produced 358,789 fixed pairs, capped at five positives per batch.
- After the unchanged content pointwise checkpoint, one predeclared pairwise
  epoch moved validation from `0.636106651` to `0.635846175`
  (`-0.000260476`). It moved forward from `0.641647569` to `0.642195188`
  (`+0.000547619`). Neither magnitude meets the fixed `0.002` gate, and
  validation nDCG@5 regressed even though GAUC rose slightly.
- Decision: reject and close. Do not tune the pairwise learning rate, pair cap,
  number of negatives, epochs, or hard-negative policy. Do not run the family
  on later shadows or official validation.

## 2026-08-29 18:12 SGT — statistic table excluded; multi-tag family fixed

- The official README defines every `video_features_statistic_1k.csv` value as
  an average over the full month. The table directly includes long-time-play
  counts, the judged target concept. It has no date column with which to make a
  prior-only join. Using it would leak future validation/test outcomes, so the
  entire 3.1 GB table is excluded without a model attempt.
- The label-free basic table audit found 3,289,054 videos with one tag, 918,131
  with two, 26,293 with three, 903 with four, 3 with five, and 137,484 with no
  tag. Tags are bounded integer IDs 0–68.
- Next fixed family: add exactly tag positions two and three to the promoted
  content representation. This captures nearly all multi-tag videos without
  inspecting labels or tuning a tag subset. Screen early/middle/late against
  the recorded one-tag content FM before any official validation.

## 2026-08-29 18:15 SGT — multi-tag family rejected

- The multi-tag early validation score was `0.640972017`, a gain of
  `+0.004865366` over the one-tag content model. Its forward score was only
  `0.636652526`, a regression of `-0.004995043` against the same parent.
- The conflict is large and directional: extra tags help the nearby period but
  do not transfer to the later one. It fails the predeclared requirement that
  both validation and forward improve by at least `0.002`.
- Decision: reject and close after one attempt. Do not run middle, late, or
  official validation; do not separate second from third tag after observing
  this result. The current 1K candidate remains content seed 2028.

## 2026-08-29 18:18 SGT — rich label-free metadata family fixed

- The remaining safe basic-table audit found seven music types, four visibility
  states, three coarse aspect classes, and usable upload dates for all but 58
  catalogue rows. Music ID has 2,622,610 distinct nonmissing values and is
  excluded because it mostly duplicates sparse video identity.
- The fixed family adds only music type, visibility, portrait/square/landscape,
  and video age at the interaction date using edges 1/3/7/14/30/90/365 days.
  Missing or apparently future upload dates map to unknown. The one-month
  statistic table remains excluded.
- Screen all four fields together against the one-tag content FM. If the early
  validation and forward gains are not both at least `0.002`, close the entire
  family without field ablation or official validation.

## 2026-08-29 18:20 SGT — literal convergence audit and campaign lock

- A fresh audit caught that the literal organizer rule had already triggered:
  after attempt 13 set the `0.653746753` best, attempts 14, 15, and 16 produced
  no improvement above epsilon `0.002`. Run 16 should have stopped at attempt
  16.
- Attempts 17 and 18 were executed before this accounting mistake was caught.
  Both are rejected, neither evaluated public-test labels, and neither altered
  the attempt-13 candidate. They are retained in the immutable ledger but
  explicitly excluded as post-convergence exploration.
- Attempt 18 independently failed both content gates: validation
  `0.634508083` (`-0.001598568`) and forward `0.637413681`
  (`-0.004233888`). This does not excuse the overrun.
- Decision: hard-lock `run16` against all further model attempts. Report 18
  executed, 16 convergence-eligible, and 2 excluded post-convergence attempts.
  Packaging and label-free inference verification may continue without opening
  another search campaign.

## 2026-08-29 18:25 SGT — frozen candidate packaged label-blindly

- The saved seed-2028 checkpoint reconstructed all 2,524,980 saved official
  validation predictions bit-for-bit; maximum absolute error was `0.0`.
- A streaming inference pass generated 4,132,081 predictions for April 29–May
  8. The code resolves and indexes only date, user, video, tab, and duration
  fields from the interaction log. It does not resolve or index any outcome
  column and computes no public-test metric.
- A second label-blind pass checked every row ID, user ID, video ID, finite
  score, and the exact source row count. The resulting ignored CSV SHA-256 is
  `b3b8fa2ac501daf31608fae8875f02b14f7812dc976620ac791d16acb2d56764`.
  Inference plus alignment took 47.558 seconds with 1,600,421,888-byte peak
  RSS.
- Decision: retain this as an unsubmitted local test-format package. Do not
  claim organizer format acceptance: no 1K-specific checker or delivery route
  was published, so the schema is derived from the Pure starter and the
  statement that 1K uses the same task.
- A deliberate wrapper lock test returned nonzero with `search is closed at
  convergence iteration 16`; SHA-256 checks confirmed that neither run state
  nor ledger changed. The lock is operational, not merely documentary.
- The first final `py_compile` command failed before checking code because
  Python tried to write bytecode under the macOS user cache, outside the
  permitted workspace. Re-running with `PYTHONPYCACHEPREFIX=/tmp/track2-pycache`
  succeeded. Three causal-history/pair-sampler unit tests passed, all 14
  protected Pure artifacts reverified by hash, and a fresh 1K check-only pass
  revalidated all 4,132,081 rows in 17.599 seconds without outcome access.
