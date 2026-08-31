# Strategic review 001 — temporal context result

## Result

Attempt 1 improved early validation from 0.616920352 to 0.618160486 and all
five robustness slices, but its forward score fell from 0.603989244 to
0.603295803. The 0.000693440 loss exceeds the 0.0005 safety limit. The
configuration is a near-miss, not a promotable candidate.

## Long-horizon check

Raw dates were never used, but even recurring weekday context can exploit the
particular early window. The hidden period may have a different weekday or
traffic mix. Selecting this result after observing a single-window gain would
increase validation-overfit risk. Its broad slice gains make it worth retaining
as evidence or later ensemble diversity, not worth time-feature micro-tuning.

## Organizer-clue coverage

- The current parent already uses target-aware attention over the user's last
  20 positive long-view videos and tags.
- Causal behavior-rate features included long view, click, like, follow, and
  comment but did not beat the parent.
- Latest click and strong-engagement context was positive but below the
  robustness gate.
- Watch-ratio and click auxiliary objectives did not improve robust selection.
- User-grouped listwise softmax and BPR ranking fine-tuning were implemented and
  tested; both reduced their own pointwise checkpoints.
- The current parent still lacks a causal sequence representation that keeps
  action type and negative feedback. `is_hate` is present in the official data
  but is not currently materialized.

## Autoresearch application

Karpathy autoresearch is used as the research-loop design, not as runnable
model code: fixed evaluator, bounded candidate file, predeclared timeouts,
one hypothesis per attempt, immutable keep/discard records, resource logging,
and autonomous continuation. Its included GPT workload and H100-only training
script do not operate on KuaiRand and cannot legitimately replace the Track 2
model. Robust chronological windows and promotion gates are added because pure
single-validation hill climbing would be unsafe for this drifting dataset.

## Decision

End the temporal family. Open a new independent campaign for multi-behavior
causal histories, including explicit negative feedback, while retaining the
official `long_view` target and keeping public-test labels locked.
