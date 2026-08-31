# Run92 protocol: hard target-match history expert

## Frozen construction

Parent: Run83 causal seed 2027 on `shadow_early`, validation primary
`0.6169077754020691`, forward primary `0.6040810346603394`.

The candidate preserves the parent soft candidate-attended last-20 causal
long-view video/tag profile. It also selects exactly one earlier history vector:
the valid slot with the largest existing candidate-dot-history logit. That hard
profile, candidate product, and absolute difference are appended to the MLP.
The original neural FM term, optimizer, loss, and all other settings are
unchanged. Empty histories contribute zeros.

## Opening command

```text
.venv/bin/python scripts/run_pure_campaign_experiment.py \
  --campaign run92 \
  --id 001-hard-target-match-shadow-early-seed2027 \
  --family hard-target-match-history-expert \
  --parent run83-causal-seed2027-shadow-early \
  --hypothesis "A parameter-free best-matching positive-history vector can preserve a candidate-specific interest that soft pooling dilutes." \
  -- \
  --variant sequence_nn --split-mode shadow_early --evaluate-forward \
  --history-event long_view --history-tags --hard-history-expert \
  --history-length 20 --attention-mode dot \
  --embedding-dim 16 --hidden-dim 128 --dropout 0.2 \
  --nn-batch-size 4096 --nn-epochs 12 --nn-patience 4 \
  --nn-lr 0.0005 --nn-weight-decay 0.00001 --device auto --nn-fm-term \
  --seed 2027 \
  --model-out outputs/models/run92-hard-target-match-shadow-early-seed2027.pt \
  --predictions-out outputs/predictions/run92-hard-target-match-shadow-early-seed2027.npz
```

## Frozen gates

1. Unit tests must prove valid-slot argmax selection and finite zero output for
   empty histories.
2. The opening attempt must improve validation primary by at least `+0.0005`
   and forward primary must not decline.
3. Neither GAUC nor nDCG@5 may decline more than `0.0005` on validation or
   forward evaluation. No activity/date slice may decline more than `0.001`.
4. Failure closes the family without changing top-k, temperature, history
   length, dimensions, loss, seed, or blending.
5. Only a passing opening may repeat unchanged on middle and late windows. At
   least two of three windows must pass before three fixed official seeds.
   Promotion then requires `+0.0002` primary over Run84 and all component and
   slice floors.

No official final-test outcomes may be loaded. Maximum 50 counted attempts and
six hours; convergence is three consecutive improvements below `0.00005`,
subject to earlier frozen failure gates.
