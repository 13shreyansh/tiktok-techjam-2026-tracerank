# Run 36 decision journal

## 2026-08-30 07:02 SGT — labels-blind audit and run opening

- Run 35 correctly closed after its first gate failure. Do not tune pairwise
  learning rate, pair cap, patience, or negative selection.
- The next independent transfer risk is high-cardinality memorization. On the
  fixed official-development feature rows, training-frequency median is 0 for
  video and 412 for author. Video has 1,377,905 unseen rows and author has
  208,209; labels were not accessed for this audit.
- A single minimum count 5 is conservative: it adds only 111,978 low-support
  video rows and 112,112 low-support author rows to their existing cold pools.
  The shared buckets will be learned from rare training observations instead
  of remaining zero-only unseen fallbacks.
- Add frequency-mask logic and tests, fix boolean pairwise trace serialization,
  and commit before scoring. No threshold or field subset search is permitted.

## 2026-08-30 07:05 SGT — implementation gate passed

- Added training-only minimum-frequency masks with default count 1 preserving
  prior behavior. Run 36 will set video and author counts to 5; field dimensions
  and all other encodings remain unchanged.
- Results and checkpoints now record both thresholds and retained video/author
  counts. Legacy checkpoints default missing threshold metadata to 1 for strict
  compatibility checks.
- Corrected pairwise trace selection to serialize JSON booleans; this does not
  alter Run 35 metrics or decision.
- Ranker SHA-256 is
  `495a722611e9c2912ea5105d94570375403f81e4f1477955512869177dfe9f32`.
  Python compilation and 47 standard-library tests pass with zero failures.
  Commit before attempt 1.

## 2026-08-30 07:12 SGT — early shadow failed; Run 36 closed

- Attempt 1 completed successfully in 394.885 seconds with 14,225,686,528-byte
  peak RSS. The output is durable and the public test remained locked.
- Early validation primary was `0.6236370376110999`, down
  `0.0060066754111817` from Run 34. Forward primary was
  `0.6258332778114647`, down `0.0062480736816554`.
- All five fixed robustness slices regressed: cold/low `-0.004800578`, medium
  `-0.008202487`, high `-0.006364902`, early-date `-0.004253418`, and
  late-date `-0.005973638`.
- This misses every predeclared continuation gate. Do not try thresholds 2–4,
  separate video/author thresholds, or another seed in this run. Close the
  hypothesis after one attempt and preserve Run 34 unchanged.
