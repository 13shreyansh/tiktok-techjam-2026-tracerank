# Devpost submission packet — prepared, not finally submitted

Every bracketed field requires a real final value. This file prepares text only;
it does not authorize publication, upload, repository visibility changes, or
submission.

## Project name

**TraceRank — Evidence-Driven Autonomous Recommendation Research**

## Tagline

An autonomous ranking agent that tests ideas across time, rejects fragile
improvements, and packages reproducible KuaiRand candidates with complete
resource and decision evidence.

## Track

Track 2 — Autonomous ML Agent

## Short description

TraceRank improves short-video recommendation ordering while treating reliable
experimentation as part of the model. It starts from the organizer FM, tests
each declared hypothesis on chronological future windows and user-activity
slices, records exact commands and resources, and promotes only repeatable
gains. Its clean KuaiRand-Pure candidate reaches 0.605375 local validation
primary versus the published 0.6016 baseline; its separate KuaiRand-1K content
candidate reaches 0.653747 local validation primary. Final-test scores remain
unknown.

## What we built

TraceRank is an autonomous experimentation and recommendation-ranking system.
The agent preserves the organizer evaluator, declares each hypothesis before
execution, enforces per-run attempt and time limits, measures chronological
transfer and subgroup robustness, and records every keep/reject decision in an
append-only ledger.

For KuaiRand-Pure, the selected model combines candidate context with attention
over the user's last 20 positive long-view video and tag events. Six independent
model predictions are converted to percentile ranks within each user's list
and averaged. This reduces seed noise and aligns the final consensus with the
user-grouped GAUC and nDCG@5 metrics.

For the optional KuaiRand-1K benchmark, the agent learned that the Pure history
architecture did not transfer. It instead retained a smaller sparse
factorization model using the official primary-tag, upload-type, and video-type
fields. That candidate improved both metrics and every activity slice in three
fixed chronological screens and reproduced all saved validation predictions
bit-for-bit.

## Measured results

| Benchmark | Candidate | GAUC | nDCG@5 | Primary |
|---|---|---:|---:|---:|
| KuaiRand-Pure | Published organizer FM | — | — | 0.601600 |
| KuaiRand-Pure | Clean six-member causal-history rank consensus | 0.672521 | 0.538228 | **0.605375** |
| KuaiRand-1K | Content sparse FM, seed 2028 | 0.688786 | 0.618707 | **0.653747** |

The Pure improvement is +0.003774520 on organizer validation. The organizers
have not published a comparable 1K baseline. These are local validation values,
not final-test or leaderboard claims.

## Why it is different

Many automated ML loops maximize one visible number. TraceRank treats a score
as insufficient evidence. A candidate must survive future-time windows,
low/medium/high-activity users, date slices, multiple seeds, exact artifact
reconstruction, and a predeclared promotion rule. Time features, listwise
losses, deeper networks, captions, hierarchical categories, multi-action
histories, censored watch time, and larger ensembles were all rejected when
their apparent gains failed those gates.

The result is both a ranking model and an auditable research process: judges can
inspect the hypothesis, command, code/evaluator hash, metrics, time, peak
memory, decision, human intervention, and convergence status for every attempt.

## Impact and feasibility

At the ranking stage, a feed already has a manageable set of candidates. Better
ordering can surface personally relevant videos earlier without applying an
expensive model to the full catalogue. TraceRank's protected system ran on one
Apple M5 Pro laptop with no CUDA accelerator, cloud model service, or API
secret. The final Pure CSV passed the label-blind 170,588-row alignment checker.

The broader contribution is transferable: chronological evaluation, subgroup
checks, immutable experiment evidence, and stop rules can make autonomous model
research safer in other recommendation and ranking systems.

## Technical stack

- Python 3
- PyTorch 2.7.1 for neural factorization and history attention
- NumPy 2.0.2 and SciPy 1.13.1
- scikit-learn 1.6.1 and LightGBM 4.6.0 for bounded comparison families
- Organizer-provided KuaiRand loader, evaluator, baseline, and submission checker
- Shell and Python acquisition scripts with URL, checksum, licence, and safe-
  extraction controls
- JSONL experiment ledgers, SHA-256 artifact manifests, resource accounting,
  release/privacy audits, and deterministic sanitized release generation

## Autonomy and resource disclosure

- AI roles: one root Codex goal agent; no subagents.
- Human task messages at the complete 20:43 SGT task-history snapshot: 26
  across 52 turns; refresh again if another user message arrives.
- Unique logged campaign-control events: six.
- Total research executions: 344; 333 successful and eleven failed/timed out.
- Original Pure candidate run: 37 / 50 attempts and 3,172.35 seconds.
- All-causal Pure artifact run: 5 / 50 attempts; chronological selection audit:
  24 / 50 attempts.
- Clean final-test-boundary rebuild: 8 / 50 executions, including one disclosed
  duplicate seed execution caused by an orchestration polling race.
- Separate Pure strict-skip-history run: 1 / 50 successful execution, rejected
  at its first chronological gate without rescue tuning.
- Separate Pure task-protected click run: 2 / 50 executions; one pre-model
  MPS-sandbox failure and one scored rejection at the first materiality gate.
- Separate Pure chronological residual-ranker run: 1 / 50 successful execution;
  rejected when its meta-window gain reversed on independent target and forward
  windows.
- Separate Pure majority-pairwise consensus run: 2 / 50 successful executions;
  stopped after two chronological transfer failures.
- Separate Pure causal self-attention run: 1 / 50 successful execution;
  rejected after catastrophic validation and forward regressions.
- Separate Pure dual-timescale positive-history run: 1 / 50 successful
  execution; rejected by the forward and high-activity gates.
- Separate Pure explicit-engagement-history run: 1 / 50 successful execution;
  rejected by validation and high-activity gates.
- Separate Pure hard target-match run: 1 / 50 successful execution; rejected
  by validation, forward, and slice gates.
- Separate Pure seed-saturation audit: 8 / 50 executions; one pre-model device
  failure and seven successful subprocesses. It closed at the user's
  submission freeze before a declared consensus or candidate existed.
- 1K run: 18 executed / 16 convergence-eligible; two post-convergence attempts
  are disclosed, excluded, and did not change the candidate.
- Separate 1K DeepFM run: one successful attempt, rejected at its first shadow
  gate without tuning.
- Separate 1K field-aware FM run: one successful attempt, rejected at its first
  shadow gate without tuning.
- Separate 1K within-user BPR run: one successful attempt, rejected after a
  forward gain failed the validation and robustness gates.
- Separate 1K sequence-profile run: two executions, including one encoder
  failure and one rejected shadow result.
- Separate 1K explicit-cross run: one successful attempt, rejected for forward
  and high-activity overfit.
- Separate 1K additive-wide-cross run: one successful attempt, rejected by the
  fixed forward guard despite improving all validation slices.
- Separate 1K regularized-wide-cross run: one successful attempt, rejected by
  the forward guard without a coefficient sweep.
- Recorded experiment subprocess time: 77,615.202 seconds.
- Peak exact subprocess RSS: 45,375,324,160 bytes.
- CUDA GPU-hours: zero; Apple MPS used unified memory.
- Combined Codex counter at the 20:43 SGT snapshot: 15,509,730 tokens. The
  corresponding elapsed-time snapshot is 156,696 seconds.
  The runtime does not expose a reliable input/output split; the official Track
  2 deliverable asks for the combined `input + output` total, so no split
  should be invented.

Refresh the live task-message, token, and elapsed-time counters immediately
before submission. Report both candidate-producing campaign counts and the
cumulative total because restarted-run boundaries are not defined.

## Truthful limitations

- Final-test outcomes and scores remain unread; the supplied test rows are the
  confirmed final judged rows.
- One earlier frozen Pure model was audited once on the public date-based test;
  that result did not select later candidates, and the protected candidate has
  not been test-scored.
- The selected Pure ensemble uses fully chronological histories. Its primary
  gain over the preserved mixed fallback is only `+0.0001203396`, and one of
  three chronological audit windows did not improve forward primary.
- The live statement contains a metric contradiction: its executable evaluator
  uses GAUC and nDCG@5 while one stale row says NDCG@10 and Recall@50.
- The 1K-specific checker, bonus formula, and final schema are unpublished.
- KuaiRand logs reveal reactions only to shown items and contain incomplete user
  histories, so offline gains may not transfer fully to a live feed.

## Required final links

- Public repository: **https://github.com/13shreyansh/tiktok-techjam-2026-tracerank**
- Public three-minute YouTube demo: **[ADD VERIFIED VIDEO URL]**. Track 2 calls
  the video optional/recommended, but the Devpost overview calls it required;
  providing it is the safer interpretation.
- Working project access for judges: **Public repository plus
  `docs/JUDGE_QUICKSTART.md`; datasets are acquired from their official sources
  with the included checksum-verifying scripts.**
- Track-specific model/checkpoint delivery: **[ADD OFFICIAL ROUTE WHEN PUBLISHED]**

## Final action gate

Before copying this packet into Devpost:

1. Refresh all usage and interaction counters.
2. Build and review a clean sanitized repository from
   `docs/PUBLIC_RELEASE_PROTOCOL.md`.
3. Record the real demo following `docs/DEMO_STORYBOARD.md` and confirm it is
   public and no longer than three minutes.
4. Insert and open every final URL in a logged-out browser.
5. Recheck the official Track 2 document and Devpost updates for a delivery route.
6. Obtain explicit user authorization before each push, visibility change,
   upload, or final submission action.
