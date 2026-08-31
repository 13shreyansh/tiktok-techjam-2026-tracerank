# Run 24 protocol: KuaiRand-27K memory-bounded FM anchor

Started: **2026-08-29 21:29 SGT**. The six-hour clock includes deterministic
sampling and cache construction before the first scored iteration.

## Independent question

Can the same organizer-defined `long_view`, GAUC, and nDCG@5 task be evaluated
trustworthily on the optional KuaiRand-27K benchmark within the local 64 GiB
Apple workstation, without full-month statistic leakage or CUDA-only reference
code?

No organizer 27K baseline, hidden route, checker, or bonus formula is published.
Run 24 therefore establishes a clearly scoped local anchor; it cannot claim a
full-benchmark or hidden-test score.

## Fixed data protocol

- Verified archive: 9,892,191,178 bytes; official MD5
  `3e3c799a24e2d23a4d2c757fbf9adf59`; SHA-256
  `b8a8a5b777e564202cff6b96676959ee0d6baccc7ad7376bcb4af6767362d41b`.
- Deterministic SplitMix64 hash sample on `(user_id, video_id, time_ms)`, residue
  0 modulo 32. This was fixed before any 27K score.
- Development dates only: April 8-21 for training and April 22-28 for
  validation. Rows after April 28 are rejected by date without using or
  retaining outcomes.
- Basic item metadata is allowed. Full-month item-statistics tables are
  excluded because their official definition crosses the chronological split.
- Only sampled video and author IDs are mapped into the embedding space;
  reversible source-ID arrays are retained in ignored cache artifacts.

The modulus targets approximately the already-stable 1K row budget while
preserving all 27,285 users in expectation. Actual counts are recorded only
after the sampler succeeds.

## Fixed first anchor

- Five-field sparse FM: user, sampled video, sampled author, tab, and duration.
- Rank 8, seed 2027, learning rate 0.001, batch 65,536, at most 20 epochs,
  patience 4.
- First score: chronological `shadow_early`; then unchanged middle and late
  shadows if execution is sound.
- The anchor has no 27K parent score and is not a promotion candidate by itself.
  A content FM may be compared only after the anchor exists.

## Gates and limits

An improved family must beat its paired anchor by at least 0.001 primary, lose
no more than 0.0005 on the fixed forward window, and avoid an unexplained slice
regression larger than 0.001. Require two of three chronological windows before
official validation and three unchanged seeds before promotion. Stop at family
failure, official epsilon 0.002 / N=3 convergence, 50 attempts, or six hours.

No public-test label evaluation, hidden-test access, submission, upload, push,
contact, credential use, registration change, or visibility change. Protected
Pure `0.605400885` and 1K `0.653746753` candidates remain immutable.
