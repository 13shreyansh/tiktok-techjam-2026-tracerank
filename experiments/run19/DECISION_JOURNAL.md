# Run 19 decision journal

## 2026-08-29 20:35 SGT — within-user ranking family opened

- Run 16's same-impression BPR objective was narrower than the actual evaluator,
  which groups all validation candidates by user.
- Run 19 keeps the proven content representation and changes only the ranking
  comparison population to a user's full training history.
- This autonomous transition follows the user's continuing objective and the
  failed Run 18 architecture gate; no additional human model choice occurred.
- Protected fallback remains Run 16 seed 2028 at `0.6537467530366082`.

## 2026-08-29 20:37 SGT — mixed result failed gate; family closed

- Command succeeded in 67.434 seconds with 3,964,895,232-byte peak RSS.
- One fixed BPR epoch used 377,382 pairs from 944 usable training users.
- Validation changed from `0.636106651` to `0.635773882`
  (`-0.000332769`), while forward changed from `0.641647569` to
  `0.642856239` (`+0.001208670`).
- Medium-activity validation changed from `0.618670000` to `0.616692189`
  (`-0.001977811`), breaching the fixed slice guard.
- Decision: reject and close Run 19. The positive forward signal is retained as
  evidence for future independent ranking families, but pair sampling, rate,
  cap, and epoch count are not tuned from this score.
