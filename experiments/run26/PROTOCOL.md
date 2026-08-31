# Run 26 protocol: KuaiRand-27K recent item/author trend

Started: **2026-08-29 23:41 SGT**.

## Independent question

Can recent three-day video and author exposure/long-view statistics improve the
protected cumulative causal user-item model by representing short-lived trend
and quality drift?

## Fixed representation and first candidate

- Exact Run 24 causal user history and cumulative prior-day item/author fields.
- Add four fields over the fixed last three eligible calendar days: video count
  log2, video long-view rate, author count log2, and author long-view rate.
- Count cap 15 and Beta(1,3), 21-bin rate buckets match the existing causal
  encoding. The window length is fixed before any Run 26 score and is not
  searched.
- Training rows see only the preceding three days. Validation/forward windows
  freeze the final three training days at the split cutoff.
- First score: `shadow_early`, rank-8 sparse FM, seed 2027, otherwise unchanged.
- Paired parent: Run 24 attempt 21. No window, prior, field, or optimizer sweep.

## Gates and limits

Require +0.001 validation primary, no more than -0.0005 forward, and no
unexplained slice regression beyond -0.001. Passing candidates repeat unchanged
on middle and late; require two of three before three paired official seeds.
Stop at family failure, official epsilon 0.002 / N=3 convergence, 50 attempts,
or six hours.

Run 26 is separately declared and cumulatively disclosed; no organizer-approved
reset is claimed. No public-test/hidden label evaluation, submission, upload,
push, contact, credential use, registration change, or public release. All
protected candidates remain immutable.
