# Run84 incident 001: duplicate seed-2026 execution

The first seed-2026 command was launched through an escalated execution handle.
The polling wrapper returned an empty completion before the underlying process
had surfaced its result. A state check then showed no ledger or result, so the
same fixed command was retried. The original process was still running and both
executions completed successfully.

Consequences:

- Run84 contains **8 counted executions**, not the planned 7.
- The immutable ledger contains two entries with ID
  `001-clean-seed2026-official`, both marked iteration 1 because the two
  processes read and updated state concurrently.
- Both attest `official_test_outcomes_loaded: false`; neither accessed or scored
  final-test outcomes.
- Both wrote the same ignored checkpoint/prediction paths. The artifact that
  remained on disk and entered the fixed consensus is the hash-pinned artifact
  in `manifests/run84-candidate-artifacts.json`.
- No setting, member identity, weight, or model choice changed in response to
  either score. The duplicate is not a seventh ensemble member.
- The run remains below 50 executions and six hours, but the duplicate and
  concurrent state-write defect must be disclosed.

The run is closed immediately after the six distinct fixed members and their
fixed consensus. The duplicate is preserved; no ledger line is removed.
