# Run 83 strategic review after attempt 16

Reviewed: **2026-08-31 16:29 SGT**.

## Middle-window result

Attempts 9–16 repeated the frozen three paired seeds and two consensuses on
`shadow_middle`. All succeeded and no official/public/hidden labels were
evaluated.

| Measure | Source consensus | Causal consensus | Causal - source |
|---|---:|---:|---:|
| validation primary | 0.6119293705 | 0.6121450621 | +0.0002156916 |
| validation GAUC | 0.6604037445 | 0.6610186618 | +0.0006149172 |
| validation nDCG@5 | 0.5634549965 | 0.5632714625 | -0.0001835340 |
| forward primary | 0.5901305039 | 0.5899162903 | -0.0002142136 |
| forward GAUC | 0.6626167785 | 0.6623920106 | -0.0002247679 |
| forward nDCG@5 | 0.5176442293 | 0.5174405700 | -0.0002036593 |

Paired validation-primary changes at seeds 2026, 2027, and 2028 are
`+0.0008650422`, `-0.0000185966`, and `+0.0003062487`; two of three improve and
the paired mean is `+0.0003842314`. Paired forward-primary changes are
`+0.0002915859`, `-0.0002247095`, and `-0.0000795126`, with a nearly flat mean
of `-0.0000042121`.

The fixed validation-slice primary changes are: cold/low activity
`+0.0003646794`, medium activity `+0.0005563938`, high activity
`-0.0006753057`, early dates `+0.0008663623`, and late dates
`+0.0003652730`. Every slice and aggregate component stays within its frozen
floor, but the causal consensus does not improve forward primary. The middle
window therefore **fails causal selection** under the precommitted rule.

## Third-person failure analysis

- The result is not evidence that source-order leakage is desirable. It says
  only that removing it does not produce a consistent gain in this window.
- The validation improvement and forward regression have similar small scale.
  Treating the validation gain as decisive would be ordinary adaptive
  overfitting.
- Seed dispersion is directionally inconsistent on the forward period. A
  single-seed narrative would have reached the wrong conclusion.
- No floor is catastrophic, so the one-failure stop rule does not apply. With
  early pass and middle fail, the frozen two-of-three criterion makes the late
  window necessary and decisive.
- The audit cannot justify new architecture tuning. It is limited to choosing
  between two already frozen official artifacts.

## Decision

Continue unchanged to `shadow_late`. Select the Run82 all-causal official
artifact only if the late window supports causal selection without a
catastrophic floor; otherwise retain the exact Run2 mixed fallback.

Cumulative accounting: 16/50 attempts, 16 successful, 480.570 summed
command-seconds, 3,838,902,272-byte maximum RSS, and zero public-test
evaluations.
