# Experiment status

Last updated: **2026-08-31 20:37 SGT**

- Protected clean KuaiRand-Pure validation candidate: **0.6053745200** primary
  (GAUC 0.6725210738, nDCG@5 0.5382279662).
- Published organizer FM validation baseline: **0.6016**; measured clean gain
  **+0.0037745200**.
- Historical Run82 validation reference: **0.6055212247**, quarantined because
  its legacy loader materialized official-test outcomes.
- Preserved Run2 mixed fallback: **0.6054008850**.
- KuaiRand-1K local validation candidate: **0.6537467530** primary
  (GAUC 0.6887861493, nDCG@5 0.6187073568). This is a separate bonus result,
  not directly comparable to Pure.
- Cumulative attempts across all immutable ledgers: **344 executed**
  (**333 succeeded, 11 failed/timed out**).
- Recorded experiment subprocess time: **77,615.202 seconds**.
- Maximum exact recorded subprocess RSS: **45,375,324,160 bytes**.
- Official final-test outcomes used for current candidate selection: **none**.
- Current protected Pure and 1K prediction packages pass their label-blind
  alignment and artifact checks.
- External submissions, uploads, pushes, and visibility changes: **none**.

The latest closed family is Run93. Seven seed-saturation subprocesses
succeeded and one pre-model automatic-device attempt failed. The user froze
model search for submission before the declared seed consensus was complete,
so Run93 produced no scored candidate, no official artifact, and no change to
the protected Run84 selection.

Every campaign has a predeclared protocol, immutable JSONL ledger, decision
journal, run state, and strategic review. No individual campaign exceeded 50
attempts or six hours. Restarted-run boundaries remain undefined, so the
candidate-producing campaign counts and the cumulative 344-execution total
must both be disclosed. Run16's two post-convergence attempts remain excluded
and disclosed.

The strongest result and reconstruction instructions are in
`docs/SOLUTION_REPORT.md` and `docs/RUN84_REPORT.md`; the submission-freeze
closure is in `docs/RUN93_REPORT.md`.
