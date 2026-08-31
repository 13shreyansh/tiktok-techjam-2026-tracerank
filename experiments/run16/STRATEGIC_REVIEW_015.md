# Run 16 fresh-context review — attempt 15

## Did causal history advance the winning objective?

No. It was methodologically important—the workshop and official dataset both
highlight prior behavior—but this specific representation did not generalize.
Its early validation gain was smaller than the organizer epsilon, its later
forward score regressed, and its weakest activity slice became worse.

## What was learned?

- Same-timestamp impression batches are common, so row-by-row history updates
  would be a serious leakage bug. The causal builder correctly avoids it.
- Frozen user/tag rates and last-positive-tag state add some local GAUC signal,
  but their validation gain does not persist into the later window.
- More hand-tuning of history buckets would now be validation chasing. The
  entire exact family is closed without official-validation access.
- The challenge still asks for per-item scores; list-level metrics judge the
  ordering within each user. A ranking-aware loss can therefore be tested
  without turning the task into the explicitly excluded re-ranking stage.

## Next action

Preserve the causal infrastructure as a documented negative result, but return
to the stronger label-free content representation. The next independent family
may test one predeclared ranking-aware objective against the same three content
shadows. It must improve both validation and forward ordering before official
validation. Do not reuse the rejected history fields, tune pair sampling from
results, or alter the protected Pure/1K candidates.
