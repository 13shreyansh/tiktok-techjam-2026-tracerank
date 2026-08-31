# Experiment protocol

- The organizer's `evaluate.py` is immutable and its SHA-256 is recorded for
  every iteration.
- Selection uses the official validation split only. Public test labels are not
  consulted during model selection.
- Every attempted command counts, including failures. Each campaign runner
  enforces at most 50 iterations and six elapsed hours from that campaign's
  first run. The cumulative 133-execution interpretation risk is separately
  disclosed in `docs/RESOURCE_REPORT.md`.
- `experiments/ledger.jsonl` and `experiments/run*/ledger.jsonl` contain exact
  commands, hypotheses, metrics, elapsed time, peak resident memory, failures,
  and public-test access state.
- Large models and raw logs remain under ignored `outputs/`.
- Original Run 1 performed one explicit test audit on an earlier frozen model.
  Later campaign runners lock public-test labels; the protected candidate has
  not been test-scored.
