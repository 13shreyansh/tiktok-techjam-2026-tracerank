# Fresh-context strategic audit — 2026-08-31 00:39 SGT

## What should not be continued

Runs 45-48 repeatedly found the same topic pattern: nDCG and high-activity
users improve, but aggregate gains stay below gate, GAUC weakens, and later
dates do not consistently transfer. That family is exhausted. Changing topic
buckets, routes, or ensemble weights would optimize noise rather than a new
causal question.

## Highest-value unused evidence

Run 42's rank-16 repeat-affinity member independently improved early primary
by `+0.000411189` and forward primary by `+0.000391538`, with only a
`-0.000021206` GAUC change and a positive late-date slice. It failed its
single-model `+0.0005` materiality gate, but it has a different latent capacity
from every member of the protected Run 43 three-seed rank consensus. Run 43
showed that equal within-user rank aggregation reduces seed-specific ordering
error. Whether the already-observed rank-16 ordering adds diversity to that
consensus has not been scored at full density.

Run 49 therefore asks one fixed ensemble question using existing early
archives: add exact rank-16 seed 2027 as a fourth equal rank vote to the exact
three Run 43 members. No training, labels, or score selected this membership;
the only full-density rank-16 member is fixed by prior evidence. Continue only
if both validation and forward gain `+0.0003` with slice safety. This is a
cheap, falsifiable use of demonstrated stable diversity before opening another
expensive representation family.
