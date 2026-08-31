# Fresh-context strategic audit — 2026-08-30 23:56 SGT

## Why global averaging was the wrong test shape

Run 46's topic-diverse consensus improved the high-activity slice by
`+0.001570031` and medium activity by `+0.000473062`, but the cold slice was
flat and global forward gain only `+0.000098079`. Applying a specialist to all
users diluted its concentrated benefit. This does not justify choosing an
arbitrary route or threshold from validation.

## One causal, frozen routing question

The existing robustness protocol already defines user activity solely from
the training population and divides positive activity into tertiles. Run 47
uses that pre-existing upper-tertile boundary unchanged. Users above it receive
the four-member topic-diverse rank consensus; all other users receive the exact
three-member Run 43 consensus. The cutoff uses only training exposure counts,
is available at prediction time, and is recomputed from each window's training
population without labels.

No threshold, soft gate, weight, member, or feature search is allowed. Early
validation and its independent forward window must both improve materially
before middle or late topic artifacts are built. The routed design is a new
model-of-experts hypothesis; it is not a continuation or tuning of closed Run
46.
