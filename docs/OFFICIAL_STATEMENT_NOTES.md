# Official Track 2 statement notes

Public source: [TikTok TechJam 2026 Information Document](https://bytedance.larkoffice.com/wiki/GdYFwzWNLiREsSkuIjZcDznInWc#Awozdl0mGo1DnXxwFuemYSilyzP)

Early-bird source: [TikTok TechJam 2026 problem statements](https://bytedance.larkoffice.com/wiki/DNtSwxgeciCS2nkiUefc5qqtnkf#DM16dtAj1oEaJex5qSlm2DAiyag)

Rechecked through **2026-08-31 19:48 SGT** after public launch. Track 2 now
shows **Added FAQs: 31 August 2026, 1:57 PM**. The latest read-only evidence is
in `docs/OFFICIAL_FAQ_AUDIT_2026-08-31.md`.

## Preparation-relevant requirements

- Required benchmark: KuaiRand-Pure. KuaiRand-1k and KuaiRand-27k are described
  as optional bonus benchmarks.
- The benchmark task is impression ranking: predict `long_view` and rank each
  user's logged impressions. It is not full-catalog item retrieval.
- Operative metrics are `GAUC` and `nDCG@5`; primary is their arithmetic mean.
- The supplied date-based test rows are the final judged rows. There is no
  separate private dataset. Test outcomes cannot be used at any development
  stage; code and logs are reviewed for this boundary.
- The fixed date split published beside the starter is train
  `20220408–20220421` (1,141,112 rows), validation `20220422–20220428`
  (124,909 rows), and test `20220429–20220508` (170,588 rows).
- The organizer starter is NumPy-only. The published FM configuration is `k=16`,
  `lr=0.001`, five categorical fields, with an expected single-core runtime of
  about 40 seconds.
- The statement publishes FM validation `GAUC 0.6674 / nDCG@5 0.5357 /
  primary 0.6016` and test `0.6610 / 0.5282 / 0.5946` as five-seed reference
  values. The 31 August FAQ allows a team to predeclare its own convergence
  epsilon, consecutive-window length, and optional minimum-iteration floor.
- The starter submission schema is
  `row_id,user_id,video_id,score`; `row_id` is required because user/video pairs
  are not unique.
- Required final materials are described as a Devpost description, public code
  repository, iteration logs plus manual-intervention count, final output or
  checkpoint, results summary, and a resource report containing total LLM token
  consumption (`input + output`), total agent wall-clock time, iterations used
  out of 50, and GPU-hours if any. The official wording requests the combined
  token total; it does not require a separate input/output breakdown.
- Each benchmark run has a hard cap of 50 iterations and a six-hour wall-clock
  ceiling. Convergence parameters must be fixed and logged before the run;
  failed attempts consume budget but do not alter the convergence window. LLM
  tokens and GPU-hours must be reported but are not capped.
- Feasibility is scored only after the final-test primary exceeds the official
  baseline. Qualifying submissions are placed in coarse low/medium/high resource
  tiers; agent wall-clock is the scored compute measure, while GPU-hours remain
  reportable.
- The statement publishes random primary `0.4753`, baseline primary `0.5946`,
  and oracle-ceiling primary `0.8645`, placing the baseline at about 31% of the
  attainable random-to-oracle interval.

These notes describe the statement; they do not authorize a submission,
visibility change, or pre-window solution work.

## Metric clarification and remaining stale row

The 27 August revision resolves the practical scoring contract in favour of the
organizer starter:

| Official location | Label and metrics |
|---|---|
| Introduction, benchmark table, deliverables, judging formula, and published FM scores | `long_view`; `GAUC / nDCG@5`; primary is their mean |
| Unchanged downloaded `README.md`, `data.py`, `evaluate.py`, and `baseline_scores.json` | `long_view`; `GAUC / nDCG@5`; primary is their mean |
| Limits-table first bullet only | stale `click`; `NDCG@10 / Recall@50` |

The Limits-table bullet remained an internal contradiction in a fresh live-page
find at 19:48 SGT (`NDCG@10`: 1 match; `Recall@50`: 1 match; `nDCG@5`: 1
match) and should not be silently erased. It is nevertheless a lone outlier
rather than the former document-wide split. This repository preserves that
distinction and does not begin a judged solution before the official window.

## Other unresolved statement gaps

- Optional KuaiRand-1k and KuaiRand-27k benchmarks are labelled bonus, but no
  bonus formula or point value is stated.
- Track 2 states final-only weights of Technical 35%, Innovation 20%, Impact
  20%, Feasibility 15%, and Presentation 10%. Devpost's Official Rules instead
  state four equally weighted Stage Two criteria and omit Presentation. Neither
  source states which controls if they differ.
- Track 2 says a three-minute video is optional but recommended, while the
  Devpost overview says a public three-minute YouTube demo is required. The
  safer submission plan is to provide the video while preserving the conflict.
- The Lark attachment exposes no stable direct URL in the visible document.
  Provenance therefore records the page, Track 2 starter anchor, attachment
  name, byte size, and checksum.

## Official resource locations

- Public Information Document and Track 2 statement: the public Lark URL above
- Starter attachment: the early-bird Lark URL above; the public page identifies
  the same Track 2 statement version
- Devpost Resources: <https://tiktoktechjam2026.devpost.com/resources>
- Devpost Updates: <https://tiktoktechjam2026.devpost.com/updates>
- Devpost Rules: <https://tiktoktechjam2026.devpost.com/rules>
- Official Telegram channel: <https://t.me/TikTokTechJam2026>
- KuaiRand project: <https://kuairand.com>
- KuaiRand Zenodo record: <https://zenodo.org/records/10439422>
- Organizer-authorized KuaiRand-Pure file:
  <https://zenodo.org/records/10439422/files/KuaiRand-Pure.tar.gz>

The complete machine-readable provenance record is
`manifests/official-resources.json`.
