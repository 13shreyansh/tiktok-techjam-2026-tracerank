# Run 37 report: cross-density consensus rejected

Run 37 closed after one successful early-shadow evaluation. It converted the
exact Run 33 half-density and Run 34 full-density predictions to within-user
percentile ranks and averaged them 50/50.

| Measure | Run 34 parent | Fixed blend | Change |
|---|---:|---:|---:|
| Early validation primary | 0.629643713 | 0.628496291 | -0.001147422 |
| Forward primary | 0.632081351 | 0.632138956 | +0.000057605 |
| Cold/low activity | 0.654823026 | 0.653798993 | -0.001024033 |
| Medium activity | 0.599935175 | 0.599353855 | -0.000581320 |
| High activity | 0.548873976 | 0.545868221 | -0.003005755 |
| Early dates | 0.627207911 | 0.626225829 | -0.000982082 |
| Late dates | 0.628516454 | 0.627896394 | -0.000620061 |

The fixed gate required at least `+0.0003` on validation and forward and no
slice below `-0.0003`. It failed decisively, so no blend-weight, normalization,
member, shadow, or seed search followed. The command took 6.183 seconds with
3,358,916,608-byte peak RSS.

The protected Run 34 seed-2028 development candidate remains `0.645083464`.
This is not a hidden-test, full-benchmark, submission, or leaderboard score.
No public-test labels, hidden labels, upload, submission, push, organizer
contact, or public release occurred.
