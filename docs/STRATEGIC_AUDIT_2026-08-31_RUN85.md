# Fresh-context strategic audit before Run85

Audit time: **2026-08-31 17:30 SGT**. This review was written before any
Run85 scored model execution.

## Does the next work advance the goal of winning?

Yes, conditionally. Run84 is a clean, reproducible six-seed candidate at
validation primary `0.605374519999571`. Capacity, learning-rate, loss,
metadata, caption, temporal, repeat-memory, and action-bit families have
already failed transfer gates. Another micro-tune would consume validation
budget without a new source of signal. A separate causal negative-history
channel is a materially different hypothesis: it represents what a user
quickly rejected while preserving the successful positive long-view channel.

## Training-only evidence

Command:

```bash
./.venv/bin/python scripts/audit_pure_history_signals.py \
  --data-dir data/KuaiRand-Pure/data --history-length 20
```

The audit reads only `log_standard_4_08_to_4_21_pure.csv`. It does not open
the validation/test log. On 1,141,112 training rows and 26,210 users:

- explicit `is_hate` occurs on only 480 rows and reaches 258 users (0.985%);
- a strict skip (`long_view=0`, `is_click=0`, watch ratio at most 5%) occurs on
  413,525 rows and reaches 24,415 users (93.151%);
- the unconditional long-view rate is `0.336619894`;
- a candidate video present in the causal last-20 strict-skip history has a
  later long-view rate `0.214188085` across 29,997 matches;
- a candidate tag present only in strict-skip history has later long-view rate
  `0.224999152` across 176,894 matches;
- positive-history video and tag matches remain strongly positive, so replacing
  or merging the positive history would discard useful information.

One exploratory inline audit first failed with `TypeError: 'NoneType' object is
not callable` because an unfinished `under_2s` criterion remained in the local
dictionary. It produced no statistics or model score, was corrected, and is
disclosed here rather than erased. The preserved script above is the clean,
reproducible audit.

## Decision and risks

Freeze one family: dual-history sequence-NFM. The positive channel remains
exactly the last 20 causal long views. The new channel independently stores the
last 20 strict skips and applies candidate-aware attention over their video and
tag embeddings. It contributes its profile, candidate-profile product, and
absolute difference to the nonlinear head. It does not enter the FM term, so
the model is not forced to treat rejected similarity as attraction.

Main risks are exposure bias (a short watch is not always dislike), shared
embedding interference, and window-specific behavior drift. These are handled
by a strict 5% threshold fixed from training-only evidence, a paired seed gate,
three chronological windows, component/slice floors, and three independent
official seeds. If the first paired shadow attempt misses the declared gate,
the family closes without threshold, length, weight, seed, or architecture
tuning.
