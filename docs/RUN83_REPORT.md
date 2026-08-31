# Run 83 report: paired chronology audit selects frozen all-causal Pure candidate

Run83 resolved the remaining candidate-provenance question without reopening
official model search. It compared the exact sequence-FM architecture under
legacy source-row histories and strictly chronological per-user histories on
three predeclared temporal validation/forward windows. Each window used fixed
seeds 2026–2028 and equal within-user rank consensuses. Source-order models
were diagnostic comparators only and cannot enter the package.

The early window supported causal history: consensus primary changed by
`+0.0002935404` on validation and `+0.0002778589` forward. The middle window
failed because validation improved `+0.0002156916` while forward regressed
`-0.0002142136`. The decisive late window supported causal history, with
`+0.0000093049` validation and `+0.0001408403` forward. Across every window,
all frozen component and activity/date slice floors passed. Detailed paired
seed, component, and slice evidence is preserved in the three strategic
reviews under `experiments/run83/`.

Under the precommitted two-of-three rule, Run83 selects the already frozen
Run82 six-causal artifact. Its local official-validation metrics remain GAUC
`0.6727584132959411`, nDCG@5 `0.5382840360094916`, and primary
`0.6055212246527164`, a `+0.0001203396147427` primary gain over the exact Run2
mixed fallback. The gain is small; the selection is primarily about cleaner
chronology and better transfer evidence, not a claim of a material leaderboard
jump. The Run2 artifact at `0.6054008850379737` remains preserved as fallback.

Run83 used 24 counted attempts, all successful, with 764.313 recorded command
seconds and 3,977,576,448-byte maximum RSS. It evaluated no official
validation, public-test, or hidden-test labels, changed no frozen model,
performed no adaptive member/weight/seed search, and made no upload or
submission. Hidden-test performance remains unknown.
