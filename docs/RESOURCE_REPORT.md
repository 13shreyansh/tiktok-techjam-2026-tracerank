# Resource and autonomy report

Ledger and task-history snapshot: **2026-08-31 20:43 SGT**. Experiment totals
below are current through closed Run93. Refresh usage counters again at action
time if any further work occurs.

## Experiment accounting

| Campaign | Attempts | Outcome |
|---|---:|---|
| Run 1 | 33 | Selected first history model; one frozen public-test audit |
| Run 2 | 37 | Selected and packaged protected six-seed ensemble |
| Run 3 | 6 | Ranking/aggregate/context families rejected |
| Run 4 | 4 | Random-exposure robustness families rejected |
| Run 5 | 4 | Sampled listwise and BPR families rejected |
| Run 6 | 1 | Temporal context failed forward gate |
| Run 7 | 2 | Multi-behavior sequence variants rejected |
| Run 8 | 13 | Temporal diversity ensemble rejected officially |
| Runs 9-13 | 5 | Cross, CWM, Lambda, category, caption families rejected |
| Run 14 | 8 | Median-rank consensus rejected on shadows |
| Run 15 | 2 | Strictly causal repeat-pair memory rejected on shadows |
| Run 16 (closed) | 18 executed / 16 eligible | 1K content seed 2028 selected; two post-convergence attempts excluded |
| Run 17 | 1 | 1K DeepFM family rejected on first shadow gate |
| Run 18 | 1 | 1K field-aware FM family rejected on first shadow gate |
| Run 19 | 1 | 1K within-user BPR family rejected on first shadow gate |
| Run 20 | 2 | 1K sequence profile rejected; one engineering failure, one scored attempt |
| Run 21 | 1 | 1K exact user crosses rejected for forward overfit |
| Run 22 | 1 | 1K additive wide crosses rejected by forward guard |
| Run 23 | 1 | 1K regularized wide crosses rejected by forward guard |
| Runs 24-81 | 148 | Continued bounded Pure, 1K, and 27K audits; 145 success, 3 failed |
| Run 82 | 5 | Six-causal Pure artifact frozen; 4 success, 1 device failure |
| Run 83 | 24 | Three-window chronology selection audit; all successful |
| Run 84 | 8 | Clean Pure rebuild selected; 7 planned roles plus one disclosed duplicate seed execution |
| Run 85 | 1 | Strict-skip history rejected at its first chronological gate |
| Run 86 | 2 | Task-protected click extraction rejected; one pre-model device failure, one scored attempt |
| Run 87 | 1 | Cross-fit LambdaMART residual rejected after independent temporal transfer failed |
| Run 88 | 2 | Majority-pairwise consensus rejected after two chronological transfer failures |
| Run 89 | 1 | Causal self-attention history encoder rejected after catastrophic opening failure |
| Run 90 | 1 | Dual-timescale positive history rejected by forward and high-activity gates |
| Run 91 | 1 | Separate explicit-engagement history rejected by validation and high-activity gates |
| Run 92 | 1 | Hard target-match history expert rejected by validation, forward, and slice gates |
| Run 93 | 8 | Submission freeze before seed consensus; 7 success, 1 pre-model device failure, no candidate |
| **Total** | **344 executed** | **333 success, 11 failed/timed out** |

Recorded experiment subprocess time is **77,615.202 seconds** (21 h 33 m 35.2 s).
The largest exact subprocess RSS is **45,375,324,160 bytes**. These are summed
per-command elapsed times and the largest per-command peak RSS; they are not
exclusive accelerator kernel time and should not be represented as wall-clock
duration or simultaneous memory use. CUDA GPU-hours are zero. Apple MPS ran on
an Apple M5 Pro with 64 GB unified memory under macOS 26.6.2.

Every individual campaign remained below 50 attempts and six elapsed hours.
The live statement explicitly applies both limits **per benchmark run** and
asks for the resources required to reach the selected converged result. Run2
produced the mixed fallback after 37 attempts and 3,172.35 seconds of campaign
wall time. Run82 froze the selected all-causal artifact in 5 attempts, and
Run83 selected it through 24 independent chronological-audit attempts. Run84
rebuilt the final candidate label-blind in 8 counted executions; the eighth is
the preserved duplicate described in its incident report. Run85 tested one
strict-skip-history candidate and closed at its frozen first gate. The
Run86 task-protected click family then closed after one failed construction and
one below-gate scored attempt. Run87 then closed after its cross-fit residual
improved the meta window but failed both independent transfer windows. Run88
closed after two list-aggregation transfer failures. Run89 closed after one
catastrophic self-attention transfer failure. Run90 closed after one
dual-timescale attempt failed forward transfer and the high-activity floor. The
Run91 separate engagement channel improved forward but failed validation and
the high-activity floor. Run92 hard target matching failed validation, forward,
and three slice floors. Run93 stopped at the user's submission freeze after
seven successful seed subprocesses and one pre-model device failure, before
any declared consensus or candidate. The continuous body of work totals 344 executions, and
the statement does not define the boundary between restarted campaigns. Report
**Run2's 37 / 50,
Run82's 5 / 50, Run83's 24 / 50, Run84's 8 / 50, Run85's 1 / 50, Run86's
2 / 50, Run87's 1 / 50, Run88's 2 / 50, Run89's 1 / 50, Run90's 1 / 50,
Run91's 1 / 50, Run92's 1 / 50, Run93's 8 / 50, Run16's 18 executed / 16
convergence-eligible, and the 344-execution
cumulative total**. A literal audit
found that Run 16 attempts 14-16 met the three-round epsilon stop; attempts
17-18 are disclosed and excluded post-convergence exploration. They did not
change the attempt-13 candidate. Do not conceal the two extra executions or
claim that all 18 were eligible;
do not claim organizer approval of the interpretation. The live evidence is in
`docs/LIVE_RULES_AUDIT_2026-08-29.md`; all later campaign counts are preserved
in immutable ledgers.

## AI usage

- AI roles actually used: one root Codex goal agent; no sub-agents.
- Goal-runtime token snapshot at 20:43 SGT: **15,509,730 combined tokens**. The
  corresponding elapsed-time snapshot is **156,696 seconds** (43 h 31 m 36 s);
  refresh both immediately before the external submission.
- The available runtime counter does not expose a reliable input/output token
  split. The signed-in official Track 2 deliverables were re-read at 19:05 SGT
  and explicitly request `total token consumption (input + output)`, not a
  separate breakdown. Report the combined counter as exposed and do not invent
  an unavailable split.
- Karpathy autoresearch, AIDE, and FML-Bench were used as pinned research and
  process references. Their incompatible workloads were not run or claimed as
  the Track 2 solution.

## Human interaction disclosure

The Codex task-history API was paginated to exhaustion at this snapshot: 52
turns contained **26 user-authored messages**. This is the complete product-task
message count returned by that API at the snapshot, not a claim that all 26
messages changed model search.

Campaign logs identify two explicit kickoff messages and two later
behavior-changing strategic steers. The first steer is recorded at both the Run 6
close and Run 7 start and must be counted once, not twice. Thus the experiment
ledger contains **six unique disclosed human campaign-control events**, of
which the two kickoffs set process objectives without changing an active
candidate and four steers changed the next hypothesis-family priority, run
interpretation, or submission freeze. Other user
questions and status requests did not change an active experiment, while
autonomous campaign transitions are explicitly marked as such.

The count was refreshed through `hasMore=false`; autonomous continuations
increased the turn count without increasing the 26 user-authored messages.
Refresh again before submission if another user message arrives. The current
experiment-ledger count is six unique campaign-control events. Do not describe
AI steering as human intervention.

## External-action boundary

On 2026-08-31, the user authorized creation of a separate public repository and
publication of the audited sanitized release. The private canonical repository
remains private. No dataset, checkpoint, prediction archive, generated CSV,
cache, credential, or private communication was included. No final Devpost
submission, organizer contact, registration change, or final-test output upload
has been performed.
