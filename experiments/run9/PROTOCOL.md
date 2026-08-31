# Run 9 Deep & Cross protocol

Run tag: `run9-deep-cross-network`
Branch: `codex/run9-deep-cross-network`
Started: 2026-08-29 15:40 SGT

## Objective

Test whether a two-layer DCN-V2-style full-rank cross tower learns useful
higher-order interactions among user, video, author, tag, tab, duration, and
target-aware history features beyond the parent's MLP plus FM pairwise term.

## Evaluation and stopping

- Compare with Run 8's fresh early parent at validation 0.616858721 and forward
  0.603960752 under the same seed and split.
- Change only the addition of two parallel cross layers.
- Require at least +0.001 validation, no forward loss beyond 0.0005, and no
  material activity/date regression before multi-window or seed promotion.
- If the two-layer architecture fails, stop the family; do not sweep layer
  count, rank, width, or learning rate on this window.
- Keep public-test labels locked and preserve the exact 0.605400885 fallback.

Count every attempt up to 50, stop within six hours, enforce a ten-minute
subprocess timeout, and write a strategic review after the family or eight
attempts. Do not submit, upload, push, contact organizers, use credentials,
change registration, or change repository visibility.
