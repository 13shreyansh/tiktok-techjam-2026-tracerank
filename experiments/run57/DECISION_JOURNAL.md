# Run 57 decision journal

## 2026-08-31 07:25 SGT — combined sequence hypothesis frozen

- Exact 24-field Run52 parent plus 11 fixed causal recent-sequence fields.
- Build only early first; later preparation is locked behind the score gate.
- Preserve Run52. No model attempt may start until early archive verification.

## 2026-08-31 07:28 SGT — early sequence archive independently verified

- The Python builder completed its manifest in `182.707748` seconds with
  `23,448,190,976`-byte peak RSS. The outer `/usr/bin/time -l` command returned
  1 only because the sandbox denied its final `sysctl kern.clockrate` query;
  this is not represented as a zero-exit wrapper run.
- Independent read-only verification confirmed shape `(207446146, 11)`, dtype
  `int16`, 4,563,815,340 bytes, and SHA-256
  `c923ffff272f87b9a93b78be7ba523c6b3b059399a1079af041b15cfbfaae712`.
- The manifest records 41,010,906 training rows, 166,435,240 frozen score rows,
  25,695 source-order inversions corrected to zero causal inversions, and
  6,626,844 simultaneous multirow timestamp batches.
- Unlock exactly the seed-2027 early model attempt.

## 2026-08-31 07:43 SGT — sequence gate fails decisively

- Attempt 1 completed successfully in `746.208740` seconds with
  `31,684,935,680`-byte peak RSS.
- Combined primary is `0.6323049226201478`, regressing
  `-0.0028604164125673` versus exact Run52. GAUC regressed
  `-0.0032633884162504`, nDCG@5 `-0.0024574444088842`, and forward primary
  `-0.0052830863275360`.
- Every fixed slice crossed the `-0.001` guard: cold/low
  `-0.0026969801914234`, medium `-0.0025298103778844`, high
  `-0.0044425374937088`, early dates `-0.0018734127180537`, and late dates
  `-0.0025127036764150`.
- The ignored 3,787,021,709-byte checkpoint SHA-256 is
  `b52c94698e8e0a9e6706a3c9672a4723d722709a1dd0ab8cec88f517b2b96f06`;
  the 6,625,227-byte prediction SHA-256 is
  `1bfba96269c497d27aeb3b22e0bfd69c2c3da4cb5988d30cef98ff6ae766a652`.
- Stop without middle, late, or official sequence preparation; no field subset,
  history-length, action, rank, objective, or ensemble variation follows.
