# Run 48 decision journal

## 2026-08-31 00:03 SGT — representation and gates frozen before score

- Run 43 remains protected at local 27K development-sample primary
  `0.6501881386335703`.
- Run 45 showed weak but consistent early primary-tag affinity; Runs 46-47
  failed to turn it into a global or routed candidate and remain closed.
- Full-cache read-only coverage: tag 1 valid on 202,886,252 rows; distinct tag
  2 valid on 34,333,275; distinct tag 3 valid on 951,810, out of 207,446,146
  rows. Run 48 changes only how prior primary-tag affinity is accumulated.
- Unit audit passes 39 tests. Builder SHA-256 is
  `c76be67c7e26c9788268d90b1cef539856fbecc4dd015d80b483983355cb9014`;
  ranker SHA-256 is
  `ac60e09ea16503e3d6d927b8100a45b9cbc76a4e52c89f74bc4a6693b9002863`.
- Build early once, record provenance and resources, then score seed 2027. A
  sub-gate result closes this exact family without bucket or capacity tuning.

## 2026-08-31 00:27 SGT — early causal artifact verified

- The builder emitted a complete manifest after `1399.211288` seconds. The
  outer `/usr/bin/time -l` command returned exit 1 only after the child output,
  because sandboxing denied its final `sysctl kern.clockrate` query; do not
  represent the wrapper command as a zero-exit run.
- Independent verification exited zero: shape `(207446146, 2)`, dtype `int16`,
  count buckets `0..13`, rate buckets `0..20`, and exact expected row count.
- Artifact: `user_multitag_history_shadow_early.npy`, 829,784,712 bytes,
  SHA-256
  `7809e65724a42a249480bbafac035334f1078ded58588d85a23728e048bcdadd`.
- Builder-reported peak RSS was 7,748,534,272 bytes. The wrapper printed
  `1399.28 real`, `1351.94 user`, and `13.87 sys` before its sandbox error.
- The artifact is ignored and not committed. Proceed to exactly one declared
  seed-2027 paired early evaluation.

## 2026-08-31 00:37 SGT — positive but below both gates; close

- Attempt 1 exited zero and selected epoch 1. Validation primary was
  `0.6332129485871906`, `+0.0003270752908452` over the exact repeat parent;
  forward primary was `0.6350109623757293`, `+0.0002577981011443`.
- GAUC changed `-0.0003397962796746` while nDCG@5 gained
  `+0.0009939468613651`. Slice changes were cold/low
  `+0.0003122743046099`, medium `+0.0000229133559279`, high
  `+0.0014588785007073`, early dates `+0.0002316998794909`, and late dates
  `-0.0002554852691493`.
- The slices remain within the safety floor, but both validation and forward
  are below the frozen `+0.0005` continuation gate. Close without middle,
  late, official, seed, bucket, current-tag, capacity, or ensemble variants.
- Attempt elapsed time was `523.473079` seconds; peak subprocess RSS was
  16,137,142,272 bytes. Ignored model SHA-256 is
  `609f3c7a5b52125ddab93d7666c62779c1b5499f1703381da127a94e6d7f2bc7`;
  ignored prediction SHA-256 is
  `2db39eea87d939e6683e8b2945354650818d3961e673d845a752d051c69b6457`.
