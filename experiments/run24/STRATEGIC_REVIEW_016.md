# Run 24 fresh-context review — after sixteen scored iterations

## Progress that survived falsification

Label-free content/context fields improved all three shadows by more than 0.01
primary and every forward and activity slice. Strictly causal multi-behavior
history then improved all three shadows by 0.001654 to 0.003696 validation and
0.002534 to 0.003614 forward. On locked official development, history beat its
paired content parent for seeds 2027, 2028, and 2029 by 0.004202, 0.009649, and
0.002264. The best sampled-development checkpoint is history seed 2028 at
0.626141456 (GAUC 0.685625081, nDCG@5 0.566657832).

## What did not survive

Seed 2029 regressed the high-activity slice by 0.002137 even while aggregate
primary improved. The fixed three-seed rank ensemble scored 0.625972142, below
the best member, and did not improve that member's high-activity slice. It is
therefore rejected. Selecting only the two favorable seeds after seeing the
result would be post-hoc selection and is not allowed.

## Remaining structural gap

The current history model uses primary tag plus aggregate user/tag behavior,
but ignores available secondary categories, music type, visibility, aspect,
and causal item age. These are label-free current-item descriptors that may
help cold items and top-five ordering. They are a more independent hypothesis
than retuning history buckets or seeds. The 1/32 sample still makes histories
incomplete, so no result here establishes full 27K or hidden performance.

## Next gate

Test the existing `rich` label-free content encoder first against the exact
content parent on `shadow_early`, unchanged rank/optimizer/seed. Require the
same +0.001 validation, forward, and slice rules. If it passes at least two
shadows, implement one reviewed combination with causal history and test it
against the exact history parents. If rich content fails, close it immediately
and evaluate a denser/full-history construction rather than tuning field
subsets from the score. No hidden/public-test labels, upload, or submission.
