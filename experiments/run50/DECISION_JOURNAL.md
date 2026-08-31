# Run 50 decision journal

## 2026-08-31 01:50 SGT — seeds and gates frozen before training

- Protected Run49 official primary is `0.6509565751074728`.
- Existing rank-16 seed-2027 official primary is `0.6509324353012714`; its
  early prediction SHA-256 is
  `ed420a98c352bebe2ba3bfe2e462fb8cf8df5d7d73392e574e9ea55ca50aa234`.
- Seeds 2028 and 2029 are inherited from the successful Run43 consensus, not
  selected after rank-16 scores. Train both once under the identical early
  configuration, then score exactly one equal-rank consensus.

## 2026-08-31 02:09 SGT — early rank-16 consensus passes

- Attempts 1 and 2 trained seeds 2028 and 2029 successfully in `501.847675`
  and `473.992095` seconds. Attempt 3 scored the fixed consensus in
  `7.061831` seconds.
- Consensus validation primary is `0.6344202801780747`, a gain of
  `+0.0011232179352874`; forward is `0.6368080901076800`, a gain of
  `+0.0016633881716472` over rank-16 seed 2027.
- Every slice improved: cold/low `+0.0008733751682426`, medium
  `+0.0019711624070644`, high `+0.0003211827235818`, early dates
  `+0.0010601175553895`, and late dates `+0.0015942270433370`.
- Seed-2028 model/prediction SHA-256 values are
  `9e39438d3922c18307b46fec43e562b7e8b878e5bede60e528d5621140a7ee7b`
  and `8f142592e7a397e4684ee2085eb800d374605215c4ff6382104b85034baa387d`.
  Seed-2029 values are
  `cce90ebb5bc976c17e2f1ebd0d90f68032598d587fd30d53c521147da673c5e6`
  and `14396a80ca19017958b91dd2ba10f44d2f92591a724dab7e0dae8a7c9fd649d1`.
  Consensus prediction SHA-256 is
  `168e80be2b8e52c22d27460d746cd844c670bd6a57512e36577c94ea8d272e65`.
- Continue only with the identical missing middle and late seeds.

## 2026-08-31 02:37 SGT — middle rank-16 consensus passes

- Attempts 4 and 5 trained seeds 2028 and 2029 successfully in `793.045554`
  and `761.930888` seconds. Attempt 6 scored the fixed consensus in
  `7.318913` seconds.
- Consensus validation primary is `0.6460459543227950`, a gain of
  `+0.0015533569919579`; forward is `0.6358637232491495`, a gain of
  `+0.0006119631524623` over rank-16 seed 2027.
- Every slice improved: cold/low `+0.0014813357206498`, medium
  `+0.0016491375323215`, high `+0.0016475576806512`, early dates
  `+0.0005473956721596`, and late dates `+0.0011525861478115`.
- Seed-2028 model/prediction SHA-256 values are
  `df8950d93d96fe18764bc0565942a3fd13d359c52f7afc18fb0961900bfaac65`
  and `94ba15d32b96537b498c053f148ce6824de6aaea48c69907bf488e39b39b0c6b`.
  Seed-2029 values are
  `f2e129c21b0ceefcc965c116270dab56334c67f68f8733a3f65bdf0e6ce6f0e2`
  and `ef3d2b34e8442a922650fbfc5fb47818d7ae9f933b32c43b8cc5ec3e5d5852ff`.
  Consensus prediction SHA-256 is
  `872321deea7aa2cb6a86e54b4bd7ac313d76407380b3255ad0078777484dba3a`.
- Early and middle now both pass the aggregate and slice gates. Continue with
  the frozen late window before any official training.

## 2026-08-31 03:17 SGT — late rank-16 consensus passes; official unlocked

- Attempts 7 and 8 trained seeds 2028 and 2029 successfully in `1107.824217`
  and `1110.842764` seconds. Attempt 9 scored the fixed consensus in
  `8.977456` seconds after the required fresh strategic review.
- Consensus validation primary is `0.6433356338874292`, a gain of
  `+0.0013398750845424`; forward is `0.6437716138508182`, a gain of
  `+0.0008953698311622` over rank-16 seed 2027.
- Every slice improved: cold/low `+0.0014219722286252`, medium
  `+0.0013056647436776`, high `+0.0012973063755756`, early dates
  `+0.0010126946765360`, and late dates `+0.0007082007144432`.
- Seed-2028 model/prediction SHA-256 values are
  `afd5aae51f6cd7df496bcabcbc991744ab1717b3d010b1788d74bae6376cad7b`
  and `18a9fa2cfd6f67cb2742b8481d0665e2be17bec278c28f9050158b5deac94f2a`.
  Seed-2029 values are
  `171b8850e7b03df5601dfdb70b7498873d244d5dbe2868337ff02cbc08b7574c`
  and `81e0d03ec8a7e86bd55bda50c2b1368614c0c41325557a230a99b90beaefcba9`.
  Consensus prediction SHA-256 is
  `aed7b50d4d7996a27404e99b18551e373477bece9c4edf6cb094f6ab7b7280eb`.
- All three windows pass validation, forward, and slice gates. Train only the
  two missing official seeds, then apply the frozen stability and Run49
  promotion gates.

## 2026-08-31 04:09 SGT — official stability gate fails; no consensus scored

- Attempts 10 and 11 trained official seeds 2028 and 2029 successfully in
  `1523.712928` and `1517.983664` seconds. Peak RSS was `28,542,648,320`
  bytes.
- Seed 2028 primary is `0.6505381497088332`, or `-0.0003942855924383`
  versus seed 2027, and its worst fixed slice is high activity at
  `-0.0006945065390102`. It passes the per-seed aggregate and slice gates.
- Seed 2029 primary is `0.6501438334379509`, or `-0.0007886018633205`
  versus seed 2027. Cold/low changes `-0.0015195199439885` and late dates
  changes `-0.0010147527030016`. It fails both the `-0.0005` aggregate floor
  and `-0.001` slice floor. The three-seed primary span is
  `0.0007886018633205`, inside `0.002`, but the failed seed and slices stop the
  protocol.
- No official consensus was scored, because protocol step 3 is a prerequisite
  for step 4. Run49 remains protected at `0.6509565751074728`; Run50 is not
  promoted.
- Seed-2028 model/prediction SHA-256 values are
  `1922fc19689333179debe94d92a8438b2e8467d2cdf813f129b4b9fc0a0be81c`
  and `b1e11232f1646d92a74692805c070e2136290906d27d852204bd2ebf91ce86f4`.
  Seed-2029 values are
  `a2ddd01a3e9cda0e62e4ff6aa8b79a8bb7b9dd07a0c45e0fb4605e838a10ee23`
  and `42f5f5bd8f793c9d0d04d03b520283629e674126ce5864c4130c93d5af3af364`.
- Closing this bounded run does not stop the overall campaign. A fresh audit
  must choose the next independent hypothesis without tuning Run50 weights,
  members, or seeds from this result.
