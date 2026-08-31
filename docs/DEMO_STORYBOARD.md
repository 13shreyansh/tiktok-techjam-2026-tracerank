# Three-minute demo storyboard — draft, not recorded or published

Purpose: demonstrate the working system and its safeguards without claiming a
hidden-test result. Target length: **2:50–3:00**.

## 0:00–0:25 — the problem

**Screen:** one user, several candidate videos, then the recommendation funnel.

**Narration:** “TikTok already has a small candidate set by the ranking stage.
Our task is to order each user's shown videos so meaningful long views appear
near the top. A good model must learn preference without overfitting one public
validation period.”

## 0:25–0:55 — the autonomous agent

**Screen:** `experiments/run2/ledger.jsonl`, a decision journal, and the
chronological split diagram from the presentation.

**Narration:** “The agent starts from the untouched organizer FM. Every idea is
declared before execution, tested on chronological shadow and forward windows,
checked across user-activity and date slices, and logged with its command,
metrics, time, memory, and code hash. Fragile improvements are rejected.”

## 0:55–1:30 — the selected Pure model

**Screen:** [`figures/tracerank-system.svg`](figures/tracerank-system.svg),
cropped to the selected-model row: candidate fields plus the user's last 20
positive video/tag events feeding six models, followed by within-user rank
averaging.

**Narration:** “The strongest Pure candidate combines current item context with
recent meaningful viewing history. Six independent models vote through ranks
inside each user's list. This reduces seed noise and matches GAUC and nDCG's
user-grouped objective.”

## 1:30–1:55 — measured result

**Screen:** [`figures/results-summary.svg`](figures/results-summary.svg), first
the Pure panel and then the validation-only warning.

**Narration:** “The published FM validation primary is 0.6016. Our clean
protected candidate reaches 0.605375: GAUC 0.672521 and nDCG at five 0.538228.
This is a validation result, not a final-test claim.”

## 1:55–2:20 — 1K generalization

**Screen:** Run 16 table showing base FM, content FM, and rejected history,
pairwise, multi-tag, and metadata rows.

**Narration:** “On the optional 1K benchmark, complicated sequence and ranking
ideas did not transfer. The agent retained the simpler content FM, which passed
three forward-time screens and three fixed seeds, reaching 0.653747 locally.”

## 2:20–2:42 — live verification

**Screen and command:**

```text
.venv/bin/python scripts/release_audit.py
.venv/bin/python scripts/verify_candidate_artifacts.py
```

Then show the organizer checker output:

```text
✓ 格式与对齐校验通过：170,588 行，split=test
```

**Narration:** “The release audit checks tracked files, JSON ledgers, starter
checksums, large-artifact boundaries, and common secret formats. The local
artifact verifier confirms every checkpoint, prediction, and final CSV hash.”

## 2:42–3:00 — honest close

**Screen:** `docs/RESOURCE_REPORT.md` and the limitations section.

**Narration:** “Every success, failure, resource cost, intervention, and known
rule ambiguity remains visible. The result is not just a score—it is a
reproducible agent that knows when evidence is too weak to promote a change.”

## Recording gates

- Use only real terminal output captured in one clean rehearsal.
- Do not show personal email, browser tabs, secrets, private remote URLs, or
  unredacted local paths.
- Keep “validation,” “local,” “unsubmitted,” and “hidden score unknown” visible.
- Record or publish nothing until the user explicitly authorizes the external
  action and confirms the final repository state.
- Render the two SVGs from the sanitized release tree, not the canonical tree,
  so no local path or private context can enter the recording.
