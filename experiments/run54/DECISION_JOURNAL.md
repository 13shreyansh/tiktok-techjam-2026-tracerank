# Run 54 decision journal

## 2026-08-31 07:06 SGT — rank-32 topic-affinity hypothesis frozen

- The only model change is the existing two-field causal primary-tag affinity
  encoder on the exact Run52 rank-32 parent.
- Existing early feature archive SHA-256 is
  `9e16654f699d1e27e8ee5e39095f89fdf9d08292812d608c83cdd4a513b62e68`,
  829,784,712 bytes over 207,446,146 rows.
- Preserve Run52 and begin with seed-2027 early only. Later feature builds and
  all official training remain locked behind their declared gates.

## 2026-08-31 07:17 SGT — early gate fails; topic-capacity branch closes

- Attempt 1 completed successfully in `583.584926` seconds with
  `29,213,523,968`-byte peak RSS.
- Candidate primary is `0.6341768633198739`, regressing
  `-0.0009884757128412` versus exact Run52 rank-32. GAUC changed
  `-0.0005653607709151`, nDCG@5 `-0.0014115906547674`, and forward primary
  `-0.0001424604771062`.
- All fixed primary slices regressed. High activity changed
  `-0.0031349960604745` and early dates `-0.0012520649948180`, each crossing
  the frozen `-0.001` slice guard.
- The ignored 3,786,957,637-byte checkpoint SHA-256 is
  `a9208acb0f03864066e3f55c0a60b04fc9d84e81e46482f9fa44858f278f4c61`;
  the 6,603,912-byte prediction archive SHA-256 is
  `85103dc2fe2726f2f9f206be704108133bce2fb075f21a844e4052bc1634c5d8`.
- Stop without building middle, late, or official tag archives and without any
  later or official model. Rank32 does not rescue the earlier rank8 topic clue.
