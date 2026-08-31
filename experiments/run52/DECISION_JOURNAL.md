# Run 52 decision journal

## 2026-08-31 04:15 SGT — rank 32 and gates frozen before training

- Rank 32 is the only tested capacity; it is the exact doubling of the
  confirmed rank-16 architecture, not one point in an adaptive sweep.
- Model, data, features, optimizer, seed sequence, chronological windows,
  evaluator, and gates are fixed before the first score.
- Host physical memory is `68,719,476,736` bytes and free disk is 324 GiB.
  Preserve Run49 regardless of resource or score outcome.
- Begin with seed-2027 early only.

## 2026-08-31 04:24 SGT — early rank-32 capacity gate passes

- Attempt 1 completed successfully in `559.445640` seconds with
  `28,706,553,856`-byte peak RSS.
- Validation primary is `0.6351653390327151`, a gain of
  `+0.0018682767899277`; forward is `0.6367819403169371`, a gain of
  `+0.0016372383809043` over rank-16 seed 2027.
- Every fixed slice improved: cold/low `+0.0015503896562237`, medium
  `+0.0017336416272513`, high `+0.0032599454230763`, early dates
  `+0.0017011561177218`, and late dates `+0.0023485442501282`.
- The ignored 3,786,952,205-byte checkpoint SHA-256 is
  `a55600b5348abcf1d959576efbcbd0b7612c4d3dadd03d7cb479cbe077cdf3d8`;
  the 6,607,883-byte prediction SHA-256 is
  `8d2392915731af585177bbb79287fc391629dea2fbce9f1faab0c965db911872`.
- The immutable first receipt records campaign age `-18.616895` seconds
  because the declared `04:15:00` start was 18.616895 seconds after the actual
  command start. Correct the run state to the observed command timestamp
  `2026-08-31T04:14:41.383105+08:00`; do not alter the receipt.
- Continue unchanged to middle seed 2027.

## 2026-08-31 04:41 SGT — middle rank-32 capacity gate passes

- Attempt 2 completed successfully in `928.834008` seconds with
  `29,435,396,096`-byte peak RSS.
- Validation primary is `0.6456476792466785`, a gain of
  `+0.0011550819158414`; forward is `0.6362992984204794`, a gain of
  `+0.0010475383237922` over rank-16 seed 2027.
- Every fixed slice improved: cold/low `+0.0010432287801581`, medium
  `+0.0012251402860275`, high `+0.0013688432080785`, early dates
  `+0.0004955644066072`, and late dates `+0.0010700519210087`.
- The ignored 3,786,952,213-byte checkpoint SHA-256 is
  `8bd9a65a23e74c89f43e50dc3ef32a10fcc58d91e1bc380a7d8dd863e5f328d1`;
  the 7,653,342-byte prediction SHA-256 is
  `1ea3cfdf6a04c4bcae31db2cbf66ebfea09caab85d44ed6508b60bb47ca1c93b`.
- Early and middle now pass. Continue unchanged to late seed 2027 before
  unlocking official training.

## 2026-08-31 05:04 SGT — late safe; two-of-three shadow gate passes

- Attempt 3 completed successfully in `1383.383686` seconds with
  `31,251,513,344`-byte peak RSS.
- Validation primary is `0.6425338692342100`, a gain of
  `+0.0005381104313232`; forward is `0.6425838273568443`, a change of
  `-0.0002924166628117` versus rank-16 seed 2027.
- Late is not a full win because forward misses `+0.0003`, but it remains
  inside the `-0.0005` aggregate guard. Every slice improved: cold/low
  `+0.0003671932499747`, medium `+0.0003321843908269`, high
  `+0.0015679684747581`, early dates `+0.0004281317724209`, and late dates
  `+0.0003156119712997`.
- The ignored 3,786,952,197-byte checkpoint SHA-256 is
  `764ceef306f73541df5650991d1c1beeda3f3b59b03e8fa074b211ec374a02f5`;
  the 12,190,709-byte prediction SHA-256 is
  `468e9a1a76b5a25afab7e7ca3b3af5350320bc654a38eef8ae9e95fc5ff8fcc6`.
- Early and middle are two full wins out of three; late violates no aggregate
  or slice guard. Unlock exactly the three frozen official seeds.

## 2026-08-31 05:39 SGT — official seed 2027 improves materially

- Attempt 4 completed successfully in `2027.580731` seconds with
  `34,475,294,720`-byte peak RSS.
- Rank-32 seed-2027 primary is `0.6517384046901091`, gaining
  `+0.0008059693888377` over rank-16 seed 2027 and `+0.0007818295826363`
  over protected Run49.
- Every fixed slice improves versus rank-16 seed 2027: cold/low
  `+0.0003617947973606`, medium `+0.0014366823048756`, high
  `+0.0015878912499075`, early dates `+0.0013541963538169`, and late dates
  `+0.0009286851983035`.
- The ignored 3,786,952,173-byte checkpoint SHA-256 is
  `d7211eac5a2bc844a5e17817f9cdeb0300dbb245d47ae04c265559fe23ab379b`;
  the 8,053,077-byte prediction SHA-256 is
  `f926402bf440a2bbab13a8cdfe23bf5b782a7fe591dd4a65c4013dcd69942d80`.
- One seed is not sufficient for promotion. Continue with the already frozen
  official seed 2028; do not change any setting.

## 2026-08-31 06:10 SGT — official seed 2028 confirms capacity gain

- Attempt 5 completed successfully in `1825.066608` seconds with
  `35,119,562,752`-byte peak RSS.
- Rank-32 seed-2028 primary is `0.6515220863479626`, gaining
  `+0.0009839366391294` over rank-16 seed 2028 and `+0.0005655112404898`
  over protected Run49.
- Every fixed slice improves versus rank-16 seed 2028: cold/low
  `+0.0004947869434011`, medium `+0.0020817328853247`, high
  `+0.0011188070413111`, early dates `+0.0008691919578429`, and late dates
  `+0.0008048619147319`.
- The rank-32 seed-2027/2028 primary span is `0.0002163183421465`.
- The ignored 3,786,952,173-byte checkpoint SHA-256 is
  `43b535de81cabda52376910b0c577a18b89caaef8c23abd4ec3ebb4f3e28fa47`;
  the 8,046,969-byte prediction SHA-256 is
  `f59b1d795b6f81c77331780cb1f38e97fc3bbab03a40c52372f0773abac05ae8`.
- Continue unchanged with frozen official seed 2029.

## 2026-08-31 06:41 SGT — official seed 2029 completes the stability gate

- Attempt 6 completed successfully in `1832.340001` seconds with
  `35,985,244,160`-byte peak RSS.
- Rank-32 seed-2029 primary is `0.6514699555817938`, gaining
  `+0.0013261221438429` over rank-16 seed 2029 and `+0.0005133804743210`
  over protected Run49.
- Every fixed slice improves versus rank-16 seed 2029: cold/low
  `+0.0013465751975758`, medium `+0.0013816289810025`, high
  `+0.0010096367249613`, early dates `+0.0012577820932889`, and late dates
  `+0.0018135584729394`.
- The three-seed primary span is `0.0002684491083153`; the paired mean gain
  over the matching rank-16 seeds is `+0.0010386760572700`. All three seeds
  and every fixed slice improve, so the frozen consensus is unlocked.
- The ignored 3,786,952,173-byte checkpoint SHA-256 is
  `80d136be4dc8b6196fc1a7b799235b2e32bdbd20d6d8f3597d7f8272faec58a2`;
  the 8,052,709-byte prediction SHA-256 is
  `923d80263c61d8fbc11ed58aee4af729fc560c8a1daff96cf97907d5d8bbd85a`.

## 2026-08-31 06:42 SGT — fixed three-seed rank-32 consensus promoted

- Attempt 7 completed successfully in `10.264335` seconds with
  `5,315,805,184`-byte peak RSS. It used the predeclared equal mean of
  deterministic within-user percentile ranks for seeds 2027, 2028, and 2029.
- The fixed development-sample score is GAUC `0.7066506868398097`, nDCG@5
  `0.6003449099691580`, and primary `0.6534977984044839`.
- Versus protected Run49, gains are primary `+0.0025412232970110`, GAUC
  `+0.0018695671245460`, and nDCG@5 `+0.0032128794694759`.
- Every official robustness slice improves versus Run49: cold/low
  `+0.0018444591766053`, medium `+0.0041558441321636`, high
  `+0.0023557141149478`, early dates `+0.0021444564027909`, and late dates
  `+0.0023425318802298`.
- The ignored 6,725,014-byte consensus archive SHA-256 is
  `12e4652ef8b3636936b6bc310b500d3ad11714cfa25e3a0775c1c8e5e9696b96`.
- Promote Run52 locally and preserve Run49 as a fallback. Close this bounded
  run at seven attempts because the fixed hypothesis has converged; closing
  Run52 does not stop the 72-hour campaign or authorize a submission.
