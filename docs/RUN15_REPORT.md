# Run 15 report: strictly causal repeat-pair memory

## Decision

Rejected after two successful attempts. The fixed candidate added a strictly
past-only memory of repeated `(user, video)` outcomes and time gaps to the
protected neural history architecture. It failed both the early and middle
validation/forward gates, making the required two-of-three window result
impossible. The late window, official validation, additional seeds, ensemble,
and public test were not run.

## Results

| Window | Parent valid | Candidate valid | Change | Parent forward | Candidate forward | Change |
|---|---:|---:|---:|---:|---:|---:|
| Early | 0.616858721 | 0.616689324 | -0.000169396 | 0.603960752 | 0.603714585 | -0.000246167 |
| Middle | 0.611559033 | 0.611072183 | -0.000486851 | 0.589432478 | 0.589249134 | -0.000183344 |

Early low-activity users improved by `+0.000833879`, but high activity
regressed by `-0.002051692`. In the middle window, the medium-activity slice
regressed by `-0.000787866`. The signal therefore concentrates in a subgroup
and does not improve the overall chronological ranking objective.

## Implementation and leakage boundary

For each training impression, the model received prior count, smoothed
long-view/click/like/watch rates, last outcomes, and time since the last
impression of the same user-video pair. Training features were generated in
timestamp order. Validation, forward, random, and test transforms use only the
state frozen at the end of their training split; no evaluation outcome updates
that state.

A synthetic unit test initially failed to import because direct shell execution
omitted the repository's local `libomp` path. The same test passed after setting
`DYLD_LIBRARY_PATH=.deps/libomp/22.1.8/lib` and verified past-only behavior.
This was not counted as a model iteration and read no benchmark evaluation data.

Run 15 used **2 / 50** counted attempts, both successful, totaling
**195.844 seconds** of subprocess time. Maximum recorded RSS was
**4,329,701,376 bytes**. The unchanged evaluator SHA-256 was
`ecfde28392eb14fec4f488083251df50624e1af2b86278b962daecfb42d195de`.

Attempt 2's append-only ledger records the wrong human-readable parent ID
(`run8-005...`); the parent evidence actually comes from Run 8 iteration 004.
The full command, code hash, metrics, and output are correct, and the correction
is preserved in the decision journal rather than rewriting the ledger.

No public-test evaluation, submission, upload, push, organizer contact, secret
use, registration change, or repository visibility change occurred. The exact
Run 2 fallback remains protected at official validation primary
`0.6054008850379737`.

