# Run91 protocol: separate explicit-engagement history

## Frozen construction

Parent: Run83 causal seed 2027 on `shadow_early`, validation primary
`0.6169077754020691`, forward primary `0.6040810346603394`.

The candidate keeps the parent long-view-positive video/tag history unchanged.
It adds one independent candidate-attended history over strictly earlier
training impressions where at least one of `like`, `follow`, `comment`, or
`forward` is true. Click-only and hate events are excluded. Both histories use
the fixed length 20 and shared learned video/tag embeddings. The new profile,
candidate-product, and absolute-difference vectors are appended before the
unchanged MLP and neural FM term.

## Opening command

```text
.venv/bin/python scripts/run_pure_campaign_experiment.py \
  --campaign run91 \
  --id 001-explicit-engagement-shadow-early-seed2027 \
  --family separate-explicit-engagement-history \
  --parent run83-causal-seed2027-shadow-early \
  --hypothesis "A separately attended history of prior likes, follows, comments, and forwards can add strong-preference signal without diluting the selected long-view history." \
  -- \
  --variant sequence_nn --split-mode shadow_early --evaluate-forward \
  --history-event long_view --history-tags \
  --secondary-history-event engagement --history-length 20 \
  --attention-mode dot --embedding-dim 16 --hidden-dim 128 --dropout 0.2 \
  --nn-batch-size 4096 --nn-epochs 12 --nn-patience 4 \
  --nn-lr 0.0005 --nn-weight-decay 0.00001 --device auto --nn-fm-term \
  --seed 2027 \
  --model-out outputs/models/run91-explicit-engagement-shadow-early-seed2027.pt \
  --predictions-out outputs/predictions/run91-explicit-engagement-shadow-early-seed2027.npz
```

## Frozen gates

1. Unit tests must prove the engagement selector includes only like, follow,
   comment, or forward and excludes click-only and hate events.
2. The opening attempt must improve validation primary by at least `+0.0005`
   and forward primary must not decline.
3. Neither GAUC nor nDCG@5 may decline more than `0.0005` on validation or
   forward evaluation. No activity/date slice may decline more than `0.001`.
4. Failure closes the family without changing event membership, history
   length, dimensions, attention, loss, seed, or blending.
5. Only a passing opening attempt may proceed to the predeclared middle and
   late windows. At least two of three windows must pass before three fixed
   official seeds are permitted. Promotion then requires at least `+0.0002`
   over Run84 with no component or slice loss beyond `0.001`.

No official final-test outcomes may be loaded. Maximum 50 counted attempts and
six hours; the convergence rule is a three-attempt window with improvement
below `0.00005`, subject to the earlier frozen failure gates.
