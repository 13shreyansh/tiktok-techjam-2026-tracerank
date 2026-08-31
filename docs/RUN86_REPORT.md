# Run86 report: task-protected click extraction rejected

Run86 tested a bounded PLE-style response to prior multi-task negative transfer.
The exact causal sequence-NFM parent was given two shared nonlinear experts,
one long-view-only expert, one click-only expert, task-specific gates, and a
fixed click auxiliary-loss weight of `0.05`. Training-only analysis showed
click on 99.58% of long-view rows; all 98 tests passed and implementation commit
`ec02891` preceded scoring.

## Result

The first counted launch failed before model construction because the sandbox
hid MPS and the existing `auto` device branch attempted a literal `auto`
device. It produced no score or model. The exact unchanged retry completed on
MPS in `39.646280` seconds with peak RSS `3,456,827,392` bytes and no official
final-test outcomes loaded.

| Evidence | Run83 parent | Run86 | Delta |
|---|---:|---:|---:|
| validation GAUC | 0.6738564372 | 0.6737705469 | -0.0000858903 |
| validation nDCG@5 | 0.5599591136 | 0.5602560043 | +0.0002968907 |
| validation primary | 0.6169077754 | 0.6170132756 | +0.0001055002 |
| forward primary | 0.6040810347 | 0.6041076183 | +0.0000265837 |
| cold/low activity | 0.6274745515 | 0.6278491934 | +0.0003746420 |
| high activity | 0.5669689051 | 0.5662757220 | -0.0006931831 |

The predeclared opening gate required `+0.0005` validation primary. The task-
protected architecture improved nDCG slightly but not materially, reduced
GAUC, and remained activity-dependent. The family therefore closed after two
counted executions without expert-count, weight, label, seed, window, or blend
tuning.

The ignored checkpoint is 3,697,047 bytes with SHA-256
`38cd68850f48aa5320887526a111109000f5f28eb9622407ba0006ed94f47e78`;
the ignored prediction archive is 1,805,069 bytes with SHA-256
`44a07c570c27ecd147378708f4fb9cc1539e6e04c50183b4191b41e0a7eb78c8`.
Run84 remains protected at official-validation primary
`0.605374519999571`. Nothing was submitted, uploaded, pushed, or made public.

