# Run 62 decision journal

## 2026-08-31 08:29 SGT — high-activity fallback frozen

- Route only users above the existing training-activity upper tertile.
- Ordinary users receive exact Run61; routed users receive exact Run52.
- Begin with early only. Preserve Run52.

## 2026-08-31 08:30 SGT — construction failure, no score

- Attempt 1 returned code 1 in `0.993456` seconds with `3,226,222,592`-byte
  peak RSS.
- The existing `high_activity_last_member` implementation requires at least
  four inputs and blends the final member with three base members. Run62's
  frozen exact-fallback design correctly supplied only the already-aggregated
  Run61 base and Run52 fallback, so it raised `ValueError` before evaluation.
- No prediction output, validation score, forward score, robustness score, or
  public-test evaluation was produced.
- Close Run62 per its construction-failure stop. Any exact-fallback router fix
  and score must occur in a fresh run.
