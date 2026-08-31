# Official Track 2 FAQ audit — 31 August 2026

Public source: [TikTok TechJam 2026 Information Document](https://bytedance.larkoffice.com/wiki/GdYFwzWNLiREsSkuIjZcDznInWc#Awozdl0mGo1DnXxwFuemYSilyzP)

Observed in the signed-in live Lark page again at **2026-08-31 19:48 SGT**. The
Track 2 section displayed **Added FAQs: 31 August 2026, 1:57 PM**. This audit
uses the public FAQ, not private email content.

## Corrections that change our execution

1. **The supplied test rows are the final judged rows.** There is no separate
   private dataset. The agent may use training and public validation freely,
   then produce one prediction file for the supplied test rows. Test outcomes
   may not be used for training, model selection, early stopping, threshold
   tuning, or feature statistics. Review includes code and run logs; a pipeline
   that uses test outcomes is disqualified.
2. **Convergence is predeclared, not universally fixed at 0.002 for three
   iterations.** A run may predeclare its own epsilon, consecutive-window
   length, and optional minimum-iteration floor. Those values must be fixed
   before execution and logged. The 50-iteration and six-hour caps still apply.
   The scored checkpoint is the validation-best checkpoint when the run stops.
   Failed attempts consume iteration/time budget but do not advance or reset
   the convergence window.
3. **Pure training data is only the 8–21 April standard log.** The random
   exposure log is analysis/EDA-only, not training data. KuaiRand-1K and 27K
   remain separate bonus benchmarks and may not be used for auxiliary training
   or pretraining of the Pure candidate.

## Remaining live-page inconsistency

The public page still visibly contained one Limits-table row saying
`NDCG@10 / Recall@50` and `click = positive` at the time of this audit. That
row conflicts with the current benchmark table, task text, FAQ, starter kit,
evaluator, published reference scores, and deliverables, all of which define
`long_view` ranking with `GAUC` and `nDCG@5` averaged as the primary metric.
We therefore treat the row as stale but preserve the contradiction rather than
claiming it has disappeared.

A fresh live-page find at 19:48 SGT returned one match each for `NDCG@10`,
`Recall@50`, and `nDCG@5`, and displayed the legacy terms in the Limits row.
This is direct public-page evidence that the contradiction remained visible at
that time.

## Operational conclusion

The former “unknown hidden-test route” blocker is resolved. The urgent release
gate is now stronger: final candidate generation and alignment validation must
be label-blind for the supplied 29 April–8 May rows. Historical artifacts that
were created through a loader which materialized those outcomes are not clean
final candidates, even when the outcome values were not intentionally used.
