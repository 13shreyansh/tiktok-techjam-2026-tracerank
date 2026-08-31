# Run 10 censored watch-time protocol

Run tag: `run10-censored-watch-time`
Branch: `codex/run10-censored-watch-time`
Started: 2026-08-29 15:47 SGT

## Objective

Test whether the organizer-recommended CWM censored watch-time objective adds
information beyond the prior naive watch-ratio auxiliary. The main long-view
BCE and inference score remain unchanged. A separate auxiliary head uses the
paper's likelihood: incomplete views are exact watch-time observations and
completed views are right-censored at video duration.

## Fixed candidate and gate

- Paired parent: Run 8 early control, 0.616858721 validation and 0.603960752
  forward, seed 2027.
- Candidate: main BCE plus CWM auxiliary weight 0.1, upstream KuaiRand
  `c_inv=40`, `sigma=2`, otherwise identical parent settings.
- Require at least +0.001 validation, no forward loss beyond 0.0005, and no
  material activity/date regression before multi-window or seed promotion.
- If this fixed candidate fails, stop CWM auxiliary search; do not tune its
  weight, cost, or sigma on the same window.

Count every attempt up to 50, stop within six hours, enforce a ten-minute
subprocess timeout, and write a fresh strategic review after the family or
eight attempts. Keep public-test labels locked and preserve the exact
0.605400885 fallback. Do not submit, upload, push, contact organizers, use
credentials, change registration, or change repository visibility.
