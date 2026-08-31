# Run 71 report: identity-freeze test invalidated by parent drift

Run71 intended to reproduce exact Run52 through epoch 1, then freeze raw user,
video, and author rows while lower-cardinality context and causal histories
continued learning. All 70 tests and isolated-cache bytecode compilation
passed, but those tests did not yet include exact protected-parent reproduction.

The one counted attempt completed successfully, but epoch 1 scored
`0.6347827300641647` rather than Run52's `0.6351653390327151`. Its validation,
forward, and prediction archive exactly match rejected Run60, including
prediction SHA-256
`91976e932b79719f0d51344740868d9016b0fed0945205defbf820455cbd5d8c`.
Run60's corrected zero initialization of unknown embedding rows remained the
default after rejection, so Run71 did not reproduce its declared parent.

Frozen-identity epochs 2–5 deteriorated more slowly than Run60's fully updated
epochs but never exceeded epoch 1. This observation cannot answer the frozen
Run71 question on exact Run52. The attempt took `684.152659` seconds, peaked at
`26,781,106,176` bytes RSS, and produced an ignored 3,786,952,557-byte
checkpoint with SHA-256
`a10b60f3092f74a9b41be313e0c3e33b2359a9de64251d7025e8e4507df62ce5`.

Run71 closes as construction-invalid after one counted attempt. No promotion,
later window, official seed, hidden/public-test evaluation, submission, or
external action occurred. Run52 remains protected at local primary
`0.6534977984044839`. A corrected fresh run must explicitly restore legacy
Run52 unknown-row initialization before testing the identity-freeze hypothesis.
