# Run 2 robust-ranking protocol

Run tag: `run2-robust-ranking`  
Branch: `codex/run2-robust-ranking`  
Human kickoff: 2026-08-29 12:55 SGT

## Objective

Maximize likely hidden-test `primary = mean(GAUC, nDCG@5)`, not merely exceed
the baseline. The public date-based test labels are locked for this campaign.

## Selection gates

1. Keep the organizer evaluator unchanged and verify its SHA on every attempt.
2. Count every launched attempt, including crashes, against 50 iterations.
3. Never use `--evaluate-test`; the Run-2 harness rejects it.
4. Start from the reproduced Run-1 model. Change one coherent idea at a time.
5. Use causal histories only: an example may not see a later interaction.
6. Build temporal shadow validation inside the official training period and
   inspect official validation only as a promotion gate.
7. Prefer gains that improve both GAUC and nDCG@5 and survive temporal slices,
   user-activity segments, and independent seeds.
8. Treat an isolated gain smaller than normal seed variation as unconfirmed.
9. Keep failed branches in the ledger; advance only from a defensible parent.
10. Stop at 50 attempts, six hours, the organizer convergence rule, or a real
    blocker. Do not submit or publish without explicit user approval.

## Search order

1. Correct chronology and establish shadow-split reliability.
2. Improve interest history: positive and negative events, recency, target-aware
   attention, tags, and short/long-term representations.
3. Add useful auxiliary supervision (`click`, watch ratio, engagement) without
   changing the target metric.
4. Test ranking-aligned objectives only after the representation is stable.
5. Test exposure-bias robustness with the random-exposure log as an audit, not
   as a source of public-test feedback.
6. Replicate and ensemble only candidates that pass the robustness gates.

## Human-interaction accounting

The kickoff message that created Run 2 is recorded in `human_interactions.jsonl`.
Any later user message during the campaign will also be recorded and classified
as status-only, clarification, or steering. Commentary emitted by Codex is not a
human intervention.
