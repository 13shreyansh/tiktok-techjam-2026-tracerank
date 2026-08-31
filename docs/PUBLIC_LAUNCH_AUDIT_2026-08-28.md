# Public launch audit — 2026-08-28

This is a preparation-only audit of the official launch. It does not select or
implement a judged strategy.

## Sources checked

- Public Information Document:
  <https://bytedance.larkoffice.com/wiki/GdYFwzWNLiREsSkuIjZcDznInWc#Awozdl0mGo1DnXxwFuemYSilyzP>
- Early-bird Track 2 statement and starter attachment:
  <https://bytedance.larkoffice.com/wiki/DNtSwxgeciCS2nkiUefc5qqtnkf#DM16dtAj1oEaJex5qSlm2DAiyag>
- Devpost Resources, Updates, and Official Rules:
  <https://tiktoktechjam2026.devpost.com/resources>,
  <https://tiktoktechjam2026.devpost.com/updates>, and
  <https://tiktoktechjam2026.devpost.com/rules>
- Official Telegram channel: <https://t.me/TikTokTechJam2026>

The public Information Document reported `Last updated: Aug 28`. Both Lark
copies reported `Problem Statement last updated: 27 August 2026, 5:55 PM` for
Track 2. The early-bird copy stated that the public release was the same version.

## What changed or became clear

1. The operative benchmark contract is now repeated across the introduction,
   benchmark table, deliverables, judging formula, published baseline, and
   unchanged starter: predict `long_view`, rank within each user's logged
   impressions, and score `GAUC` plus `nDCG@5`; primary is their mean.
2. The run budget is no longer TBD: 50 iterations per benchmark run, with a
   six-hour wall-clock ceiling. Epsilon `0.002` over `N=3` iterations is the
   convergence rule expected to stop most runs first.
3. The resource report now names LLM input/output tokens, total agent wall-clock,
   iterations used out of 50, and GPU-hours if any. Tokens and GPU-hours are
   reported rather than capped.
4. Feasibility scoring has a quality gate: the hidden-test primary must beat the
   official baseline before resource efficiency is scored. Qualifying entries
   are grouped into low/medium/high resource tiers rather than ranked by a
   continuous cost formula.
5. The statement publishes random primary `0.4753`, official baseline `0.5946`,
   and oracle ceiling `0.8645`.

## Remaining inconsistencies

- One Limits-table bullet still says `click` with `NDCG@10 / Recall@50`. It is
  the only such row; all operational and implementation-facing sections say
  `long_view`, `GAUC`, and `nDCG@5`.
- The statement calls the final test hidden and one-shot, while the starter
  exposes and scores a public date-based split named `test`.
- The optional KuaiRand-1k and KuaiRand-27k bonus has no published formula.
- Track 2's 35/20/20/15/10 weights conflict with Devpost's four equally weighted
  Stage Two criteria.
- The starter archive still contains no licence or notice file.

## Starter attachment verification

The attachment was downloaded through the signed-in Lark UI, checked, and the
temporary duplicate was removed after comparison. Exact local checks:

```bash
shasum -a 256 '${USER_HOME}/Downloads/kuairand-starter-kit (2).zip' \
  artifacts/original/kuairand-starter-kit.zip
stat -f '%N %z bytes' \
  '${USER_HOME}/Downloads/kuairand-starter-kit (2).zip' \
  artifacts/original/kuairand-starter-kit.zip
cmp -s '${USER_HOME}/Downloads/kuairand-starter-kit (2).zip' \
  artifacts/original/kuairand-starter-kit.zip
```

Observed result: both files were 15,848 bytes, both had SHA-256
`07237e62cc1a9cd8278556dab995dd5388516f10772724f582ef8320ac68b10b`,
and `cmp` returned `0`. The preserved archive and extracted starter therefore
remain current. No baseline rerun was needed because the official input archive
did not change; the previously successful baseline evidence remains in
`docs/BASELINE_REPRODUCTION.md`.

Devpost Updates still said only to stay tuned. Devpost Resources linked the
public Information Document. Telegram announced the public statement and the
28 August workshop schedule, but no additional Track 2 starter, submission
artifact, recording, or technical clarification was visible at audit time.
