# Live rules audit — 2026-08-29

Read-only audit time: **2026-08-29 16:47 SGT**. No submission, upload,
message, visibility change, or other external mutation was performed.

## Official sources rechecked

- Track 2 in the signed-in public Information Document:
  <https://bytedance.larkoffice.com/wiki/GdYFwzWNLiREsSkuIjZcDznInWc#Awozdl0mGo1DnXxwFuemYSilyzP>
- Devpost Official Rules: <https://tiktoktechjam2026.devpost.com/rules>
- Devpost Updates: <https://tiktoktechjam2026.devpost.com/updates>
- Devpost Resources: <https://tiktoktechjam2026.devpost.com/resources>

The Lark document showed a global `Last modified: 23:23 Yesterday` marker, but
the Track 2 section still identified itself as **Problem Statement last
updated: 27 August 2026, 5:55 PM**. The starter remained the 15.48 KB
`kuairand-starter-kit.zip`. Devpost Updates still contained no announcement.

## What the live wording establishes

1. The compute limit is expressly **per benchmark run**: 50 iterations and a
   six-hour wall-clock ceiling per run. The same section says the convergence
   rule normally stops a run first.
2. The convergence rule is validation improvement no greater than epsilon
   `0.002` over the last `N=3` consecutive iterations. The validation-best
   checkpoint at convergence is evaluated once on the hidden test.
3. The resource deliverable asks for the consumption required to reach the
   converged result: total LLM input plus output tokens, total agent wall-clock,
   iterations used out of 50, and GPU-hours if any.
4. Autonomy is assessed through per-iteration logs and a manual-intervention
   summary. A fully autonomous run is described as ideal, while a small number
   of interventions is explicitly acceptable.
5. The submitted repository must be public and contain reproducible code and a
   README. Judges must also be given access to a working project. The Devpost
   deadline is **1 September 2026 at 12:00 PM SGT**.

## Interpretation for this repository

The protected candidate was produced and frozen in Run 2 after **37 / 50**
counted attempts and **3,172.35 seconds** of campaign wall time. Later Runs
3–14 tested other hypothesis families and did not change the protected
candidate. The literal per-run wording therefore supports reporting Run 2 as
the candidate-producing benchmark run.

The statement does not define when one run ends and another begins or whether
teams may report several restarted research campaigns. Because the same Codex
goal continued across them, a conservative judge could still aggregate the
whole body of work. The transparent submission policy is therefore:

- report Run 2's 37 attempts and 3,172.35 seconds as the resources that produced
  the selected converged candidate;
- separately disclose **113 cumulative attempts** across Runs 1–14, with every
  campaign below 50 attempts and six hours; and
- do not claim that the organizers approved this interpretation.

This is a narrower residual ambiguity than previously recorded. The official
text does not state a cumulative 50-attempt cap across all campaigns.

This paragraph is an audit-time snapshot. Run 15 later brought the current
research total to 115, and Run 16 later brought it to 133 executions, of which
16/18 Run-16 attempts are convergence-eligible. `docs/RESOURCE_REPORT.md` is
authoritative for the latest counter; Run 17 subsequently brought the total to
134 with one rejected DeepFM shadow attempt, and Run 18 brought it to 135 with
one rejected field-aware FM shadow attempt.
Run 19 then brought the total to 136 with one rejected within-user BPR shadow
attempt.
Run 20 then brought the total to 138 with one encoder failure and one rejected
causal sequence-profile shadow result.
Run 21 then brought the total to 139 with one explicit-cross shadow result
rejected for forward overfit.
Run 22 then brought the total to 140 with one additive-wide-cross shadow result
rejected by the fixed forward guard.
Run 23 then brought the total to 141 with one regularized-wide-cross shadow
result rejected by the fixed forward guard.

## 18:35 SGT public-portal refresh

A second read-only check of the public Devpost Overview, Resources, Updates,
and Rules pages found no new Track 2 attachment, hidden-test delivery route,
1K-specific checker, or organizer announcement. The Updates page still showed
only “Stay tuned for important announcements.” The deadline remained
**1 September 2026 at 12:00 PM SGT**.

The public requirements still require a written description, a public code
repository with a comprehensive README, and a public three-minute YouTube demo.
The Rules separately require access to a working project for judging. This
refresh did not modify Devpost, send a message, download an attachment, or
perform any other external action. Chrome could see the existing signed-in
Lark tab but could not attach to it within the read timeout, so this refresh
does not claim a newer Lark document verification than the 16:47 SGT audit.

## Contradictions that remain live

- The Limits table still says `click`, `NDCG@10`, and `Recall@50`. The benchmark
  table, starter, evaluator, deliverables, convergence section, and published
  baseline consistently use `long_view`, `GAUC`, and `nDCG@5`. The stale row
  has not been removed.
- Lark publishes Track 2 weights of 35/20/20/15/10, including Presentation at
  the final event. Devpost Rules publish four equally weighted Stage Two
  criteria. Neither source supplies a precedence rule.
- The statement calls the final test hidden and one-shot, while the starter
  exposes a public date-based split named `test`. The protected candidate has
  not been scored on that split, and the eventual hidden-test identity remains
  unknown.
- The exact mechanism for delivering the hidden-test artifact or checkpoint is
  still not exposed in the checked official pages.

## 18:47 SGT delivery-route recheck

A third read-only public check again found no new Track 2 attachment,
KuaiRand-1K checker, hidden-test delivery route, or posted update. Devpost still
listed only the information-document link under Resources and “Stay tuned for
important announcements” under Updates. The deadline and required written
description, public repository, and public three-minute YouTube demo were
unchanged.

The signed-in Chrome session still listed the official Lark information
document at the same wiki URL, but two supported attachment attempts timed out.
The tab's existence and title are therefore confirmed; its current contents
were not read in this refresh. No private-content claim is made from the tab,
and no click, message, submission, download, or account change occurred.

## 20:11 SGT run-boundary re-read

The signed-in live statement still says `50 iterations per benchmark run` and
`6 h wall-clock ceiling per run`, with convergence normally triggering first.
It separately defines convergence as no validation-primary improvement greater
than epsilon `0.002` over `N=3` consecutive iterations. It does **not** define
when one run ends and another may begin, nor state a cumulative cap across all
development campaigns.

Literal interpretation permits closing and documenting a converged run before
opening another predeclared run. An arbitrary restart after every weak result
would also make the cap ineffective, so this is not treated as blanket approval
for unlimited resets. Repository policy is to require a genuinely independent
hypothesis family, declare its protocol before scoring, apply fresh per-run
limits, and disclose both per-run and full cumulative resources. This is a
transparent interpretation, not an organizer clarification.

## 19:05 SGT signed-in route and deliverables audit

A fresh agent-created Chrome tab successfully loaded the signed-in official
Lark information document and navigated to Track 2. The section still labels
itself **Problem Statement last updated: 27 August 2026, 5:55 PM**. It confirms:

- final KuaiRand-Pure output/checkpoint is required and bonus-benchmark outputs
  should be submitted for bonus scoring;
- per-iteration hypothesis, code-diff, metrics, error/recovery, and manual-
  intervention records are required;
- resource reporting asks for **total token consumption (input + output)**,
  agent wall-clock, iterations out of 50, and GPU-hours; a separate input/output
  token split is not requested; and
- Track 2 does not require a video, although a roughly three-minute video is
  recommended when helpful.

The last point conflicts with the live Devpost overview, which still says a
public three-minute YouTube demo is required. Supplying the video remains the
conservative plan. The Lark section still exposes no hidden-test delivery
mechanism, 1K-specific checker, or bonus formula.

The signed-in Devpost overview confirmed registration and the 1 September 2026
12:00 PM SGT deadline. Its **My projects** page currently says “Start a Project”
and exposes only a **Create project** action; no submission draft or track-
specific upload field exists yet. Read-only element inspection confirmed that
the button submits a `POST` to the project-management endpoint and invokes
invisible reCAPTCHA; there is no non-mutating field-preview link. The action was
not clicked because creating a project is an external mutation requiring
explicit authorization. No message, download, project creation, upload,
visibility change, or submission occurred.
