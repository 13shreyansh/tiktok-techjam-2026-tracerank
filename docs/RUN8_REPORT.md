# Run 8 robust diversity ensemble report

Run tag: `run8-robust-diversity-ensemble`
Branch: `codex/run8-robust-diversity-ensemble`
Started: 2026-08-29 15:10 SGT
Stopped: 2026-08-29 15:38 SGT

## Outcome

An equal within-user rank blend of the stable parent and hour-plus-weekday model
improved all three chronological windows, their forward windows, and every
recorded robustness slice. However, the predeclared three-seed official
nine-member ensemble scored **0.605206580**, below the protected six-member
fallback at **0.605400885**. The temporal ensemble is rejected without weight
search, and the fallback remains final.

| Window | Parent validation | Blend validation | Delta | Parent forward | Blend forward | Delta |
|---|---:|---:|---:|---:|---:|---:|
| Early | 0.616858721 | 0.618297050 | +0.001438329 | 0.603960752 | 0.604082451 | +0.000121698 |
| Middle | 0.611559033 | 0.612144915 | +0.000585882 | 0.589432478 | 0.589892031 | +0.000459553 |
| Late | 0.592785835 | 0.593479373 | +0.000693538 | 0.603447437 | 0.603695803 | +0.000248366 |

Official temporal seeds 2026, 2027, and 2028 scored 0.603768229,
0.604628444, and 0.604765832. All three entered the fixed nine-member ensemble;
none was cherry-picked. The other six members were the exact raw prediction
members of the protected fallback. Equal within-user rank averaging gave the
temporal family one-third total weight.

## Accounting and boundary

Run 8 used 13 counted attempts totaling 1,400.01 subprocess seconds. Maximum
recorded RSS was 4,292,509,696 bytes. The unchanged evaluator SHA-256 was
`ecfde28392eb14fec4f488083251df50624e1af2b86278b962daecfb42d195de`.
Exact commands, results, traces, source hashes, times, return codes, and resource
readings are in `experiments/run8/ledger.jsonl`.

Test score arrays were generated without reading test labels, so a future final
candidate could have been packaged without retraining. Because official
validation failed, the Run 8 test array was not packaged as a candidate CSV.
Run 8 performed zero public-test evaluations. No submission, upload, push,
organizer contact, credential use, registration change, or repository
visibility change occurred.
