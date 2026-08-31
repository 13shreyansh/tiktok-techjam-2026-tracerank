# Run 35 report: hard within-user ranking rejected

Run 35 closed after one successful, predeclared early-shadow attempt. Starting
from the exact Run 34 checkpoint, it paired up to five lowest-scored training
positives with highest-scored training negatives per user and applied a
conservative pairwise fine-tune.

| Measure | Run 34 parent | Hard-ranking result | Change |
|---|---:|---:|---:|
| Early validation primary | 0.629643713 | 0.629643713 | +0.000000000 |
| Forward primary | 0.632081351 | 0.632081351 | +0.000000000 |
| Selected pairwise epoch | — | none (parent restored) | — |

Pairwise epoch 1 regressed validation by `-0.000070145`; epoch 2 regressed it
by `-0.000178117`. The validation-gated rollback restored the parent before
forward and slice evaluation. Independent comparison confirmed bit-for-bit
identical valid and forward prediction arrays with maximum absolute difference
`0.0`. The predeclared `+0.0005` early-validation gate therefore failed, and no
pairwise hyperparameter or sampling sweep followed.

The attempt completed in 31.329 seconds with 18,265,079,808-byte peak RSS and
128,765 training-only pairs from 25,883 usable users. The ignored rollback
checkpoint SHA-256 is
`2f61f0a280e71f23c0f77291103cd88c106f87e30227c5a11fb6cd705a939002`;
its prediction artifact SHA-256 is
`05e587f2c646d40f17230b2ed6c1ab2a986385070c4357a463d66aac1d55d0dc`.

The protected Run 34 seed-2028 development candidate remains `0.645083464`.
This is not a hidden-test, full-benchmark, submission, or leaderboard score.
No public-test labels, hidden labels, upload, submission, push, organizer
contact, or public release occurred.
