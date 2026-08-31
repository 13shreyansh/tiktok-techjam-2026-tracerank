# Run 7 decision journal

## 2026-08-29 14:57 SGT — campaign start

- Protected fallback: Run 2 six-seed within-user rank ensemble, official
  validation primary 0.605400885.
- Paired early parent: validation 0.616920352, forward 0.603989244.
- First attempt: preserve the last-20 positive long-view videos/tags and add
  compact embeddings for the seven action bits recorded on those events.

## 2026-08-29 15:03 SGT — attempt 1 rejected

- Validation 0.615921021, down 0.000999331 from the paired parent.
- Forward 0.603857279, down 0.000131965.
- All five activity/date slices regressed, and runtime increased to 263.96 s.
- In the training log, 382,512 of 384,121 long views are also clicks. Action
  embeddings on long-view-selected events therefore add limited independent
  signal; rare actions cannot compensate.
- Continue only with the predeclared behavior-selected history. It introduces
  clicked-but-not-long-view events and explicit hate events, so it tests a
  different informational question rather than tuning attempt 1.

## 2026-08-29 15:08 SGT — attempt 2 rejected and family stopped

- Behavior-selected history validation 0.616259575, down 0.000660777.
- Forward 0.603470147, down 0.000519097, also narrowly outside the safety gate.
- All activity/date slices remained below the paired parent; runtime was
  288.35 s with 3,805,315,072 bytes maximum RSS.
- Both predeclared variants failed. Do not tune action weights, history length,
  or individual rare actions on this window. Retain the simpler parent.
