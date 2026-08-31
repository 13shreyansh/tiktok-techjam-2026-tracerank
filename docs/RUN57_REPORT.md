# Run 57 report: combined recent sequence rejected

Run57 built the first KuaiRand-27K recent-sequence profile and appended its 11
strictly causal ordered fields to all 24 protected Run52 repeat/history fields.
This differed from the old KuaiRand-1K sequence test, which replaced the later
27K representation. Thirty-nine targeted tests passed before scoring.

The independently verified early archive has shape `(207446146, 11)`, dtype
`int16`, 4,563,815,340 bytes, and SHA-256
`c923ffff272f87b9a93b78be7ba523c6b3b059399a1079af041b15cfbfaae712`.
It records 25,695 corrected source-order inversions, zero causal inversions, and
6,626,844 same-timestamp batches. The Python build completed in `182.707748`
seconds at `23,448,190,976` bytes RSS; its outer timing utility returned 1 only
because the sandbox denied the final clock-rate query, which is disclosed.

The model attempt completed but regressed sharply: primary
`-0.0028604164125673`, GAUC `-0.0032633884162504`, nDCG@5
`-0.0024574444088842`, and forward primary `-0.0052830863275360` versus exact
Run52. Every fixed slice regressed beyond `-0.001`, with high activity worst at
`-0.0044425374937088`. The ordered categorical memories add noise or redundant
interaction burden in this FM representation.

The one counted attempt took `746.208740` subprocess seconds and peaked at
`31,684,935,680` bytes RSS. The ignored 3,787,021,709-byte checkpoint SHA-256
is `b52c94698e8e0a9e6706a3c9672a4723d722709a1dd0ab8cec88f517b2b96f06`;
the ignored 6,625,227-byte prediction SHA-256 is
`1bfba96269c497d27aeb3b22e0bfd69c2c3da4cb5988d30cef98ff6ae766a652`.

No later sequence archive, later shadow, official seed, field subset, action,
history-length, rank, or ensemble variant followed. Run52 remains protected at
local primary `0.6534977984044839`. These are fixed 1/32 development-sample
results, not the full benchmark, hidden test, submission, or leaderboard. No
public-test labels or external action occurred; the campaign continues.
