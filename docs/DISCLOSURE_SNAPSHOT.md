# AI, human, iteration, and external-action disclosure snapshot

Experiment-ledger and task-history snapshot: **2026-08-31 20:43 SGT**. Goal
counters and the complete task history were refreshed together. Refresh the
usage counters again at action time if any further work occurs.

## AI participation

- One root Codex goal agent performed the research and implementation.
- No subagents were used.
- Combined goal-runtime counter: **15,509,730 tokens**.
- Goal elapsed-time counter: **156,696 seconds** at the 20:43 SGT
  snapshot.
- The available counter does not expose a trustworthy input/output split. No
  split is estimated or invented.
- Karpathy autoresearch, AIDE, and FML-Bench were process references only. Their
  incompatible upstream workloads were not executed as this solution.

## Human participation

The Codex task-history API was read in six pages until `hasMore=false`. It
returned 52 turns and **26 user-authored messages** at this snapshot. The turn
count increased through autonomous continuations while the user-message count
remained 26.

The experiment ledgers separately identify **six unique human
campaign-control events**:

1. Run 2 kickoff: requested a continuous, maximum-score campaign with safeguards.
2. Run 3 kickoff: requested the 72-hour objective and periodic fresh-context review.
3. Run 6/7 strategic steer: prioritized explicit multi-behavior history,
   within-user ranking/list reasoning, and fuller autoresearch discipline.
4. Run 17 steer: challenged the global-stop interpretation and directed
   continued, fully documented benchmark runs.
5. Run 18 steer: explicitly resumed the winning objective and required the
   next distinct, fully documented model-family run to begin immediately.
6. Run 93 steer: explicitly froze further model search and directed submission
   planning; the active seed-saturation audit closed without a candidate.

The third event is duplicated across the Run 6 close and Run 7 start for
provenance and is counted once. The two kickoff messages established process
objectives but did not replace an active model candidate. The strategic steer
events changed the next hypothesis-family priority or run-boundary
interpretation. Questions and status requests are
included in the 26-message total but are not mislabeled as model-search changes.

## Experiment and compute accounting

- Total research executions: **344**.
- Successful executions: **333**.
- Failed or timed-out executions: **11**.
- Run2 mixed-fallback campaign: **37 / 50 attempts**, 3,172.35 seconds.
- Run82 all-causal artifact campaign: **5 / 50 attempts**.
- Run83 chronological selection audit: **24 / 50 attempts**, all successful.
- Run 16 KuaiRand-1K campaign: **18 executed / 16 convergence-eligible**; two
  post-convergence executions are disclosed and excluded from candidate choice.
- Run 17 KuaiRand-1K DeepFM campaign: **1 rejected shadow attempt**.
- Run 18 KuaiRand-1K field-aware FM campaign: **1 rejected shadow attempt**.
- Run 19 KuaiRand-1K within-user BPR campaign: **1 rejected shadow attempt**.
- Run 20 KuaiRand-1K sequence-profile campaign: **2 executions**; one encoder
  failure and one rejected shadow result.
- Run 21 KuaiRand-1K explicit-cross campaign: **1 rejected shadow attempt**.
- Run 22 KuaiRand-1K additive-wide-cross campaign: **1 rejected shadow
  attempt**.
- Run 23 KuaiRand-1K regularized-wide-cross campaign: **1 rejected shadow
  attempt**.
- Run84 clean Pure rebuild: **8 executions**, including one disclosed duplicate.
- Run85 strict-skip Pure family: **1 rejected scored attempt**.
- Run86 task-protected click Pure family: **2 executions**, one pre-model
  device failure and one rejected scored attempt.
- Run87 chronological residual Pure family: **1 rejected scored attempt**.
- Run88 majority-pairwise Pure family: **2 rejected scored attempts**.
- Run89 causal self-attention Pure family: **1 rejected scored attempt**.
- Run90 dual-timescale positive-history Pure family: **1 rejected scored attempt**.
- Run91 separate explicit-engagement-history Pure family: **1 rejected scored attempt**.
- Run92 hard target-match history Pure family: **1 rejected scored attempt**.
- Run93 seed-saturation audit: **8 executions**; one pre-model device failure,
  seven successful subprocesses, and no completed consensus or candidate.
- Recorded subprocess time: **77,615.202 seconds**.
- Largest exact subprocess RSS: **45,375,324,160 bytes**.
- CUDA GPU-hours: zero. Apple MPS was used on an Apple M5 Pro with 64 GB unified
  memory under macOS 26.6.2.

Every individual campaign remained below 50 attempts and six hours. The
challenge statement does not define when a restarted campaign becomes a new
benchmark run, so the artifact-producing and selection-audit campaign counts
and the cumulative 344-execution count must all be disclosed. No organizer approval of this
interpretation is claimed.

## Evaluation and external-action boundary

- Hidden-test access: none.
- One early frozen public-test audit is documented; later candidates were not
  selected on public-test labels.
- One user-authorized external publication action occurred on 2026-08-31: a
  separate public repository was created for the audited sanitized release.
  The private canonical repository remains private.
- No final-test output, checkpoint, generated prediction CSV, or dataset was
  published. The selected Pure candidate, mixed fallback, and 1K candidate
  remain local, hashed, and unsubmitted to the organizer.
- No Devpost final submission, registration change, or organizer contact has
  occurred.

Before submission, refresh all live counters and the task-history count. If the
organizer requires separate LLM input and output tokens, obtain a product export
or report that the runtime exposed only a combined counter.
