# Run 7 multi-behavior sequence report

Run tag: `run7-multibehavior-sequence`
Branch: `codex/run7-multibehavior-sequence`
Started: 2026-08-29 14:57 SGT
Stopped: 2026-08-29 15:08 SGT

## Outcome

Two causal action-aware history designs were tested. Neither met the promotion
rule, so the family stopped without micro-tuning.

| Candidate | Validation | Forward | Seconds | Max RSS bytes |
|---|---:|---:|---:|---:|
| Paired parent | 0.616920352 | 0.603989244 | 119.24 | -- |
| Seven action bits on long-view history | 0.615921021 | 0.603857279 | 263.96 | 3,759,439,872 |
| Any-action history with action bits | 0.616259575 | 0.603470147 | 288.35 | 3,805,315,072 |

Both candidates also regressed every recorded activity/date robustness slice.
The evaluator SHA-256 remained
`ecfde28392eb14fec4f488083251df50624e1af2b86278b962daecfb42d195de`.
Exact commands, outputs, traces, source hashes, times, return codes, and resource
readings are in `experiments/run7/ledger.jsonl`.

## What was actually tested

The model stored a compact seven-bit causal action code for each history event
and decoded it into shared embeddings for long view, click, like, follow,
comment, forward, and `is_hate`. Attempt 1 preserved exactly the parent's
positive long-view event selection. Attempt 2 included any explicit action,
allowing clicked-but-not-long-view videos and explicit negative feedback into
the history.

This is separate from final-list re-ranking, which the workshop explicitly
says is not part of the challenge. Run 5 had already tested user-grouped
listwise softmax and BPR ranking losses; neither improved the pointwise parent.

The exact Run 2 six-seed candidate at official validation primary
**0.6054008850** remains the protected fallback. Run 7 performed zero
public-test evaluations. No submission, upload, push, organizer contact,
credential use, registration change, or repository visibility change occurred.
