# Run 15 protocol: strictly causal repeat-pair memory

Started: **2026-08-29 16:51 SGT**

## Win-aligned question

Can a strictly past-only memory of repeated `(user, video)` interactions add a
material and temporally stable signal that the current positive-only attention
history misses?

The public test labels remain locked. The exact Run 2 candidate at official
validation primary `0.6054008850379737` is the immutable fallback.

## Fixed hypothesis

For each training impression, derive numeric features only from earlier
training impressions of the same `(user, video)` pair. Freeze the resulting
state at the end of training when transforming validation and test. The fixed
feature set is:

- whether the pair was previously seen and `log1p` prior count;
- smoothed prior long-view, click, like, and watch-ratio rates;
- the last observed long-view, click, and like outcomes; and
- `log1p` hours since the last prior pair impression.

The candidate otherwise uses the protected parent's architecture and settings:
positive `long_view` video/tag history length 20, dot attention, 16-dimensional
embeddings, 128 hidden units, dropout 0.2, neural FM term, AdamW learning rate
0.0005, and seed 2027 for shadow screening. No repeat-feature subset, smoothing,
weight, history-length, or architecture sweep is allowed.

## Attempt order and gates

1. Run the fixed candidate on `shadow_early`, `shadow_middle`, and
   `shadow_late`, each with its paired forward window and robustness slices.
2. Reuse the immutable same-seed parent scores already recorded by Run 8; do
   not spend attempts rerunning unchanged parents.
3. Stop immediately after any two window failures. A window passes only if
   validation and forward primary both improve by at least `0.0005`, neither
   GAUC nor nDCG@5 materially regresses, and no activity slice drops by more
   than `0.0007`.
4. The family passes the three-window gate only if at least two windows pass,
   median validation gain is at least `0.002`, median forward gain is positive,
   and no window loses more than `0.0005`.
5. The organizer convergence rule is binding: if the first three consecutive
   iterations do not establish an improvement greater than epsilon `0.002`,
   close the run even if a weaker research signal exists.
6. Only after the shadow gate may seeds 2026, 2027, and 2028 run on official
   validation. All three enter one fixed equal within-user-rank ensemble with
   the protected six members; no seed cherry-picking or weight search.
7. Promote only if the final official ensemble improves the fallback by at
   least `0.0003`, neither official GAUC nor nDCG@5 decreases, all three new
   seeds are competitive, and robustness slices do not reveal a material
   regression. Otherwise preserve the fallback.

## Hard boundaries

- Maximum 50 counted attempts, including failures and timeouts.
- Maximum six hours from this campaign's start and ten minutes per subprocess.
- Fresh strategic audit after eight attempts if the run is still active.
- No `--evaluate-test`, no test-label reads, no submission, upload, push,
  organizer contact, secret use, registration change, or visibility change.
- Exact command, result, code/evaluator hashes, elapsed time, maximum RSS,
  errors, and recovery events are appended to `ledger.jsonl`.

