# Run 15 decision journal

## 2026-08-29 16:51 SGT — family selection

- Question: does this action improve the probability of winning rather than
  merely generate more experiments?
- Answer: potentially. Exact repeated-item feedback is a high-specificity
  preference signal that is absent from the causal aggregate feature keys and
  is only weakly represented by positive-history attention.
- Main failure mode: repeated pairs may be too rare, or the signal may encode
  stale exposure policy rather than preference and fail forward in time.
- Safeguard: one fixed feature set, three chronological windows, paired forward
  checks, strict convergence, no test scoring, and no tuning after observing a
  result.
- Fallback: Run 2 six-member user-rank ensemble, `0.6054008850379737` official
  validation primary.

## 2026-08-29 16:53 SGT — implementation verification

- `python -m py_compile` passed for the model and campaign wrapper.
- The first synthetic builder import failed because direct shell execution did
  not set the repository's local `libomp` runtime path required by LightGBM.
- Recovery: reran the same test with
  `DYLD_LIBRARY_PATH=.deps/libomp/22.1.8/lib`; it passed and confirmed that the
  first pair occurrence has no memory, the next occurrence sees only the first,
  and frozen evaluation state sees both prior training occurrences.
- This was an engineering unit test, not a model iteration, and it did not read
  validation or test data.

## 2026-08-29 16:55 SGT — early window failed

- Validation primary: `0.616689324`, change `-0.000169396` from the fixed
  same-seed parent.
- Forward primary: `0.603714585`, change `-0.000246167`.
- The low-activity slice improved `+0.000833879`, but high activity regressed
  `-0.002051692`; validation GAUC also decreased.
- Decision: the first window fails. Run the unchanged middle window because one
  remaining path to the required two-of-three result still exists.

## 2026-08-29 16:57 SGT — second failure and stop

- Middle validation primary: `0.611072183`, change `-0.000486851`.
- Middle forward primary: `0.589249134`, change `-0.000183344`.
- Medium activity regressed `-0.000787866`, beyond the fixed slice gate.
- The attempt ledger's human-readable parent field says
  `run8-005-parent-export-shadow-middle`; the actual unchanged parent evidence
  is Run 8 iteration 004, `004-parent-export-shadow-middle`. The metrics and
  command are unaffected; this journal preserves the metadata correction rather
  than altering the append-only ledger.
- Decision: two window failures make the required two-of-three result
  impossible. Stop after two successful attempts. Do not run late, official
  validation, seed replication, ensemble construction, or test scoring.
- Win alignment: rejecting this plausible feature protects against selecting a
  low-activity-only gain that weakens the denser users most likely to dominate
  weighted GAUC.
