# Unmodified FM baseline reproduction

Status: **SUCCEEDED** on 2026-08-26 SGT.

Only organizer-provided code was run. No model, feature, metric, data split, or
hyperparameter was changed. The sole command-line addition was an explicit path
to the organizer-authorized dataset.

## Environment

- macOS 26.6.2, arm64
- Apple M5 Pro, 18 logical CPUs
- 64 GiB physical memory
- Python 3.9.6
- NumPy 2.0.2
- GPU use: 0 GPU-hours; the baseline was CPU-only
- LLM use inside the baseline: 0 calls and 0 tokens

## FM command

Working directory: `organizer/kuairand-starter-kit`

```bash
/usr/bin/time -l ../../.venv/bin/python baseline.py \
  --model fm \
  --data_dir ../../data/KuaiRand-Pure/data
```

Observed split load:

```text
{'train': 1141112, 'valid': 124909, 'test': 170588} fields=['user_id', 'video_id', 'author_id', 'tab', 'dur_bucket']
```

Observed training trace:

```text
epoch  1 | loss 0.6391 | valid GAUC 0.6467 nDCG@5 0.5272 primary 0.5869 | 1.1s
epoch  2 | loss 0.5479 | valid GAUC 0.6589 nDCG@5 0.5323 primary 0.5956 | 1.0s
epoch  3 | loss 0.5129 | valid GAUC 0.6642 nDCG@5 0.5344 primary 0.5993 | 1.1s
epoch  4 | loss 0.5004 | valid GAUC 0.6642 nDCG@5 0.5346 primary 0.5994 | 1.1s
epoch  5 | loss 0.4941 | valid GAUC 0.6661 nDCG@5 0.5360 primary 0.6010 | 1.0s
epoch  6 | loss 0.4897 | valid GAUC 0.6658 nDCG@5 0.5354 primary 0.6006 | 1.1s
epoch  7 | loss 0.4859 | valid GAUC 0.6671 nDCG@5 0.5358 primary 0.6015 | 1.0s
epoch  8 | loss 0.4821 | valid GAUC 0.6665 nDCG@5 0.5359 primary 0.6012 | 1.0s
epoch  9 | loss 0.4784 | valid GAUC 0.6666 nDCG@5 0.5348 primary 0.6007 | 1.0s
epoch 10 | loss 0.4744 | valid GAUC 0.6650 nDCG@5 0.5342 primary 0.5996 | 1.0s
epoch 11 | loss 0.4705 | valid GAUC 0.6640 nDCG@5 0.5341 primary 0.5990 | 1.0s
early stop at epoch 11
```

Observed final result:

```text
=== fm (seed=0) ===
valid  GAUC 0.6671 | nDCG@5 0.5358 | primary 0.6015
test   GAUC 0.6621 | nDCG@5 0.5286 | primary 0.5953
```

Resource observations from `/usr/bin/time -l`:

- elapsed: 22.86 s
- user CPU: 17.27 s
- system CPU: 0.36 s
- maximum resident set size: 796,508,160 bytes
- peak memory footprint: 787,874,704 bytes
- swaps: 0

The command exited successfully. The observed single-seed result is near the
organizer's published five-seed reference (`valid primary 0.6016`, `test primary
0.5946`); no equality claim is made.

## Organizer example-submission check

The official generator and checker were also run without code changes:

```bash
mkdir -p ../../outputs
/usr/bin/time -l ../../.venv/bin/python submit.py \
  --make --split test \
  --data_dir ../../data/KuaiRand-Pure/data \
  ../../outputs/official-example-test.csv
../../.venv/bin/python submit.py \
  --check --split test \
  --data_dir ../../data/KuaiRand-Pure/data \
  ../../outputs/official-example-test.csv
```

Observed result:

```text
170,588 data rows written with the official FM baseline
format and alignment check passed for 170,588 rows, split=test
```

Generator resources: 17.48 s elapsed and 778,158,080 bytes maximum resident set
size. The resulting 4,606,993-byte CSV is ignored and was not submitted or
committed.
