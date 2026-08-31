# Run 38 decision journal

## 2026-08-30 07:17 SGT — independent repeat-affinity family opened

- Run 37 rejected cross-density consensus and is closed. Run 34 seed 2028 at
  `0.645083464` remains protected; the overall campaign continues.
- Existing user history covers total activity, strong/hate counts, current-tag
  count/rate, and last positive tag. Existing item history covers global
  video/author count/rate. Their intersection—this user's history with this
  author/video—is absent.
- Repeated creator affinity is a direct operationalization of the workshop clue
  that a person's history matters, while staying pointwise at inference as the
  organizers specified. Exact-video repeat history is included in the same
  fixed family because both identities are already core Run 34 fields.
- Implement one causal builder and four bounded fields. Test simultaneous-time
  isolation and cutoff freezing before any score. No post-result feature or
  smoothing choices.

## 2026-08-30 07:37 SGT — early causal feature build verified

- The full-row builder completed successfully in 1,166.613 seconds with
  7,850,917,888-byte peak RSS. It wrote all 207,446,146 rows and verified four
  monotonic source-user segments.
- The ignored 1,659,569,296-byte feature archive has SHA-256
  `7059bddf2ae238130d3657088ad2c4aefb0817067a0068a6122865d93753e725`;
  builder SHA-256 is
  `f1b24bda5bdb3e98f543baedeac21ab415708d77555cc08c13aa3d5464cb9796`.
- On fixed residue-0 early evaluation rows, prior author exposure is nonzero
  for 17.68% of training, 22.91% of validation, and 19.04% of forward rows.
  Exact-video repeat is much rarer: 1.63%, 0.38%, and 0.13%, respectively.
  This labels-blind coverage check does not change the fixed four-field family.
- Python compilation and 49 standard-library tests pass. Proceed to the first
  counted early-shadow model attempt; public test remains locked.

## 2026-08-30 07:45 SGT — early shadow passed materially

- Attempt 1 completed successfully in 421.691 seconds with
  15,493,169,152-byte peak RSS. Epoch 1 was selected.
- Validation primary is `0.6328858732963454`, `+0.0032421602740638` over the
  exact Run 34 parent. Forward is `0.6347531642745850`, `+0.0026718127814649`.
- Every fixed slice improved: cold/low `+0.001419362`, medium `+0.005080173`,
  high `+0.007855165`, early dates `+0.003133556`, and late dates
  `+0.002424311`.
- The early gate passes with substantial headroom. Preserve the exact code and
  settings; build middle and late causal features and repeat unchanged. Do not
  inspect official validation yet.

## 2026-08-30 08:06 SGT — middle feature build verified

- The unchanged middle-cutoff builder completed successfully in 1,224.811
  seconds with 7,694,450,688-byte peak RSS and all 207,446,146 rows written.
- The ignored middle archive SHA-256 is
  `692f95e3a9f5d091129c3994e1386231b2577213fb137acf7e96be5498ed89dc`.
  The manifest retains the exact early archive receipt and causal contract.
- Proceed to attempt 2 with the frozen model settings and matching Run 34
  middle parent. Public test and official validation remain locked.

## 2026-08-30 08:21 SGT — middle shadow replicated the gain

- Attempt 2 completed successfully in 932.427 seconds with
  17,466,982,400-byte peak RSS. Epoch 1 was selected unchanged.
- Validation primary is `0.6436189634056466`, `+0.0025779085225655` over Run
  34. Forward is `0.6335031947946410`, `+0.0030143147019258`.
- Every slice improved again: cold/low `+0.001237425`, medium `+0.003384228`,
  high `+0.006704538`, early dates `+0.002277409`, and late dates
  `+0.002417744`.
- Early and middle both pass. Build and test late unchanged as the final
  temporal guard; official validation remains locked until that result.

## 2026-08-30 08:41 SGT — late feature build verified

- The unchanged late-cutoff builder completed successfully in 1,157.184
  seconds with 7,693,762,560-byte peak RSS and all 207,446,146 rows written.
- The ignored late archive SHA-256 is
  `5c3791c6aff438acd1433c78b38ccdf258daeeb67f2c98209ea0787479b6fcb4`.
- Proceed to attempt 3 with the frozen model and matching Run 34 late parent.
  Official validation remains locked until this final shadow is reviewed.

## 2026-08-30 08:59 SGT — all temporal shadows passed; official gate opened

- Attempt 3 completed successfully in 1,044.123 seconds with
  21,824,651,264-byte peak RSS. Epoch 1 was selected.
- Validation primary is `0.6403109621770943`, `+0.0031189205465242` over Run
  34. Forward is `0.6407769790928279`, `+0.0031236328119908`.
- Every slice improved: cold/low `+0.002098897`, medium `+0.004190228`, high
  `+0.005089447`, early dates `+0.002638638`, and late dates `+0.003346348`.
- All three shadows improve validation, forward, and every fixed slice. Set
  `shadow_gate_passed` true, build the official-cutoff features, then run the
  predeclared seeds 2027–2029 unchanged. This opens development evaluation,
  not public-test or hidden labels.

## 2026-08-30 09:20 SGT — official feature build verified

- The official-cutoff builder completed successfully in 1,243.626 seconds
  with 7,687,471,104-byte peak RSS and all 207,446,146 rows written.
- The ignored official archive SHA-256 is
  `b67e0e2ef0f5034df06c01db2c171a875be4bd929913375fe9fbb471c2bb90c2`.
  The manifest now records all four split archives under one unchanged script
  hash and causal contract.
- Start official seed 2027 with the exact shadow-qualified configuration. Do
  not change features or training settings between seeds.

## 2026-08-30 09:52 SGT — official seed 2027 passed

- Attempt 4 completed successfully in 1,887.325 seconds with
  21,636,136,960-byte peak RSS. Epoch 1 was selected by the predeclared
  patience rule.
- Primary is `0.6485516995559275`, `+0.0039366268146272` over the exact Run 34
  seed-2027 parent. GAUC improves `+0.0025390852841227` and nDCG@5 improves
  `+0.0053341683451318`.
- Every fixed slice improves: cold/low `+0.002747213`, medium `+0.003610857`,
  high `+0.010145631`, early dates `+0.003886854`, and late dates
  `+0.002814948`.
- This is one seed, not a promotion. Run seed 2028 unchanged and keep the
  protected Run 34 candidate until the complete three-seed gate passes.

## 2026-08-30 10:24 SGT — official seed 2028 passed

- Attempt 5 completed successfully in 1,844.362 seconds with
  21,875,490,816-byte peak RSS. Epoch 1 was selected.
- Primary is `0.6490165630480562`, `+0.0039330988963173` over the exact Run 34
  seed-2028 parent. GAUC improves `+0.0022492586574292` and nDCG@5 improves
  `+0.0056169391352057`.
- Every fixed slice improves: cold/low `+0.002412985`, medium `+0.004627963`,
  high `+0.009670193`, early dates `+0.003921223`, and late dates
  `+0.003105100`.
- Direct artifact verification found model SHA-256
  `4cc674104bc7daf8163b0abe174b7bddaf75034defa1522d3f74e6035e976465`
  and prediction SHA-256
  `7ec69a8fb701948f0397aa4946f9d1c8c0b91e39a6d4704c56704795c0012327`.
  The ledger field named `model_sha256` hashes the model entrypoint source,
  not the checkpoint; retain it for ledger compatibility and use direct
  artifact hashes in the final report.
- Two official seeds pass. Run seed 2029 unchanged; promotion remains locked
  until the complete predeclared gate is evaluated.

## 2026-08-30 13:50 SGT — six-hour guard closed Run 38

- The unchanged seed-2029 command was rejected before execution because the
  Run 38 wall clock had crossed six hours. It did not consume an iteration or
  create a result.
- Close Run 38 at five successful attempts. The three temporal shadows pass,
  and the two completed official seeds have mean `0.6487841313019919`, paired
  mean gain `+0.0039348628554723`, and span `0.0004648634921287`.
- Do not promote from Run 38: its protocol requires three official seeds and
  only two completed. Run 34 remains the protected candidate.
- This run boundary does not stop the hackathon campaign. Open a separately
  disclosed confirmation run after a fresh-context audit, carry the exact
  frozen Run 38 candidate into seed 2029 without tuning, and evaluate the
  campaign-level three-seed evidence there.
