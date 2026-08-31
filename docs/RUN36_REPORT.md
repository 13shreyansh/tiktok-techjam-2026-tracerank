# Run 36 report: rare-identity pooling rejected

Run 36 closed after one successful, predeclared early-shadow attempt. Video
and author identities with fewer than five training observations were mapped
to learned cold buckets while the full-density Run 34 FM and all other settings
remained fixed.

| Measure | Run 34 parent | Rare-pooling result | Change |
|---|---:|---:|---:|
| Early validation primary | 0.629643713 | 0.623637038 | -0.006006675 |
| Forward primary | 0.632081351 | 0.625833278 | -0.006248074 |
| Cold/low activity | 0.654823026 | 0.650022448 | -0.004800578 |
| Medium activity | 0.599935175 | 0.591732687 | -0.008202487 |
| High activity | 0.548873976 | 0.542509074 | -0.006364902 |
| Early dates | 0.627207911 | 0.622954493 | -0.004253418 |
| Late dates | 0.628516454 | 0.622542816 | -0.005973638 |

The attempt completed in 394.885 seconds with 14,225,686,528-byte peak RSS.
It retained 1,222,255 video identities and 616,219 author identities and
selected epoch 1. The rejected checkpoint SHA-256 is
`df12273a02dbb1bd42b58a82be48b8787aeed4109b5ef03c897892c7fdaa6f89`.

The predeclared early gate required at least `+0.0005` validation, no worse
than `-0.0005` forward, and no slice below `-0.001`. Every condition failed,
so no threshold, field, or seed sweep followed. The evidence suggests even
low-frequency identities carry useful ranking signal that the shared buckets
destroyed.

The protected Run 34 seed-2028 development candidate remains `0.645083464`.
This is not a hidden-test, full-benchmark, submission, or leaderboard score.
No public-test labels, hidden labels, upload, submission, push, organizer
contact, or public release occurred.
