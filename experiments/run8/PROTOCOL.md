# Run 8 robust diversity ensemble protocol

Run tag: `run8-robust-diversity-ensemble`
Branch: `codex/run8-robust-diversity-ensemble`
Started: 2026-08-29 15:10 SGT

## Objective

Test whether the broadly positive but forward-fragile hour-plus-weekday model
adds complementary within-user ordering signal to the stable causal parent.
This follows the strongest prior local result: within-user rank ensembling
improved the official candidate more reliably than validation-selected seeds.

## Attempts and promotion

1. Reproduce and export the paired parent on the early window.
2. Reproduce and export hour-plus-weekday on the identical window and seed.
3. Evaluate one predeclared equal-weight within-user rank ensemble.

Require the ensemble to gain at least 0.001 over its freshly reproduced parent,
lose no more than 0.0005 forward, and avoid material activity/date regression.
Only a passing ensemble can proceed to middle/late windows and three official
seeds. Keep public-test labels locked and preserve the exact Run 2 fallback.

## Limits

Count every attempt up to 50, stop within six hours, enforce ten-minute
subprocess timeouts, and write a strategic review after the family or eight
attempts. Do not submit, upload, push, contact organizers, use credentials,
change registration, or change repository visibility.
