# Run85 decision journal

## 2026-08-31 17:30 SGT — family frozen

- Goal check: this is a new candidate-aware behavioral signal, not capacity,
  seed, weight, or learning-rate micro-tuning.
- Clean protected fallback: Run84 primary `0.605374519999571`.
- First paired gate: dual-history seed 2027 on early chronological shadow
  versus Run83 causal seed 2027.
- Training-only audit supports a separate strict-skip channel; explicit hate is
  too sparse, and merging actions previously regressed in Run7.
- Stop immediately if the first attempt misses any predeclared gate.

## 2026-08-31 17:41 SGT — implementation verification

- The first targeted-test command failed before importing the project because
  `lib_lightgbm.dylib` could not locate `libomp.dylib`; no model was launched
  and this is not a counted experiment.
- Re-running with the repository-local audited runtime
  `DYLD_LIBRARY_PATH=.deps/libomp/22.1.8/lib` passed all 7 targeted tests.
- The complete test suite passed 97/97, both edited Python files compiled, CLI
  discovery exposed the frozen negative-history flag, and `git diff --check`
  passed.
- The reusable training-only audit reproduced 1,141,112 rows, 26,210 users,
  413,525 strict skips, and the declared negative future-long-view signals.
- Goal check: implementation evidence is sufficient to spend the first counted
  execution on the predeclared paired chronological gate; no parameter changed.

## 2026-08-31 17:44 SGT — first gate closes the family

- Run85-001 succeeded in 46.96 s with 3.44 GB peak RSS, used MPS, loaded no
  official-test outcomes, and did not evaluate the public final-test labels.
- Versus the paired Run83 seed-2027 parent, validation primary changed by only
  `+0.0001149774`, below the frozen `+0.0005` continuation requirement. GAUC
  changed by `-0.0000182986` while nDCG@5 changed by `+0.0002481937`.
- Forward primary improved by `+0.0004829168`, but the effect was not uniform:
  cold/low activity gained `+0.0008381046`, while high activity lost
  `-0.0008892577`. All hard component and slice floors passed.
- Decision: close the family after one counted execution. Do not run the other
  seeds, change the 5% definition, alter history length, or search a blend.
- Goal check: the negative-history signal is real but too small and
  activity-dependent to justify promotion. The clean Run84 candidate remains
  stronger evidence for final-test transfer.
