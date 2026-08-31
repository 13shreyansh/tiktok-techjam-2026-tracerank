# Run 22 protocol: KuaiRand-1K additive wide user crosses

Started: **2026-08-29 20:49 SGT**.

## Independent question

Can exact user-category preferences transfer when they are restricted to
additive wide corrections rather than allowed to form higher-order latent
interactions? Run 21's unrestricted cross fields improved nearby validation but
failed forward, consistent with excessive interaction capacity.

The fixed model keeps the proven eight-field content FM latent interactions.
The four explicit user × tag/type/duration identities receive linear weights
only; their latent vectors are never read in the forward pass.

## Fixed first candidate

- Exact Run 21 cross encoder, but `wide_cross_fm` architecture.
- Sparse content FM interactions over eight base/content fields plus four
  additive cross weights.
- Chronological `shadow_early`, rank 16, seed 2027, learning rate 0.001, batch
  65,536, at most 20 epochs, patience 4.
- Paired parent: Run 16 attempt 8 content sparse FM.
- No cross subset or parameter will be selected after viewing a score.

## Gates and limits

A unit test must prove cross latent vectors cannot affect scores. The first
shadow must improve primary by at least 0.001, lose no more than 0.0005
forward, and avoid an unexplained slice regression larger than 0.001. If it
passes, repeat unchanged on middle and late; require two of three windows
before official validation. Stop at the family gate, official epsilon `0.002`
/ `N=3` convergence, 50 attempts, or six hours.

No public-test label evaluation, hidden-test access, submission, upload, push,
contact, credential use, registration change, or visibility change. Protected
KuaiRand-1K score `0.6537467530366082` remains immutable.
