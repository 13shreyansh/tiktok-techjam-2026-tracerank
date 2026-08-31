# Submission narrative draft — not submitted

## What we built

We built an autonomous experimentation system for impression ranking on
KuaiRand-Pure. Instead of treating every video independently, the model asks a
simple TikTok-like question: how similar is this candidate to the videos this
person recently watched for a meaningful amount of time? A neural factorization
machine combines user, video, author, tag, context, and duration information
with attention over the person's last 20 positive viewing events.

Our final local candidate is an ensemble of six independently trained models.
Each model's scores are converted to ranks separately inside each user's list,
then averaged. This matches the evaluator's user-grouped ranking objective and
reduces the effect of one unlucky training seed. On official validation it
scores GAUC 0.672521, nDCG@5 0.538228, and primary 0.605375, compared with the
published FM primary 0.6016.

## Autonomous research process

The agent began from the untouched organizer baseline, preserved the evaluator,
and logged every success and failure with its exact command, code hash, time,
memory, metrics, and decision. It used chronological shadow windows and user/
date robustness slices before promotion. When a method improved one slice but
failed forward in time, the agent rejected it rather than optimize the visible
validation set.

The research covered every organizer-prioritized direction: pairwise/listwise
losses, user-history models, multi-action targets, censored watch time, deeper
feature crosses, temporal drift, and unbiased random-exposure validation. It
also audited official category and caption resources. Negative results remain
in the repository as reproducible evidence.

## Innovation, impact, and feasibility

The technical contribution is not simply a larger network. It is a leakage-
audited causal history representation plus user-relative rank consensus, inside
an agent loop that knows when not to promote fragile gains. The system runs on
one Apple M5 Pro laptop without cloud accelerators or API secrets, and the final
CSV passes the organizer's exact row-alignment checker.

For a short-video feed, better ranking means surfacing more personally relevant
videos among already retrieved candidates. This can reduce irrelevant swipes
without requiring a costly full-catalog model. The same audit pattern—temporal
splits, subgroup checks, immutable ledgers, and stop gates—transfers to other
recommendation benchmarks.

## Truthful limitations

The 0.605375 value is validation, not final-test performance. A historical
0.605521 validation reference is quarantined because its loader materialized
final-test outcomes before the organizers clarified the boundary; the clean
protected candidate was rebuilt without loading or scoring those outcomes.
The live statement caps each benchmark run, not all research globally.
Run2 produced the preserved mixed fallback in 37 attempts and 3,172.35
seconds; Run82 froze the selected all-causal artifact in five attempts and
Run83 selected it in a 24-attempt chronological audit. For full transparency
we will disclose all 344 executions. Run16 had 18
executions but only 16 were convergence-eligible; the two post-convergence runs
are excluded and disclosed. Run 17 added one predeclared, rejected DeepFM
attempt. Run 18 added one predeclared, rejected field-aware FM attempt.
Run 19 added one predeclared within-user BPR attempt that improved forward
validation but failed its validation and slice gates.
Run 20 added one failed encoder execution and one rejected causal
sequence-profile result.
Run 21 added one explicit-cross result that improved nearby validation but was
rejected for forward and high-activity overfit.
Run 22 added one additive-wide-cross result that improved all validation slices
but was rejected by the forward guard.
Run23 added one fixed-shrinkage wide-cross result that remained unsafe forward
and closed the branch without a coefficient sweep. Run86 later added one
pre-model MPS-sandbox failure and one rejected task-protected click result.
Run87 added one rejected cross-fit LambdaMART residual: it improved its meta
window but regressed on the independent target and forward windows.
Run88 added two rejected majority-pairwise list-aggregation checks and stopped
after two chronological failures made its two-of-three gate impossible.
Run89 added one rejected causal self-attention history encoder; both validation
and forward scores collapsed, so the family closed without tuning.
Run90 added one dual-timescale positive-history profile; its small early gain
failed the forward and high-activity gates, so it also closed without tuning.
Run91 added one separate explicit-engagement profile; it improved forward
primary but failed validation and the high-activity floor, so it closed after
one attempt without tuning.
Run92 added one parameter-free best-matching history expert; validation,
forward, and three robustness slices failed, so it closed after one attempt.
Run93 began a fixed seed-saturation audit and logged eight executions. One
automatic-device attempt failed before model execution and seven MPS
subprocesses succeeded; the user froze model search for submission before any
declared consensus or candidate existed.
Run83 compared the two
already frozen Pure artifacts without reopening model search. The boundary between
restarted campaigns, token
input/output split, and final hidden-test identity remain unresolved and must
not be invented.
