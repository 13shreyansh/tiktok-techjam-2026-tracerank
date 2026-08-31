# Pure final-test label compliance audit — 31 August 2026

This is a fail-closed audit made after the official FAQ clarified that the
supplied test rows are the final judged rows and that any pipeline use of test
outcomes is disqualifying.

## Findings

- The unmodified organizer baseline reproduction scored the organizer's test
  split. That was a preparation-time reproduction of organizer-provided code,
  not selection of our judged candidate. It remains disclosed separately.
- Original Run 1 iteration 22 explicitly evaluated an early frozen candidate
  on the supplied test outcomes and recorded primary `0.5979221463`. Later
  models were not selected from that result, but the access itself is a material
  compliance incident and cannot be minimized as harmless.
- Historical Pure model code loaded every supplied test outcome into memory even
  when only predictions were requested. The Run82/Run83 candidate was selected
  only by validation and shadow-window evidence, but its prediction artifact was
  created through that overly broad loader. It is therefore quarantined from
  final submission under the strict clarified rule.
- Historical random-exposure experiments used random-log labels for development
  comparisons. The selected Run82 model did not train on the random log, but the
  new FAQ makes clear that future Pure model training may use only the standard
  8–21 April log.
- KuaiRand-1K/27K work was run as separate bonus work. No 1K/27K checkpoint is
  permitted to initialize or train the new Pure candidate.

## Remediation

1. `solution/ranker.py` now projects official test rows to feature-only records
   before any outcome field is accessed. The CLI rejects test-label evaluation.
2. `tests/test_ranker_label_boundary.py` injects deliberately unparsable test
   outcome values and proves that loading still succeeds while no outcome key
   escapes the boundary.
3. `solution/pure_submission.py` and `scripts/check_pure_submission.py` perform
   format/alignment work using only date, user ID, video ID, and score. The
   release path no longer calls the organizer checker that materializes labels.
4. A new Run84 candidate must be trained and predicted from scratch through the
   corrected path. No historical checkpoint or test prediction may be reused.
5. Final readiness must fail unless the label-boundary tests, label-blind
   alignment checker, fixed Run84 protocol, ledgers, and artifact hashes pass.

## Status

The historical incident is preserved in immutable ledgers and this audit. It is
not erased. Run82 remains a validation reference only. Run84 subsequently
produced and verified a clean replacement at validation primary `0.6053745200`;
see `docs/RUN84_REPORT.md`.
