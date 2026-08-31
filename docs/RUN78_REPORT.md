# Run 78 report: creator-and-tag DIN residual rejected

Run78 extended candidate-aware 27K history from Run77's 69 coarse tags to
aligned recent positive creator and tag identities. A new causal author archive
contained 207,446,146 × 5 int32 entries, zero timestamp inversions, and SHA-256
`d3c563e5d1f70fcde871e01c0d7185979141804d541a2391714f3a30bc140ec7`.
It built in `43.692960` seconds at `14,940,323,840` bytes RSS. Epoch-zero
predictions matched exact Run52 with maximum absolute error `0.0`.

The first trained epoch scored primary `0.6338891192837905`, GAUC
`0.7016143165310398`, and nDCG@5 `0.5661639220365414`. Versus exact Run52,
these are `-0.0012762197489246`, `-0.0012844118567609`, and
`-0.0012680276410882`. Patience one stopped training and restored epoch zero.
Final validation `0.6351653390327151`, forward `0.6367819403169371`, and all
established slices therefore equal the exact parent.

The counted command took `188.255151` wrapper seconds and peaked at
`24,688,721,920` bytes RSS. The ignored 208,781,967-byte rollback model
SHA-256 is
`53b470ba27e328d6202b291e9ccaaad284f58803b3b9ae8aa9c7b455cf22dd17`.
The ignored 6,607,883-byte final prediction is byte-identical to its parent,
SHA-256
`8d2392915731af585177bbb79287fc391629dea2fbce9f1faab0c965db911872`.

No later archive, seed, exact-video attention, width, history length, action,
optimizer, blend, public-test label, submission, or external action followed.
Run52 remains protected at local official-sample primary
`0.6534977984044839`. Two distinct first-gate failures close recent positive-
history DIN on 27K; the 72-hour campaign continues with a fresh mechanism.
These are deterministic 1/32 development-sample results, not hidden-test,
full-benchmark, submission, or leaderboard results.
