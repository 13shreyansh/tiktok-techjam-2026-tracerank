# Run 58 decision journal

## 2026-08-31 07:45 SGT — additive tail frozen

- Base fields 0–23 interact exactly as in Run52; fields 24–34 are linear only.
- Reuse the independently verified Run57 early sequence archive.
- Begin with seed-2027 early only and preserve Run52.

## 2026-08-31 07:56 SGT — additive sequence-tail gate fails

- Attempt 1 completed successfully in `623.637632` seconds with
  `31,456,198,656`-byte peak RSS.
- Early primary is `0.6316654090484246`, or `-0.0034999299842905` versus
  exact Run52. GAUC regressed `-0.0029737837727527`, nDCG@5 regressed
  `-0.0040260761958284`, and forward primary regressed
  `-0.0011815746015321`.
- Every fixed slice regressed: cold/low `-0.0035704596217806`, medium
  `-0.0035895747252990`, high `-0.0028887693988795`, early dates
  `-0.0007289192442849`, and late dates `-0.0027939835610252`.
- The ignored 3,787,021,709-byte checkpoint SHA-256 is
  `8fec6ff4e5298c0e1991cdb2318ded4f2829f7c1ef10b7420e41c23c8d20357e`;
  the ignored 6,619,983-byte prediction SHA-256 is
  `bba5ac50a354dd4cf32d01417948a8bf627231b7bd24663ad7ab204aa81b936e`.
- Stop this architecture branch after one attempt. Do not prepare middle or
  late sequence archives and do not search sequence subsets or tail weights.
