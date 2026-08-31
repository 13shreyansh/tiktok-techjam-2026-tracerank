# Run 3 decision journal

## 2026-08-29 14:04 SGT — campaign start

- Question: Is the next action aimed at winning rather than merely producing
  activity?
- Answer: Yes. It replaces single-window selection with paired chronological
  evidence and targets a missing model family.
- Current fallback: 0.605400885 validation primary, exact checked Run 2 CSV.
- Current action: establish three parent window scores before changing the
  model.
- Promotion rule: median paired gain >= 0.001, no window loss > 0.0005, segment
  safety, then official three-seed replication.

## 2026-08-29 14:10 SGT — aggregate tree family stopped

- Early-window primary: 0.613724649 versus parent 0.616833210,
  **-0.003108561**.
- Early forward primary: 0.601950878 versus parent 0.603950799,
  **-0.001999920**.
- The family also weakened the high-activity segment. Its strongest inputs were
  user long-view rate, user ID, tab-video rate, author, and video.
- Decision: stop the standalone tree immediately rather than spend two more
  windows on a clearly noncompetitive family.
- Win alignment: preserve the useful signal discovery, but move those strictly
  causal numeric aggregates into the stronger neural history parent instead of
  tuning the weaker tree.

## 2026-08-29 14:19 SGT — neural aggregate hybrid stopped

- Early-window primary: 0.616668046 versus parent 0.616833210,
  **-0.000165164**.
- Early forward primary: 0.602780282 versus parent 0.603950799,
  **-0.001170516**.
- Runtime was 468.94 seconds, over fifteen times the early parent runtime.
- Decision: stop. The hybrid failed the score, forward, and efficiency gates.
- Next family: represent the latest click and latest strong engagement directly
  as causal categorical context. This tests action-specific preference without
  the failed aggregate implementation or an additional large sequence model.

## 2026-08-29 14:22 SGT — multi-behavior context stopped

- Early-window primary: 0.617351770 versus parent 0.616833210,
  **+0.000518560**.
- Early forward primary: 0.604206920 versus parent 0.603950799,
  **+0.000256121**.
- Low and medium activity improved, but high activity regressed from
  0.566910310 to 0.565528193.
- Decision: stop. The gain is below the predeclared +0.001 promotion gate,
  below normal seed-scale uncertainty, and accompanied by a high-activity
  regression. Running two more windows would spend attempts polishing noise.
- Run decision: three distinct families have now failed to produce a material
  gain. Stop Run 3 under its convergence rule and preserve Run 2's exact
  0.605400885 fallback.
- Next campaign question: can the authorized random-exposure log provide a
  genuinely different, less exposure-biased preference signal that survives
  chronological validation? Audit it before implementing a model.
