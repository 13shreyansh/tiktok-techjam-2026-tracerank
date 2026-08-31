# Run 76 decision journal

## 2026-08-31 12:22 SGT — list-ranking tree frozen

- Run75 decisively rejected cosine geometry from frozen FM video rows.
- LambdaMART is a new model class on 27K and optimizes user-grouped lists using
  only low-cardinality, causal Run52 fields.
- Freeze the one standard configuration and equal parent/tree rank vote before
  any score. No tuning follows a failed first gate.
- LightGBM originally failed to import because `libomp.dylib` was absent. A
  checksum-verified Homebrew bottle was acquired under ignored `.deps/`; its
  licence, SBOM, URLs, hashes, and non-system scope are recorded. Import and a
  synthetic two-query fit passed.
- The attempted XGBoost wheel was removed immediately after it failed the same
  pre-score native import check. It produced no model, prediction, or score.
- All 76 tests, isolated-cache bytecode compilation, and diff checks passed.
- Begin with seed-2027 early only. Preserve Run52.

## 2026-08-31 12:22 SGT — construction failure, no score

- Attempt 1 stopped before model construction because one user query contained
  10,583 rows and LightGBM's compiled limit is 10,000.
- The receipt records return code 1, `15.585875` seconds, and
  `13,281,886,208` bytes RSS. No result JSON, model, prediction, or metric was
  produced.
- Add only the required deterministic compatibility adapter: preserve stable
  within-user order and partition an oversized user's rows into consecutive
  chunks of at most 10,000. Never mix users and verify exact row conservation.
- The hypothesis, features, relevance, parameters, parent, blend, gates, and
  split remain unchanged. Rerun after tests and a separate implementation
  commit.

## 2026-08-31 12:27 SGT — scored gate missed; branch closed

- Attempt 2 completed successfully in `198.295398` wrapper seconds, peaked at
  `14,816,526,336` bytes RSS, and selected boosting iteration 186.
- The fixed parent/tree rank consensus changed validation primary only
  `+0.0000588416694892`, below the `+0.0005` gate. Validation GAUC changed
  `-0.0004182642620896` and nDCG@5 `+0.0005359476010679`.
- Forward primary changed `+0.0006535903495063`, GAUC
  `-0.0001944458850165`, and nDCG@5 `+0.0015016265840292`.
- Slice deltas were cold/low `-0.0007184615913072`, medium
  `+0.0022727603006051`, high `-0.0006881855008379`, early date
  `-0.0002454797947051`, and late date `+0.0003241950257481`.
- This establishes complementary forward/nDCG signal but not a stable material
  validation gain. Stop before later windows, official training, parameter or
  blend variation, routing, or calibration. Preserve Run52 and continue the
  72-hour campaign with a different mechanism.
