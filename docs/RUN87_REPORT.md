# Run87 report: chronological residual ranker rejected

Run87 tested whether a small user-grouped LambdaMART model could learn stable
ordering mistakes left by the causal neural-FM ensemble. To prevent leakage,
the residual ranker trained only on out-of-time parent predictions and causal
aggregate features, stopped on a later meta window, and then faced a second,
untouched target window plus a still-later forward window. The exact protocol
and code were committed as `b8d57f5` before scoring; all 100 tests passed.

## Result

The sole counted execution completed in `77.076746` seconds with peak RSS
`6,446,383,104` bytes. No official final-test outcomes were loaded or scored.

| Evidence | Parent | Residual ranker | Delta |
|---|---:|---:|---:|
| meta primary, 15–17 April | 0.6048954350 | 0.6091704938 | +0.0042750588 |
| target GAUC, 18–21 April | 0.6670450748 | 0.6632380754 | -0.0038069995 |
| target nDCG@5, 18–21 April | 0.5187261230 | 0.5168532764 | -0.0018728466 |
| target primary, 18–21 April | 0.5928855989 | 0.5900456759 | -0.0028399230 |
| forward primary, 22–28 April | 0.6042330415 | 0.6023167555 | -0.0019162860 |
| cold/low-activity primary | 0.5906634286 | 0.5899481336 | -0.0007152950 |
| medium-activity primary | 0.6080023820 | 0.6017712334 | -0.0062311486 |
| high-activity primary | 0.5752726383 | 0.5735012581 | -0.0017713803 |

The predeclared meta gate passed, but every independent transfer check moved in
the wrong direction. This demonstrates temporal overfit: the tree learned a
useful correction for one date regime that was not stable even a few days
later. The family closed immediately, with no coefficient, tree, feature,
window, or seed tuning and no application to the official candidate.

The ignored LightGBM model is 642,283 bytes with SHA-256
`5059666c2c15cf08177710b5e5c48ebbb7fd884a9cf71d24ad88235e4dd48201`;
the ignored prediction archive is 678,820 bytes with SHA-256
`e005abeab377fafa86f1e331c386126d43391300b6008dc1c5d198da783547b0`.
Run84 remains protected at official-validation primary
`0.605374519999571`. Nothing was submitted, uploaded, pushed, or made public.
