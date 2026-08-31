# Run 37 decision journal

## 2026-08-30 07:13 SGT — fixed cross-density consensus opened

- Run 36 failed decisively and is closed. The protected Run 34 seed-2028
  candidate remains `0.645083464`; the overall hackathon goal remains active.
- The monotonic density ladder improved every shadow and official seed from
  Run 30 through Run 34, but independent SGD and different training density
  can still produce complementary within-user ordering errors.
- Test one fixed 50/50 within-user percentile-rank blend of Run 34 and Run 33.
  Reuse saved predictions, so this directly tests error diversity without a
  new training or hyperparameter confound.
- Cross-capacity consensus was already rejected in Run 28; this is a distinct
  cross-density question. Do not search weights, choose seeds post hoc, or add
  weaker density members after seeing results.

## 2026-08-30 07:14 SGT — early gate failed; Run 37 closed

- The fixed blend scored `0.6284962912285841`, down `0.0011474217936975`
  from Run 34. Forward was `0.6321389562718065`, only `+0.0000576047786864`.
- Every fixed slice regressed: cold/low `-0.001024033`, medium
  `-0.000581320`, high `-0.003005755`, early dates `-0.000982082`, and late
  dates `-0.000620061`.
- The command succeeded in 6.183 seconds with 3,358,916,608-byte peak RSS and
  no public-test evaluation. Close after one attempt; do not test raw-score
  blending, weights, later shadows, or official seeds.
