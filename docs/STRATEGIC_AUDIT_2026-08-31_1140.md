# Strategic audit — 2026-08-31 11:40 SGT

## Parent-drift finding

Run72 exactly reproduced protected Run52 only after explicit legacy random
unknown-row initialization. Run60's rejected neutral initialization remained
the default afterward, so training Runs66–71 inherited it. Stored-prediction
ensemble Runs61–65 were unaffected.

The scores and ledgers remain valid candidate measurements, but causal claims
must compare the confounded candidates to exact Run60 as well as Run52. Runs66,
67, 68, and 69 remain decisively negative versus Run60, with validation losses
from `-0.0020166074` to `-0.0058847276` and worst-slice losses from
`-0.0034570677` to `-0.0079604752`. Repeating them would not be a good use of
compute. Run71 is already closed as construction-invalid, and Run72 validly
rejects exact-parent identity freezing.

## Highest-value correction

Run70 is different. Time context plus neutral unknown initialization improved
Run60 by `+0.0002059015` validation and `+0.0006832697` forward, although high
activity regressed `-0.0013046240`. Earlier Pure time context and temporal
blends also had positive chronological evidence. It is the only confounded
branch close enough to reopen.

Run73 therefore repeats exactly Run70's Asia/Shanghai hour and weekday fields
with explicit Run52 legacy initialization. No bin, timezone, date, feature,
rank, learning-rate, loss, seed, or blend changes are allowed. Standard early
stopping remains for exact comparability. Require the same validation,
forward, component, slice, and resource gates as Run70.

## Third-person goal check

Correcting a discovered parent mismatch increases winning probability and
scientific validity; blindly accepting or discarding confounded results does
not. Only the near-positive branch is retested, while decisive failures remain
closed. Run52 stays immutable, and the 1/32 sample remains local evidence rather
than hidden/full-benchmark proof.
