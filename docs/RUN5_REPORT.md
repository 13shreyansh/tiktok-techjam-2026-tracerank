# Run 5 sampled-listwise report

Run tag: `run5-sampled-listwise`
Branch: `codex/run5-sampled-listwise`
Started: 2026-08-29 14:35 SGT
Stopped: 2026-08-29 14:48 SGT

## Outcome

The previous unbounded listwise timeout was fixed with capped per-user samples,
but neither sampled listwise setting nor hard-negative BPR improved the paired
early-window parent by the +0.001 promotion threshold. Run 5 stopped after four
counted attempts and zero public-test evaluations. The exact Run 2 candidate at
validation primary **0.6054008850** remains the fallback.

## Attempt inventory

| Attempt | Purpose | Validation | Forward | Seconds |
|---:|---|---:|---:|---:|
| 1 | fresh parent | 0.616920352 | 0.603989244 | 119.24 |
| 2 | sampled listwise, 5 positive / 20 negative | 0.616809249 | 0.604060888 | 239.94 |
| 3 | gentle listwise, 3 positive / 12 negative | 0.616773009 | 0.603764594 | 181.95 |
| 4 | top-20% hard-negative BPR | 0.616930127 | 0.603959978 | 37.78 |

The first listwise configuration completed in 239.94 seconds instead of timing
out, but used 17,984,192,512 bytes maximum RSS. Its two listwise epochs scored
0.616766393 and 0.616428733, both below its pointwise checkpoint. The gentler
listwise epoch and hard-negative BPR update also reduced their own pointwise
checkpoints. Total recorded subprocess time was 578.90 seconds.

Exact commands, metrics, trace tails, source/evaluator hashes, elapsed time,
return codes, and resource readings are preserved in
`experiments/run5/ledger.jsonl`. No submission, upload, push, organizer contact,
credential use, registration change, or repository visibility change occurred.
