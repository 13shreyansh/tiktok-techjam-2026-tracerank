# Run 28 decision journal

## 2026-08-29 23:49 SGT — fixed diversity test opened

- Rank 16 missed Run 27's model-promotion gate but improved forward primary and
  did not materially regress any slice. It may therefore be useful only if its
  ordering errors diversify the protected rank-8 model.
- One equal within-user rank blend is predeclared. No blend weight, subset,
  score normalization, or hyperparameter will be searched after the result.
- Run 24 seed 2029 at `0.630624629` remains the protected 27K sampled candidate.

## 2026-08-29 23:50 SGT — early blend passed; start-time defect disclosed

- The equal rank blend scored `0.614972885`, improving the exact rank-8 parent
  by `0.000513685`. Forward scored `0.617191586`, improving `0.000677662`.
- All five slices improved: cold/low `+0.000292094`, medium `+0.000869328`,
  high `+0.000506378`, early dates `+0.001100657`, and late dates
  `+0.000513307`. This clears the fixed ensemble gate.
- The state file was mistakenly initialized at 23:51 even though the first
  command began at 23:49:40.323426. The append-only attempt record therefore
  contains `campaign_elapsed_seconds_at_start: -79.676574`; it is preserved.
  The live state and protocol are corrected to the observed command start, and
  the 5.831-second subprocess receipt remains valid.
- Generate the unchanged rank-16 middle member, then test the same 50/50 blend.

## 2026-08-29 23:52 SGT — middle blend missed; late is decisive

- The rank-16 support member scored `0.626031551` versus rank 8
  `0.626371128` (`-0.000339577`); its forward change was `-0.000954836`.
- The fixed rank blend scored `0.626467573`, only `+0.000096446` over rank 8,
  and forward changed `-0.000141666`. This fails the required `+0.0003` on
  both periods.
- Slice changes ranged from `-0.000067853` to `+0.000278648`; there is no large
  hidden subgroup effect. With early passing and middle failing, the unchanged
  late window determines the two-of-three gate.

## 2026-08-29 23:54 SGT — late narrowly missed; family closed

- The late rank-16 support member was weaker than rank 8 by `0.000421205` on
  validation and `0.000735667` forward.
- The fixed blend improved validation by `0.000340783`, but forward improved
  only `0.000265401`, below the `+0.0003` requirement. Medium-activity primary
  also regressed `0.000413005`, beyond the `-0.0003` guard.
- Only the early window passed; middle and late failed. The two-of-three gate
  therefore rejects the ensemble. Do not score official validation, search
  blend weights, or select the high-activity improvement post hoc.
