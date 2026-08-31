# Run 84 report: clean final-test-boundary reconstruction

Run84 rebuilt the fixed six-member causal history consensus from fresh model
initializations after the 31 August FAQ confirmed that the supplied test rows
are the final judged rows. No historical checkpoint or prediction was reused.
All six model executions and the consensus reported
`official_test_outcomes_loaded: false`; the only training labels came from the
standard 8–21 April log, and validation used 22–28 April.

The six fresh member validation primaries were `0.6042517424`, `0.6044837832`,
`0.6043951511`, `0.6047577858`, `0.6046444774`, and `0.6041823626`. Every
member passed the predeclared `0.6035` floor. The fixed equal within-user-rank
consensus saved to disk re-evaluated at **GAUC 0.6725210738**, **nDCG@5
0.5382279662**, and **primary 0.6053745200**, a `+0.0037745200` validation gain
over the published `0.6016` baseline. Its worst fixed slice delta versus the
Run82 validation reference was `-0.0005331832`, inside the `-0.001` gate.

The ledger contains eight executions rather than the planned seven. An
orchestration polling race launched seed 2026 twice before either process had
updated state. Both succeeded label-blind, no result influenced any setting,
and only the hash-pinned artifact remaining at the fixed path entered the
six-distinct-seed consensus. The duplicate is preserved and disclosed in
`experiments/run84/INCIDENT_001_DUPLICATE_SEED2026.md`; it is not an ensemble
member. Run84 closed at 8/50 and under seven minutes wall-clock.

The final prediction archive SHA-256 is
`eb645924bcefc857283cbc5e819dc39b3caa041eeb12412023ba810db7764480`.
The 170,588-row, nine-significant-digit CSV SHA-256 is
`35f5fcbd718c7cdc0be10db031dd12e06909b16fd3aa2a53b070b8f006118539`.
The label-blind alignment checker passed. `scripts/verify_run84_candidate.py`
verifies all 14 artifacts, all eight ledger records, the label boundary,
validation metrics, and robustness gate. No final-test outcome was scored and
nothing was uploaded or submitted.
