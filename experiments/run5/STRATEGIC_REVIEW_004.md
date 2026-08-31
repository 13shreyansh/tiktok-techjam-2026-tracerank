# Strategic review 004 — Run 5 closeout

## Fresh evidence audit

| Configuration | Validation vs parent | Forward vs parent | Outcome |
|---|---:|---:|---|
| Listwise 5 positive / 20 negative, 2 epochs | -0.000111103 | +0.000071645 | reject |
| Listwise 3 positive / 12 negative, 1 gentle epoch | -0.000147343 | -0.000224650 | reject |
| Hard-negative BPR, top 20%, 1 epoch | +0.000009775 | -0.000029266 | reject |

The listwise implementation now completes, proving that the earlier timeout was
an engineering issue rather than evidence about score. Both listwise settings
failed to improve their own pointwise checkpoint. Hard-negative BPR also
reduced its own checkpoint from 0.616930127 to 0.616700888.

## Third-person assessment

An agent seeking to justify sunk work might tune list size, temperature, or
learning rate further. The evidence does not support that: aggressive,
gentle, listwise, random-pairwise, and hard-pairwise variants all fail. The
organizer's plausible objective-alignment clue has been tested rather than
assumed, and continuing would be validation overfitting.

## Decision

Stop Run 5 after four counted attempts and zero public-test evaluations. Keep
the efficient sampled implementation as negative evidence. Start a fresh
campaign for time/context representation: the current selected model has tab
and duration but omits hour and date, despite explicit organizer mention of
time features and train/test drift.
