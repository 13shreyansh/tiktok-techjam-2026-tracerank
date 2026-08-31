# Run 79 decision journal

## 2026-08-31 12:53 SGT — anti-leakage residual selected

- Run76 showed positive forward and nDCG movement but missed its validation
  materiality gate. Runs77–78 rejected two recent-history attention variants.
- Do not tune those failed models and do not search Run76 blend weights.
- Test one higher-value methodological correction: train a parent on April 8–9,
  fit the tree only from the parent's out-of-fold April 10 predictions, stop on
  April 11, then transfer unchanged to exact Run52 on April 12–17.
- Build all three causal `stack_early` sidecars before scoring. The user and
  item archives completed and were hashed; the exact user-entity repeat archive
  is still building. No model attempt or score has occurred.
- Preserve Run52 and keep the public/hidden test locked.

## 2026-08-31 13:38 SGT — residual implementation verified pre-score

- Added a separate parent-aware cross-fit script and exposed only that exact
  model through the bounded campaign wrapper. It cannot select another target
  split or stack split.
- The implementation aligns every parent archive by declared row count, rejects
  nonfinite scores, groups stably by user, conserves every row across LightGBM's
  10,000-row query adapter, and adds the tree output to the parent's within-user
  rank without a searched coefficient.
- A synthetic two-model LightGBM check used a constant init score of 7.0. The
  model predictions with and without the init score differed by exactly 0.0 and
  had maximum absolute prediction 0.1949363322, confirming that `predict`
  returns only tree contributions and that the explicit parent-rank addition is
  required once, not twice.
- Bytecode compilation, diff checks, and all 86 tests passed. No score has
  occurred; continue waiting for the still-open exact user-entity sidecar.

## 2026-08-31 14:33 SGT — causal sidecars verified

- The exact user-entity builder completed successfully after `5,800.935616`
  seconds at `7,461,683,200` bytes peak RSS. Its 207,446,146 × 4 int16 archive
  is 1,659,569,296 bytes, spans four verified source-user segments, and has
  SHA-256 `b58cd665042f090ffbe6fff2798943a7f3b203e9896a99f7fd753e550a648bee`.
- Independent full-file hashes exactly matched all three finalized manifests:
  user history `d945f67a78df479135cd3d833378d7a4869a651c55c3b963649cb1909e591a72`,
  item history `87bc0dce11d28990164c8378d9ba6bc36ed17e4de1a3a5a499beb0d68e68cb8a`,
  and exact user-entity history `b58cd665042f090ffbe6fff2798943a7f3b203e9896a99f7fd753e550a648bee`.
- User history records 20,734,690 April 8–9 training rows, 186,711,456
  frozen later rows, 3,350,745 simultaneous multirow batches, and zero
  post-sort timestamp inversions despite 24,857 source inversions.
- All archives remain ignored. Run79 is still at zero counted model attempts;
  launch the frozen supporting parent next.

## 2026-08-31 14:46 SGT — attempt 1 supporting parent accepted

- The exact frozen command completed successfully in `732.640181` wrapper
  seconds at `26,810,564,608` bytes peak RSS and selected epoch 2.
- April 10 out-of-fold validation: GAUC `0.6932832789875141`, nDCG@5
  `0.5632677431131666`, primary `0.6282755110503404`, 335,961 rows and
  22,903 users. April 11 forward: GAUC `0.6900371276872465`, nDCG@5
  `0.5551514890104612`, primary `0.6225943083488539`, 297,461 rows and
  21,626 users.
- Independent checks confirmed the prediction arrays have exact declared
  lengths, float32 dtype, and all-finite values. The 3,786,952,261-byte
  checkpoint SHA-256 is
  `c4c7961cb4653f32a00b79efe9e446bb6f7a66814d140af41572101e3e6a4b6b`;
  the 2,297,577-byte prediction SHA-256 is
  `12e96b70e1aa3edee46440e079f2ad4b224b783fd73a72c61aea18c2be5ddcf1`.
- This supporting score is not a promoted candidate. It satisfies attempt 1's
  construction gate and authorizes only the already-frozen residual attempt 2.

## 2026-08-31 14:47 SGT — attempt 2 transfer gate failed; run closed

- The fixed residual selected tree iteration 26 and completed successfully in
  `18.807056` wrapper seconds at `10,225,319,936` bytes peak RSS.
- On the clean April 11 meta-validation day it improved its parent by GAUC
  `+0.0006333603463269`, nDCG@5 `+0.0017921937699596`, and primary
  `+0.0012127770581434`, so the residual learned real out-of-fold signal.
- Transfer to exact Run52 April 12–14 improved primary only
  `+0.0002593853063149`, below the frozen `+0.0003` gate. GAUC changed
  `-0.0004366293071785` and nDCG@5 `+0.0009553999198082`.
- April 15–17 forward primary changed `-0.0001132338704767`, GAUC
  `-0.0003647626589791`, and nDCG@5 `+0.0001382949180256`, failing the required
  positive forward transfer. The high-activity slice also changed
  `-0.0030788875590728`, beyond the `-0.001` safety guard. Other slice primary
  deltas were cold/low `+0.0002077312544841`, medium
  `+0.0017895503992853`, early dates `-0.0001357742362107`, and late dates
  `+0.0004318105803535`.
- Independent hashes match the result: 98,218-byte tree SHA-256
  `a79b384fa8affd2c94e754ce7f8095c30618a89692ac9bd12475203d1663547d`
  and 7,490,150-byte prediction SHA-256
  `108b6936ea8067409d82547d9d67ead4074a6d0d5580b45b4ad78fd4363c71f4`.
  Valid, forward, and meta-valid arrays have exact expected lengths and all
  finite float32 values.
- Stop without later windows, official seeds, parameters, features, blends, or
  calibration. Run76 and Run79 together show that the causal tree supplies
  nDCG signal but does not yet transfer safely across activity and time. Keep
  Run52 protected and continue the 72-hour campaign with a fresh mechanism.
