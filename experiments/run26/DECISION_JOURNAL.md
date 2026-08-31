# Run 26 decision journal

## 2026-08-29 23:41 SGT — recent trend family opened

- Run 24 proved cumulative prior-day video/author signal. Run 25 showed that
  additional action-rate labels hurt top-five ordering and closed immediately.
- Run 26 changes the time horizon, not the target behavior: it adds a fixed
  three-day view alongside cumulative count/long-view rate to represent trends.
- This autonomous transition is separately and cumulatively disclosed. Run 24
  seed 2029 at 0.630624629 remains protected.

## 2026-08-29 23:42 SGT — causal trend cache prepared and independently checked

- The unmodified preprocessing command completed successfully in 3.51 seconds
  wall time with peak RSS 1,101,545,472 bytes.
- Each split array has shape `(6481138, 8)` and dtype `int16`. The first four
  columns exactly retain the cumulative Run 24 fields; the final four add the
  fixed prior-three-day video and author count/long-view-rate fields.
- Independent SHA-256 verification matched the manifest: official
  `2fdc746aec0ba09b49c5721bd6af2998c1a97fa0f0dabbb483cef3aa6ca37467`,
  early `8b85398577f80d7586f8c87f6d698ca0f7b3ac72022d464ca5dda3424a67128d`,
  middle `d69332c11c3409d8042d2b3b64a55faf10ccd6188f4775461afc7d37c22aae6f`,
  and late `5957401e142fe17792c6335c8a3c9b05e6f1a479da9b1319ad16d4e6e973a11b`.
- Observed count bins were within 0–15 and rate bins within 0–19 (the encoded
  bounds are 0–15 and 0–20). Training rows use only earlier calendar days;
  validation and test rows use a cache frozen at the training cutoff.

## 2026-08-29 23:44 SGT — first shadow attempt failed; family closed

- Attempt `001-history-item-trend-shadow-early` completed successfully in
  58.703 seconds with peak RSS 2,184,216,576 bytes. Its best epoch was 6.
- Early validation primary was `0.610561111`, down `0.003898089` from the exact
  Run 24 parent. Forward primary was `0.612190979`, down `0.004322945`.
- All five declared robustness slices regressed: cold/low `-0.002950266`,
  medium `-0.006442182`, high `-0.003286218`, early dates `-0.001929460`, and
  late dates `-0.004231508`.
- The candidate failed every acceptance dimension. No window, bin, prior,
  optimizer, or seed tuning is justified. Run 26 closes after one successful
  attempt; the Run 24 seed-2029 candidate remains protected.
