# Run89 protocol: causal self-attentive history encoder

Declared: **2026-08-31 18:32 SGT**, before any Run89 model score.

## Frozen architecture

Parent: Run83 causal `sequence_nn`, seed 2027, `shadow_early`; validation
primary `0.6169077754020691`, forward primary `0.6040810346603394`.

Candidate changes only `--sequence-encoder none` to
`--sequence-encoder transformer`:

- history: last 20 strictly earlier positive `long_view` video/tag events;
- one causal Transformer encoder layer;
- embedding/model width 16, four heads, feed-forward width 64;
- GELU, dropout 0.2, learned absolute positions, padding mask;
- existing candidate-conditioned dot attention after the encoder;
- existing neural-FM fields/head, batch 4096, AdamW `0.0005`, weight decay
  `0.00001`, early stopping and all other settings unchanged.

No SASRec code is copied; the mechanism is implemented with the installed
PyTorch primitives. The paper is a concept reference:
https://arxiv.org/abs/1808.09781.

## Gates

1. Verify finite forward/backward behavior with padded and empty histories, the
   full test suite, compilation, and CLI discovery. Commit before scoring.
2. Run paired seed 2027 on `shadow_early`. Continue only if validation primary
   improves at least `+0.0005`, forward primary does not decline, neither
   component declines by more than `0.0005`, and no activity/date slice declines
   by more than `0.001`.
3. Only after step 2 passes, run fixed seeds 2026 and 2028 on the same window.
   Require at least two of three seed gains, positive mean validation and
   forward deltas, candidate consensus gain at least `+0.0003`, and component /
   slice floors.
4. Only then repeat the fixed three-seed consensus on middle and late windows;
   require two-of-three chronological windows before one clean official
   six-member build. Official promotion requires `+0.0003` over Run84 with no
   component regression and no slice loss beyond `0.001`.

Stop immediately at an impossible gate, convergence, 50 attempts, six campaign
hours, or any label/alignment failure. Do not tune heads, layers, widths,
positions, masking, dropout, history length, loss, optimizer, epochs, seed, or
blend after seeing a score.

Official final-test outcomes must not be loaded, evaluated, summarized, or used
for selection. No submission, upload, push, public release, organizer contact,
registration change, or visibility change is authorized.
