# Run 16 — KuaiRand-1K bonus benchmark

Status: **search closed; 18 executed, 16 convergence-eligible, 2 excluded
post-convergence, no public-test labels evaluated**.

Run 16 is a separate, bounded benchmark run for the organizer-authorized
KuaiRand-1K bonus dataset. It does not alter the protected KuaiRand-Pure
candidate. Its cache retains only April 8–28 development rows and discards later
rows by date before accessing `long_view`.

## Reproducible data boundary

- Archive SHA-256:
  `dfaafbb5fd16e9e6d2f9a6adaa4ea25df20a14bc26a90961c136e26c00a7bb2c`.
- Stable cache-input manifest SHA-256:
  `bb3fd721eb6dd48f91d3268428f440e4fcbc10f5fff1005f2b8e07631aa6250d`.
- Historical whole-cache manifest SHA-256:
  `ed37437c8a84983b88e30af71b2cbdc12a7d58780cd3c78eeeecc557b5784354`.
  This whole-file hash is preserved as historical evidence, not as a
  reproducibility identity: that manifest included a timestamp, elapsed time,
  peak RSS, PID, and an absolute source path.
- Training: April 8–21, 5,055,984 rows.
- Validation: April 22–28, 2,524,980 rows.
- Rows after April 28 excluded: 4,132,081.
- Unchanged organizer evaluator SHA-256:
  `ecfde28392eb14fec4f488083251df50624e1af2b86278b962daecfb42d195de`.

The exact candidate-producing commit (`c85dea538dd1b71bacb644a86f83949498a07610`)
was checked out in an ignored detached worktree and its unmodified content-cache
builder was rerun. The command succeeded in 68.059 seconds with 420,118,528-byte
peak RSS, and all ten selected input arrays were byte-for-byte identical to the
corresponding arrays in the later extended cache. Per-source and per-array
hashes are authoritative in
`manifests/kuairand-1k-content-cache-inputs.json`.

## Results

| Family | Validation primary | Forward evidence | Decision |
|---|---:|---|---|
| Base sparse FM, best seed | 0.643082177 | Passed all 3 shadows | Keep only as component |
| Base fixed 3-seed rank ensemble | 0.644227425 | Seed-stable | Superseded on 1K |
| Content sparse FM, seed 2027 | 0.649990205 | Passed all 3 shadows | Retain replicate |
| Content sparse FM, seed 2026 | 0.652059461 | Passed all 3 shadows | Retain replicate |
| **Content sparse FM, seed 2028** | **0.653746753** | **Passed all 3 shadows** | **Current 1K candidate** |
| Content fixed 3-seed rank ensemble | 0.653234872 | Weaker minimum slice | Reject |
| Causal history | 0.637327703 | Forward regression | Reject |
| Same-impression pairwise | 0.635846175 | Noise-sized movement | Reject |
| Multi-tag (excluded post-convergence) | 0.640972017 | Forward regression | Reject |
| Rich metadata (excluded post-convergence) | 0.634508083 | Both gates worse | Reject |

The promoted local validation candidate reports GAUC `0.6887861493` and
nDCG@5 `0.6187073568`. Its checkpoint and validation prediction hashes are in
`manifests/kuairand-1k-candidate-artifacts.json`. The model adds exactly the
predeclared primary tag, upload type, and video type fields from the official
label-free item table to the same sparse FM. No field subset or hyperparameter
was chosen after seeing the family results.

## Robustness and caveats

The same fixed content model improved both validation and its later forward
window in all three chronological shadow splits. It improved both official
metrics and every activity slice in those screens. All three official seeds
selected epoch 4 and lie within a 0.00376 primary range.

This is not an organizer-baseline reproduction: no official KuaiRand-1K score
is published. It is also not hidden-test evidence. The bonus formula and hidden
delivery route remain unknown, logged exposure bias remains possible, and the
high-activity slice has the weakest nDCG@5. Causal history and same-impression
pairwise training both failed their first forward gate. A later literal audit
found that attempts 14–16 already satisfied the three-round epsilon convergence
stop. Attempts 17 and 18 are therefore disclosed and excluded as
post-convergence exploration; neither changed the candidate. No further model
family is admissible in Run 16.

## Label-blind packaging

The frozen seed-2028 checkpoint reconstructed all 2,524,980 saved validation
predictions bit-for-bit with maximum absolute error `0.0`. The same loading and
encoding path then generated a 4,132,081-row post-April-28 candidate CSV. A
second streaming pass verified row IDs, user IDs, video IDs, finite scores, and
exact row count while resolving and indexing no outcome column. The source file
physically contains outcome fields, but neither packaging pass used them and no
test metric was computed.

The ignored CSV is 134,388,279 bytes with SHA-256
`b3b8fa2ac501daf31608fae8875f02b14f7812dc976620ac791d16acb2d56764`.
Inference plus the alignment pass took 47.558 seconds and peaked at
1,600,421,888-byte RSS. Exact paths and hashes are in
`manifests/kuairand-1k-candidate-artifacts.json`. This establishes a local,
reconstructible package only: the CSV schema is derived from the organizer Pure
schema and the statement that 1K uses the same task because no 1K-specific
checker or submission route was published.

## Accounting snapshot

Eighteen model attempts completed successfully, using 1,578.281 recorded
subprocess seconds. Peak exact subprocess RSS is 4,022,992,896 bytes. The
campaign was 3,467.49 seconds old when attempt 18 completed. Of those attempts,
16 are convergence-eligible and 2 are excluded post-convergence exploration.
The packaging pass is not a model attempt. Search is hard-locked at the wrapper
and no submission, upload, public release, or organizer contact occurred.
