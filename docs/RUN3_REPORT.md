# Run 3 ranking-family report

Run tag: `run3-ranking-families`
Branch: `codex/run3-ranking-families`
Started: 2026-08-29 14:04 SGT
Stopped: 2026-08-29 14:22 SGT

## Outcome

Run 3 stopped by its predeclared convergence rule after six counted attempts.
It evaluated three parent windows and three new-family candidates. None met the
+0.001 promotion gate, and the public test was evaluated zero times. The exact
Run 2 candidate at validation primary **0.6054008850** remains the fallback.

The best new result added the latest clicked and latest strongly engaged
video/tag as strictly past-only context. It improved the early shadow split by
0.000518560 and its forward window by 0.000256121, but regressed the
high-activity slice by 0.001382117. This is too small and unstable to promote.

## Attempt inventory

| Attempt | Purpose | Valid primary | Forward primary | Seconds |
|---:|---|---:|---:|---:|
| 1 | unchanged parent, early | 0.616833210 | 0.603950799 | 29.36 |
| 2 | unchanged parent, middle | 0.611458898 | 0.589591861 | 33.73 |
| 3 | unchanged parent, late | 0.592536211 | 0.603363514 | 41.65 |
| 4 | causal aggregate tree, early | 0.613724649 | 0.601950878 | 84.45 |
| 5 | neural plus causal aggregates, early | 0.616668046 | 0.602780282 | 468.94 |
| 6 | latest click/engagement context, early | 0.617351770 | 0.604206920 | 40.20 |

Maximum exact recorded subprocess RSS was 4,048,994,304 bytes. The organizer
evaluator remained unchanged with SHA-256
`ecfde28392eb14fec4f488083251df50624e1af2b86278b962daecfb42d195de`.
Exact commands, outputs, times, hashes, return codes, and resource readings are
preserved in `experiments/run3/ledger.jsonl`.

## What was learned

- Leakage-safe aggregate rates are individually predictive, but neither a
  standalone LightGBM model nor direct numeric injection beat the neural
  history parent.
- Latest action-specific context may contain a small useful signal, but the
  effect is below the robustness threshold and is not safe to select alone.
- The three-window parent scores vary substantially, confirming that
  single-window micro-gains are dangerous.
- The next high-value question is exposure bias, using the separate authorized
  random-exposure log only under chronological and provenance controls.

No submission, upload, public-test score, push, organizer contact, credential
use, registration change, or repository visibility change occurred.
