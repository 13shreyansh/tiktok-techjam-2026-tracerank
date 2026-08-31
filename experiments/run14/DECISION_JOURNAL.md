# Run 14 decision journal

## 2026-08-29 16:26 SGT — campaign start

- Protected fallback: official validation primary 0.605400885.
- The rule, windows, seeds, and numerical gates are fixed before any new score.
- Existing Run 8 seed-2027 archives are immutable evidence, not new attempts.
- Winning-goal check: this targets seed-specific rank errors in the exact
  successful ensemble mechanism rather than adding another fragile feature.

## 2026-08-29 16:32 SGT — early window failed

- Mean rank: 0.617463599 validation and 0.604844990 forward.
- Median rank: 0.617297647 validation and 0.604891859 forward.
- Changes were -0.000165952 validation and +0.000046870 forward. Median also
  regressed four of five activity/date slices. This window fails.

## 2026-08-29 16:37 SGT — middle window failed; campaign stopped

- Mean rank: 0.612474178 validation and 0.590173913 forward.
- Median rank: 0.612524009 validation and 0.590387874 forward.
- Changes were +0.000049831 validation and +0.000213961 forward, both below
  the required +0.0003; low-activity users changed -0.000139384.
- Two windows have failed, so the required two-of-three success is impossible.
  Stop before the late-window seeds and do not access official validation.
- Eight successful attempts used 539.56 subprocess seconds and at most
  3,898,982,400 resident bytes. Public-test labels were never evaluated.
- Preserve the exact 0.605400885 fallback; do not try trimmed means or weights.
