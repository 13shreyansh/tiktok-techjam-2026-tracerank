# Run 4 unbiased-validation report

Run tag: `run4-exposure-debias`
Branch: `codex/run4-exposure-debias`
Started: 2026-08-29 14:25 SGT
Stopped: 2026-08-29 14:35 SGT

## Outcome

The organizer-recommended random-exposure log was integrated as an additional
validation set without training on its labels. The unchanged causal-history
parent scored **0.604725242** on standard validation and **0.388761997** on
random validation. Five uniform-random diagnostics scored 0.309854-0.311760 on
the random log; the label oracle scored 0.837328.

Three candidate families failed the random-validation promotion gate, so Run 4
stopped after four counted attempts. The exact Run 2 candidate at validation
primary **0.6054008850** remains the protected fallback.

## Attempt inventory

| Attempt | Purpose | Standard primary | Random primary | Seconds |
|---:|---|---:|---:|---:|
| 1 | unchanged parent | 0.604725242 | 0.388761997 | 49.13 |
| 2 | remove explicit FM crosses | 0.604783297 | 0.385598212 | 57.57 |
| 3 | 10% user/video embedding dropout | 0.604929268 | 0.387089133 | 105.95 |
| 4 | watch-ratio auxiliary supervision | 0.605053663 | 0.388188183 | 185.61 |

Recorded subprocess time totaled 398.26 seconds and maximum exact subprocess
RSS was 7,053,082,624 bytes. Exact commands, outputs, hashes, return codes,
times, and resource readings are preserved in `experiments/run4/ledger.jsonl`.

The random log contains 1,186,059 rows, 27,285 users, and 7,583 videos. Its
long-view rate is 0.084961 versus 0.336620 in standard training. All standard
training users and videos appear in the random log, while only 624 exact
user-video pairs overlap. Its SHA-256 is
`60b80994da969cd53da4d50c37ba3dafd6fb185df804c92c8410df34845a9d2c`.

The public standard test was evaluated zero times. No submission, upload, push,
organizer contact, credential use, registration change, or repository
visibility change occurred.
