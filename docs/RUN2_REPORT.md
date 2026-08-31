# Run 2 robust-ranking report

Run tag: `run2-robust-ranking`  
Branch: `codex/run2-robust-ranking`  
Campaign start: **2026-08-29 12:56:54 SGT**  
Search convergence declared after iteration 33; iterations 34-37 were frozen
candidate reproduction and packaging only.

## Result

The selected candidate is a six-member, within-user rank ensemble. Three
members are the Run-1 video-plus-tag history seeds; three are independently
reproduced seeds using corrected chronological causal histories. Each member
scores the same rows, its scores are converted to ranks separately for each
user, and the six ranks are averaged.

| Measure | Verified value |
|---|---:|
| GAUC | 0.6723790951 |
| nDCG@5 | 0.5384226749 |
| Primary = mean(GAUC, nDCG@5) | **0.6054008850** |
| Published organizer FM primary | 0.6016 |
| Absolute gain over published FM | **+0.0038008850** |
| Prior Run-1 best single model | 0.6048465371 |
| Absolute gain over Run-1 best | **+0.0005543479** |

This is a validation result, not a hidden-test result. The public date-based
test labels were locked for all 37 Run-2 iterations and were never evaluated.
The final hidden-test score remains unknown until the organizer evaluates a
submission.

## What changed and why

The first audit found that the source CSV is neither globally chronological nor
user-contiguous: there were 23,938 within-user time reversals and 24,729 users
who returned in later file blocks. Run 1 did not leak validation labels, but a
training example could see a later training interaction. Run 2 corrected this
by sorting each user's training examples by `time_ms` and freezing only the
chronologically latest training history for validation and test.

Complexity did not reliably help. DIN attention, GRU interest evolution,
positive-and-negative histories, explicit match features, profile features,
primary-tag history, user-balanced loss, auxiliary supervision, and smoothed
target-rate buckets were rejected by chronological shadow validation or
robustness slices. A listwise fine-tune exceeded the ten-minute attempt limit.
Seven-day training recency weighting produced only tiny, seed-scale shadow
gains and did not improve the final raw-score ensemble.

The useful improvement was variance reduction aligned to the evaluator. Three
causal seeds individually scored 0.604349-0.604521 in their exploratory exports;
their raw-score ensemble scored 0.604980. Converting each model's scores to
within-user ranks raised that ensemble to 0.605222. Rank aggregation across the
three causal and three legacy seeds raised it to 0.605392, and the exact frozen
reproductions used for packaging scored **0.605401**.

## Validation safeguards

- The organizer evaluator was unchanged in every attempt; SHA-256
  `ecfde28392eb14fec4f488083251df50624e1af2b86278b962daecfb42d195de`.
- `scripts/run_experiment_v2.py` rejected `--evaluate-test`, counted failed
  launches, recorded source hashes, enforced a ten-minute subprocess timeout,
  and capped the campaign at 50 iterations and six hours.
- Model changes were screened on an inner chronological shadow split and
  inspected across early/late dates and low/medium/high user activity.
- Important candidates were replicated with seeds 2026, 2027, and 2028.
- An isolated improvement smaller than observed seed variation was not treated
  as reliable.
- Search stopped after iterations 31-33 satisfied the published three-round
  convergence threshold of no improvement greater than 0.002. Later iterations
  only reproduced and packaged the already frozen design.

## Attempt and resource accounting

- Total counted attempts: **37 / 50**.
- Successful attempts: **35**; failed/timed-out attempts: **2**.
- Recorded experiment subprocess time: **2,287.60 seconds**.
- Campaign wall time through final ensemble: **3,172.35 seconds**
  (52 minutes 52 seconds).
- Largest exact recorded subprocess RSS: **4,549,312,512 bytes**.
- The timed-out listwise attempt had no exact RSS because the wrapper was
  interrupted; Activity Monitor showed **52.6% of a 64 GB system** at 9m31s.
- Neural training used Apple MPS on an Apple M5 Pro. Ensemble and checking
  steps used CPU memory. No cloud accelerator or API key was used.
- Human interactions during Run 2: **one kickoff message**, recorded in
  `experiments/run2/human_interactions.jsonl`; it did not change an active
  experiment. All subsequent steering was produced by the same Codex agent.
- Codex usage at the final pre-commit audit was **438,007 tokens** and
  **3,403 seconds** of goal time. The authoritative final counter is reported
  by the goal closeout after the commit because it continues during packaging.

The full immutable attempt record, including exact commands, timestamps,
return codes, metrics, hashes, output tails, and measured memory, is
`experiments/run2/ledger.jsonl`.

## Final local artifacts

Large generated artifacts remain ignored and are not committed.

| Artifact | Size | SHA-256 |
|---|---:|---|
| `outputs/predictions/run2-final-six-seed-user-rank.npz` | 476 KiB | `2f4f7e87717a6c4edc3334106a8baa4daf98d41eff99d910aa06cad1c14f91e1` |
| `outputs/submissions/run2-final-six-seed-user-rank-test.csv` | 4.0 MiB | `dad092c33f405ecd55b81e3fd4f5ed07816d56e622ffa065857d49a4abfc6c79` |

The CSV contains one header plus 170,588 data rows. This command succeeded:

```text
.venv/bin/python organizer/kuairand-starter-kit/submit.py \
  outputs/submissions/run2-final-six-seed-user-rank-test.csv \
  --data_dir data/KuaiRand-Pure/data --split test --check
```

Observed result:

```text
✓ 格式与对齐校验通过：170,588 行，split=test
```

No score command, upload, external submission, push, or repository visibility
change was performed.

## Reproduction command

The final ensemble is rebuilt from the six saved member prediction archives:

```text
.venv/bin/python solution/ranker.py \
  --data-dir data/KuaiRand-Pure/data \
  --variant prediction_ensemble \
  --prediction-ensemble-mode user_rank \
  --prediction-files \
    outputs/predictions/neural-fm-video-tag-history-seed2026.npz \
    outputs/predictions/neural-fm-video-tag-history-seed2027.npz \
    outputs/predictions/neural-fm-video-tag-history-seed2028.npz \
    outputs/predictions/run2-causal-seed2026-final.npz \
    outputs/predictions/run2-causal-seed2027-final.npz \
    outputs/predictions/run2-causal-seed2028-final.npz \
  --predictions-out outputs/predictions/run2-final-six-seed-user-rank.npz
```

The causal members were trained with `sequence_nn`, `long_view` video and tag
history of length 20, 16-dimensional embeddings, a 128-unit hidden layer,
dropout 0.2, neural FM interactions, AdamW learning rate 0.0005, weight decay
0.00001, early stopping, and seeds 2026-2028. Their exact commands are ledger
iterations 34-36.

## Known limits

- The final hidden-test identity and score are unknown.
- Apple MPS reproduction has small run-to-run numerical variation; the exact
  packaged members were rescored together rather than assuming prior metrics.
- The validation improvement over Run 1 is real on the available split but
  modest, so no claim is made that it guarantees a better hidden-test rank.
- The organizer statement's stale `click` / `NDCG@10` / `Recall@50` limits row,
  hidden-test wording, and judging-weight discrepancies remain unresolved as
  documented in `PREPARATION_STATUS.md`.
