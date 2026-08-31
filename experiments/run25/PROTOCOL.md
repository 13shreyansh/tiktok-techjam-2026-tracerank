# Run 25 protocol: KuaiRand-27K causal multi-behavior item quality

Started: **2026-08-29 23:32 SGT**.

## Independent question

Can earlier strong feedback (like, follow, comment, or forward) and hate rates
for each video and author improve the protected causal user-item history FM?
This directly tests official behavior fields highlighted in the workshop; it
does not retune Run 24's count or long-view-rate buckets.

## Fixed representation and first candidate

- Exact Run 24 user history plus prior-day video/author exposure count and
  long-view-rate fields.
- Add exactly four Beta(1,3), 21-bin categorical rates: prior-day video strong,
  video hate, author strong, and author hate.
- Strong feedback is the fixed logical OR of like, follow, comment, and forward.
- Training rows use earlier calendar days only; validation and forward state
  freezes at the training cutoff. Post-April-28 outcomes remain inaccessible.
- First score: `shadow_early`, rank-8 sparse FM, seed 2027, learning rate 0.001,
  batch 65,536, at most 20 epochs, patience 4.
- Paired parent: Run 24 attempt 21. No behavior subset, rate prior, or bucket
  sweep is allowed.

## Gates and limits

The first shadow must improve primary by at least 0.001, lose no more than
0.0005 forward, and avoid an unexplained slice regression larger than 0.001.
If it passes, repeat unchanged on middle and late; require two of three windows
before three paired official seeds. Stop at family failure, official epsilon
0.002 / N=3 convergence, 50 attempts, or six hours.

This run is separately declared but also included in cumulative Track 2
accounting; no organizer-approved reset is claimed. No public-test/hidden label
evaluation, submission, upload, push, contact, credential use, registration
change, or public release. Protected Pure `0.605400885`, 1K `0.653746753`, and
27K-sample `0.630624629` candidates remain immutable.
