# Run 45 decision journal

## 2026-08-30 23:21 SGT — frozen before feature build or score

- Run 43 remains protected at local 27K development-sample primary
  `0.6501881386335703`; Run 39 seed 2029 remains the single-model fallback.
- Topic affinity is selected from the workshop's history clue and the strong
  exact-repeat result, not from a Run 45 score. It can transfer to unseen
  videos/creators sharing a known primary tag.
- Exactly two prior-only fields and one fixed model configuration are allowed.
  Start with early state and stop immediately if its frozen gate fails.

## 2026-08-30 23:41 SGT — early causal archive completed

- The builder wrote all `207446146` cache rows across four source user
  segments. The ignored archive is 829,784,712 bytes with SHA-256
  `9e16654f699d1e27e8ee5e39095f89fdf9d08292812d608c83cdd4a513b62e68`.
- Observed build time was 1,215.340 seconds and peak RSS was
  6,021,070,848 bytes. The base cache manifest SHA-256 remains
  `977c5252243089ac1a91f935f60a80d6a1e3c5e027bede3b0e749983f8fc9f31`.
- Proceed with exactly one seed-2027 early model under the frozen gate. No
  feature result has been scored yet.

## 2026-08-30 23:52 SGT — directionally positive but below gate; close family

- The fixed seed-2027 early model selected epoch 1 and reached primary
  `0.6332310596477319`, `+0.0003451863513865` over the exact repeat parent.
  Forward reached `0.6351351013841763`, a gain of
  `+0.0003819371095913`.
- GAUC changed `-0.0002150195447559` while nDCG@5 gained
  `+0.0009053922475289`. Slice changes were cold/low `+0.0001699028750877`,
  medium `+0.0002858887344874`, high `+0.0016561919743743`, early dates
  `+0.0003241008349949`, and late dates `-0.0000424019177868`.
- Both aggregate gains are below the frozen `+0.0005` continuation gate.
  Stop before middle/late/official builds, seeds, or bucket/tag variations.
  Preserve Run 43 and carry only the directional learning into a fresh audit.
