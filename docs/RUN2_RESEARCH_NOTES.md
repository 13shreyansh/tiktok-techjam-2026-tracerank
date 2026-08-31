# Run 2 research notes

## Autonomous-search design

Karpathy autoresearch contributes the fixed evaluator, one-change experiment,
immutable keep/discard record, bounded runtime, and autonomous continuation
pattern. AIDE contributes an explicit parent/child experiment tree and separate
debug versus improvement branches. Run 2 adopts those mechanics but does not
copy their task-specific model code.

The important added safeguard is robustness selection. Pure hill-climbing on
one public validation number can overfit that split. Run 2 therefore requires
chronological inner validation, segment checks, and seed replication before a
candidate is promoted.

## Primary-source directions

- KuaiRand was released specifically with random exposures, sequential history,
  twelve feedback signals, and rich user/item features; its paper identifies
  debiasing, long sequential modeling, and multi-task learning as intended uses.
- DIN uses target-aware attention over behavior history rather than compressing
  every user's interests into one fixed vector.
- DIEN adds explicitly evolving interests and auxiliary supervision at sequence
  steps. This is more complex and should follow a verified causal DIN baseline.
- Industrial video-ranking papers support multi-objective learning, while also
  warning that task relationships and training stability matter. Auxiliary
  tasks must therefore be ablated and cannot automatically be assumed helpful.

Sources inspected:

- KuaiRand: <https://arxiv.org/abs/2208.08696>
- Deep Interest Network (DIN): <https://arxiv.org/abs/1706.06978>
- Deep Interest Evolution Network (DIEN): <https://arxiv.org/abs/1809.03672>
- Google, *Recommending What Video to Watch Next*:
  <https://research.google/pubs/recommending-what-video-to-watch-next-a-multitask-ranking-system/>
- Google, *Improving Training Stability for Multitask Ranking Models*:
  <https://research.google/pubs/improving-training-stability-for-multitask-ranking-models-in-recommender-systems/>
- Karpathy autoresearch and AIDE snapshot provenance:
  `docs/AUTONOMOUS_RESEARCH_PROVENANCE.md`.

## First audit finding

The standard KuaiRand CSV files are not globally chronological and users return
in multiple blocks. A direct file-order history construction observed 23,938
within-user time reversals in the training file. Run 1's validation history was
still restricted to training-period labels, but some training examples could
see later training interactions. Run 2 treats causal history construction as
the first correctness experiment before increasing model complexity.
