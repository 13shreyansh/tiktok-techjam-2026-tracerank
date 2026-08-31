# Run 15 fresh-context strategic review — iteration 0

The protected candidate already captures broad user/video identity, item tags,
and attention over positive viewing history. Most later families failed because
they added broad low-specificity signals or optimized one time window. The
current model still lacks a direct, strictly causal memory of whether this exact
user saw this exact video before and what happened.

This is independent of category, caption, temporal, multi-action sequence,
pairwise-loss, and rank-consensus experiments. It has plausible upside because
the official submission notes that `(user_id, video_id)` is not unique. It also
has a crisp falsification test: if exact-pair memory cannot improve at least two
chronological validation/forward pairs materially, it is not worth official
seed compute or validation exposure.

Decision: run the single predeclared causal repeat-memory family. Do not branch
into feature ablations or smoothing sweeps.

