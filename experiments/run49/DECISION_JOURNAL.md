# Run 49 decision journal

## 2026-08-31 00:39 SGT — membership frozen before ensemble score

- Parent Run 43 early consensus: primary `0.6338878866774128`; forward
  `0.6360985056312563`.
- Fixed input prediction SHA-256 values, in order:
  - rank-8 seed 2027:
    `5cc887cf5fa608025df949febeb918ced610a1815fdf7ac61950a58aaa843b02`
  - rank-8 seed 2028:
    `85b476d4477a41c01277ccefb44914774dfa03b85380af08ce1f389533de0538`
  - rank-8 seed 2029:
    `abbca756cc775af14252c83e892f13867c9dbcb8d56c17dc2fd6b9d6dd2cdaf4`
  - rank-16 seed 2027:
    `ed420a98c352bebe2ba3bfe2e462fb8cf8df5d7d73392e574e9ea55ca50aa234`
- Score exactly one equal four-member early consensus. A sub-gate result closes
  this membership without weights, subsets, or another rank.

## 2026-08-31 00:41 SGT — early ensemble gate passes

- Attempt 1 exited zero. Validation primary is `0.6343004353435262`, a gain of
  `+0.0004125486661134`; forward primary is `0.6364502717949139`, a gain of
  `+0.0003517661636576` over the exact Run 43 early consensus.
- Every frozen slice improved: cold/low `+0.0001894950871466`, medium
  `+0.0006697777465996`, high `+0.0010885865030139`, early dates
  `+0.0000128719586532`, and late dates `+0.0003789486196382`.
- The ignored consensus prediction SHA-256 is
  `66535a00531ad42cb025576525a7418e37e62fc339d013b60e21369f39b10ac2`.
  Attempt elapsed time was `7.856405` seconds and peak subprocess RSS was
  3,398,483,968 bytes.
- The early gate authorizes only the unchanged rank-16 seed-2027 middle and
  late members followed by the same four-way equal-rank consensus.

## 2026-08-31 00:59 SGT — middle ensemble gate passes

- Attempt 2 trained the fixed rank-16 middle member and selected epoch 1 in
  `1024.945643` seconds, with peak RSS 20,238,123,008 bytes. Attempt 3 scored
  the fixed four-member consensus in `8.127016` seconds.
- Consensus validation primary is `0.6453043899797450`, a gain of
  `+0.0003173346434118`; forward is `0.6349216595428666`, a gain of
  `+0.0006500682478364` over Run 43 middle.
- All slices improved: cold/low `+0.0002309751585818`, medium
  `+0.0003781142498716`, high `+0.0005477082072343`, early dates
  `+0.0001129502641554`, and late dates `+0.0002726790266813`.
- Model SHA-256 is
  `9efc4268b91b9f4fc60706f946bb55b9fe72ed8d5795ad66d70ee5b6e8fdf392`;
  member prediction SHA-256 is
  `2fb8b44308261464c72e151d98019c2d8ade871f2ffc7eefff238fcdf5c34187`;
  consensus prediction SHA-256 is
  `60a21137b9ed9c20c08b180b80fae152dd06c5708fb3afc7e76e1829859ec878`.
- Early and middle now pass, but complete the predeclared late test before
  opening official training.

## 2026-08-31 01:20 SGT — late passes; all three shadows confirm

- Attempt 4 trained the fixed rank-16 late member and selected epoch 1 in
  `1224.587901` seconds, with peak RSS 27,398,815,744 bytes. Attempt 5 scored
  the fixed consensus in `9.881772` seconds.
- Consensus validation primary is `0.6420194144400580`, a gain of
  `+0.0004998306761548`; forward is `0.6427179746376772`, a gain of
  `+0.0007538339773043` over Run 43 late.
- All slices improved: cold/low `+0.0003328292779022`, medium
  `+0.0003698482197307`, high `+0.0015009597368829`, early dates
  `+0.0004722298211153`, and late dates `+0.0005051559419472`.
- Model SHA-256 is
  `8501a0a3159f43f5e25baf027300bf3fc88235f6314026e71f32d727e07a67a7`;
  member prediction SHA-256 is
  `189c6a57aa716c88e6c6ad3bcf06c65e8af4524b4d1f3be59d97c41864428ecc`;
  consensus prediction SHA-256 is
  `2d593e36083f3b542b04f8063538ad38f745cf2d2dc68aa9ef6620468e1215be`.
- Early, middle, and late all pass with positive validation, forward, and slice
  deltas. Open exactly one fixed official rank-16 seed-2027 member.

## 2026-08-31 01:49 SGT — official gate passes; promote

- Attempt 6 trained the fixed official rank-16 seed-2027 member and selected
  epoch 1. Its individual primary was `0.6509324353012714`. Training exited
  zero in `1656.962607` seconds with peak RSS 28,455,649,280 bytes.
- Attempt 7 scored the exact four-member consensus and exited zero in
  `10.867754` seconds. GAUC is `0.7047811197152637`, nDCG@5 is
  `0.5971320304996821`, and primary is `0.6509565751074728`.
- Versus Run 43, primary gains `+0.0007684364739026`, GAUC gains
  `+0.0004955929650601`, and nDCG@5 gains `+0.0010412799827452`.
- Every official slice improves: cold/low `+0.0006515642245275`, medium
  `+0.0007329051292458`, high `+0.0013066670931650`, early dates
  `+0.0003003591877796`, and late dates `+0.0007348126573359`.
- Official rank-16 model SHA-256 is
  `254109e02b71a8f756c9f58bbd4befc15c75fc043b29c8531ff6c840aadb3e8b`;
  member prediction SHA-256 is
  `c3507f1faa5eb0d8eaf068768eda478db76c3603b2f592cbd74ccce195207c66`;
  consensus prediction SHA-256 is
  `d78777fa1e0193bc9b2b23df5baf02f20113405f031d79dc2df74aab0250cfd1`.
- Promote the fixed four-member consensus as the protected 27K development
  candidate. This does not imply hidden-test or leaderboard performance and
  does not stop the overall campaign.
