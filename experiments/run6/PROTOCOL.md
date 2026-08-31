# Run 6 temporal-context protocol

Run tag: `run6-temporal-context`
Branch: `codex/run6-temporal-context`
Started: 2026-08-29 14:48 SGT

## Objective

Test whether hour-of-day and weekday context improve causal user-level ranking
and temporal robustness. The organizer explicitly identifies time features and
train/test drift as unexplored headroom; the selected neural parent currently
uses neither hour nor weekday.

## Evaluation and promotion

- Compare one coherent temporal feature set with Run 5's fresh early parent.
- Promote only with at least +0.001 validation primary, no forward loss beyond
  0.0005, and no material activity/date regression.
- A promoted design must pass middle and late windows and official seeds 2026,
  2027, and 2028 before entering an ensemble.
- Treat smaller gains as noise unless independently useful in an ensemble.
- Keep the public standard test locked and preserve the exact Run 2 fallback.

## Limits and stopping

Count every attempt up to 50, stop within six hours, enforce a ten-minute
subprocess timeout, and write a fresh strategic review after each family or
eight attempts. Stop after three temporal configurations fail to improve by
more than 0.002. No submission, upload, push, organizer contact, credential use,
registration change, or repository visibility change is allowed.
