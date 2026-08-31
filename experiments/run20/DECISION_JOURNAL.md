# Run 20 decision journal

## 2026-08-29 20:40 SGT — causal recent-interest family opened

- Run 19 showed that user-wide comparisons transfer forward but did not improve
  the nearby window robustly. Run 20 moves the user's behavior history into the
  score representation instead of changing the loss.
- The fixed profile directly represents repeated long-view categories and the
  latest strong-positive/hate categories mentioned in the workshop.
- This is an autonomous family transition under the active goal; no new human
  model configuration or score was supplied.
- Protected fallback remains Run 16 seed 2028 at `0.6537467530366082`.

## 2026-08-29 20:41 SGT — causal profiles materialized

- The unchanged precomputation completed in 92.555 seconds with
  1,105,444,864-byte peak RSS and zero timestamp inversions in every split.
- It found the same 247,326 / 411,479 / 594,320 / 809,272 simultaneous
  multirow training batches as the earlier causal-history audit.
- Early/middle/late/official ignored profile SHA-256 values are respectively
  `93d2512047e8cac1b978bf9208f5ec4c9549b9aafa7de9f4fb4cef57cf42846d`,
  `2a2b159dd278a26fd82836c93b302b533269709ef4f1b7d5df329711cec924e8`,
  `a7b348d2d9f931a55dbcbd54bd7f08cd678a206b7a4761479a6eaa21b3125427`,
  and `881b7404406ea36f47f53f91f18ffb5d58d1ac50c3dc6b6380eec5f8829c3507`.
- The base cache manifest hash is
  `718f309372561ac3340fdebf70aacc3f441b4c19ce05303788073df73ac6acd1`.
  This was deterministic feature engineering, not a model attempt.

## 2026-08-29 20:42 SGT — first execution failed before training

- Attempt 1 exited in 5.244 seconds with 1,008,140,288-byte peak RSS and no
  validation result because the encoder declared 16 fields but wrote 19.
- Root cause: the content-field dimension condition omitted the new `sequence`
  feature-set name even though its seen-value and encoding conditions included
  it. This was an implementation defect, not evidence about the hypothesis.
- The hand-written start time was also three minutes ahead of the Git commit and
  produced an invalid negative elapsed value. The start is corrected to the
  exact opening commit minute, 20:40 SGT; the original failed ledger receipt is
  preserved.
- Recovery: add `sequence` to the dimension condition and add a real encoder
  shape/bounds regression test before rerunning the unchanged candidate.

## 2026-08-29 20:44 SGT — repaired candidate failed gate; family closed

- Attempt 2 succeeded in 54.812 seconds with 3,799,302,144-byte peak RSS.
- Validation changed from `0.636106651` to `0.633099226`
  (`-0.003007425`); forward changed from `0.641647569` to `0.640281128`
  (`-0.001366442`).
- Minimum robustness primary changed from `0.573007340` to `0.570044071`
  (`-0.002963269`).
- Decision: reject and close Run 20 after two counted executions: one failed
  before training and one valid model result. Do not tune memory length,
  behavior subset, recency buckets, rank, or learning rate from this score.
