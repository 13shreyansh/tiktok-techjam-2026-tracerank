# Run 42 report: full-density repeat-affinity latent capacity

Run 42 closed after one successful, frozen early-shadow attempt. Doubling only
the protected repeat-affinity FM rank from 8 to 16 produced a small stable gain
but missed the predeclared materiality gate.

| Measure | Rank-8 parent | Rank 16 | Change |
|---|---:|---:|---:|
| Early primary | 0.632885873 | 0.633297062 | +0.000411189 |
| Early GAUC | 0.701268679 | 0.701247473 | -0.000021206 |
| Early nDCG@5 | 0.564503067 | 0.565346652 | +0.000843584 |
| Forward primary | 0.634753164 | 0.635144702 | +0.000391538 |
| Cold/low activity | 0.656242388 | 0.656605357 | +0.000362968 |
| Medium activity | 0.605015348 | 0.604452400 | -0.000562948 |
| High activity | 0.556729141 | 0.559744326 | +0.003015185 |

The `+0.000411189` early gain is below the frozen `+0.0005` gate, so no later
shadow, official seed, rank sweep, or learning-rate tuning followed. The
attempt took 1,013.211 seconds and peaked at 19,093,716,992 bytes RSS. The
ignored checkpoint SHA-256 is
`1d2d0b8697000cd4877f9c9eaaa4e9d2b29b7e4cd3a604e99e4643e1a69079e0`;
the ignored prediction archive SHA-256 is
`ed420a98c352bebe2ba3bfe2e462fb8cf8df5d7d73392e574e9ea55ca50aa234`.

The protected `0.6492243384881571` seed-2029 repeat-affinity checkpoint remains
unchanged. These are fixed development-sample metrics, not full-benchmark,
hidden-test, leaderboard, or submission results. No public-test labels,
upload, submission, push, organizer contact, registration change, or public
release occurred.
