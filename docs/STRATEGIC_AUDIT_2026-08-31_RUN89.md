# Strategic audit: Run89 causal self-attentive history encoder

## Evidence and gap

Run88 confirmed that another aggregation rule is unlikely to unlock the current
Pure ensemble: majority pairwise voting slightly regressed both tested
validation windows. The protected representation still uses order-agnostic
candidate-to-history dot attention. Run2 tested a GRU and DIN attention, but no
self-attention encoder over the ordered positive-event sequence exists in the
Pure history.

Kang and McAuley's SASRec paper motivates causal self-attention as a middle
ground between short-memory Markov models and recurrent long-term models. Use
that mechanism only as a concept; no upstream implementation is copied. The
challenge differs from next-item retrieval, so retain the exact candidate-aware
ranker and add one small causal encoder before its existing dot attention.

Primary source: https://arxiv.org/abs/1808.09781

## Frozen hypothesis

Use the exact Run83 causal sequence-NFM with history length 20, embedding width
16, and all other settings unchanged. Replace the `none` sequence encoder with
one causal Transformer encoder layer: four heads, feed-forward width 64, GELU,
dropout 0.2, learned positions, and padding masks. The encoded events still feed
the existing candidate-conditioned dot attention and neural-FM head.

## Third-person goal check

This is a genuinely independent temporal representation, not a loss, blend, or
validation correction. It directly targets the unresolved possibility that
the order and interaction of recent positive events matter. Begin with only
seed 2027 on the early chronological window. Require a material validation gain
and nonnegative forward transfer before spending two more seeds. If it fails,
close without changing layer count, head count, width, position scheme, history
length, optimizer, loss, or seed.
