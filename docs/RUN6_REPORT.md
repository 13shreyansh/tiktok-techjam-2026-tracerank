# Run 6 temporal-context report

Run tag: `run6-temporal-context`
Branch: `codex/run6-temporal-context`
Started: 2026-08-29 14:48 SGT
Stopped: 2026-08-29 14:56 SGT

## Outcome

Hour-of-day plus weekday improved the paired early chronological validation
parent by **0.001240134** and improved every recorded robustness slice. Its
next-window score fell by **0.000693440**, however, exceeding the predeclared
maximum forward loss of 0.0005. It is retained as a near-miss and possible
future ensemble-diversity source, not promoted.

| Candidate | Validation | Forward | Seconds | Max RSS bytes |
|---|---:|---:|---:|---:|
| Run 5 paired parent | 0.616920352 | 0.603989244 | 119.24 | -- |
| Hour + weekday | 0.618160486 | 0.603295803 | 178.76 | 3,851,730,944 |

The organizer evaluator SHA-256 remained
`ecfde28392eb14fec4f488083251df50624e1af2b86278b962daecfb42d195de`.
Exact command, outputs, metrics, trace, source hash, time, return code, and
resource reading are in `experiments/run6/ledger.jsonl`.

## Strategic conclusion

The workshop states that candidate scoring and within-user ordering are the
challenge, while final whole-list re-ranking is background and explicitly not
in scope. Run 5 already tested user-grouped listwise softmax and BPR losses;
both reduced their own pointwise checkpoints. The larger untested gap is a
causal sequence representation that distinguishes click, like, follow,
comment, forward, and negative `is_hate` feedback. Run 6 therefore converged
after one attempt rather than spending attempts on temporal bin micro-tuning.

The exact Run 2 six-seed candidate at validation primary **0.6054008850**
remains the protected fallback. Run 6 performed zero public-test evaluations.
No submission, upload, push, organizer contact, credential use, registration
change, or repository visibility change occurred.
