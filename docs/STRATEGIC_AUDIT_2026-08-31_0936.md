# Strategic audit — 2026-08-31 09:36 SGT

## Evidence after Run69

The entire-space click funnel produced large negative transfer, so click-target
objectives close. The best unretired positive historical clue is recurring
time context. Run6's hour-plus-weekday member improved its earlier Pure parent
`+0.001240134` on early validation and every fixed slice, but forward regressed
`-0.000693440`. Run8 later found that an equal parent/time blend improved all
three chronological windows and forward windows, yet its official ensemble was
`-0.000194305` below the then-protected fallback. It was correctly rejected.

That result does not establish the effect on the current 27K model. Run52 uses
full-density training, causal item history, causal user history, exact
user-video/user-author repeat affinity, and rank 32. The time fields can now
interact with this materially different representation.

## Run70 decision

Add exactly the prior recurring fields—Asia/Shanghai hour of day and weekday—to
the protected Run52 FM. They enter as categorical interaction fields. Do not
add raw date, day index, recency decay, alternative timezone, cyclic encoding,
or bins. The cached epoch timestamp conversion is verified against official
`hourmin` examples; 67 tests pass.

## Risks and third-person check

Earlier official evidence was negative and calendar/traffic composition can
drift. The candidate therefore starts on early seed 2027 and must improve both
validation and the forward window with component and slice safety before any
later window. Even a shadow pass requires three official seeds and an unchanged
consensus gate. Run52 remains untouched.

An independent reviewer would allow this single revisit because the prior
signal transferred across all shadow windows, the parent and dataset changed
materially, and the fields are frozen before scoring. A failure closes temporal
context on Run52; no time-feature search follows.
