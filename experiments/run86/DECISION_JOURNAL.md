# Run86 decision journal

## 2026-08-31 17:53 SGT — family frozen

- Training-only feedback audit shows click is dense and strongly coupled to
  long-view, while deeper actions are too sparse for the first bounded test.
- Prior fully shared auxiliary/funnel designs produced negative transfer.
- Freeze a single-layer PLE-style task-protected tower: two shared experts,
  one expert per task, task-specific gates, click loss weight `0.05`.
- First and only opening gate is paired seed 2027 on the early chronological
  shadow. Stop immediately if it misses the protocol.
- Clean Run84 primary `0.605374519999571` remains protected.

## 2026-08-31 17:57 SGT — implementation verification passed

- The reusable training-only audit read only
  `log_standard_4_08_to_4_21_pure.csv`: 1,141,112 rows, long-view rate
  `0.3366198936`, click rate `0.4634470587`, click/long-view phi
  `0.7604858188`, and `P(click | long_view)=0.9958112157`.
- Eight targeted history/label-boundary tests passed; the complete suite passed
  98/98; both edited Python files compiled; CLI discovery exposed the frozen
  `task_protected` architecture; and `git diff --check` passed.
- The extraction-layer test verifies finite dual outputs and gradients for all
  shared experts, task-specific experts, gates, and heads.
- No validation or model score was produced during implementation verification.
  Commit the exact implementation and protocol before the first counted run.

## 2026-08-31 18:04 SGT — opening gate closes the family

- The first launch is preserved as counted attempt 1. It failed before model
  construction because the sandbox hid MPS and the legacy `auto` branch tried
  to create a literal `auto` device. It produced no result, score, checkpoint,
  prediction, or label-boundary attestation.
- The exact unchanged command was retried with MPS access and succeeded as
  counted attempt 2 in `39.646280` seconds with peak RSS `3,456,827,392` bytes.
  It loaded no official-test outcomes and did not evaluate final-test labels.
- Versus the paired Run83 parent, validation primary changed only
  `+0.0001055002`, below the frozen `+0.0005` continuation gate. GAUC changed
  `-0.0000858903`, nDCG@5 `+0.0002968907`, and forward primary
  `+0.0000265837`.
- Cold/low and medium activity improved `+0.0003746420` and `+0.0002155113`,
  while high activity regressed `-0.0006931831`. All hard component and slice
  floors passed, but the materiality gate did not.
- Close Run86 after two counted executions. Do not change auxiliary weight,
  expert count, task label, optimizer, or seed; do not run later windows or an
  official ensemble. Run84 remains protected.
