# Run 13 decision journal

## 2026-08-29 16:18 SGT — campaign start

- Protected fallback: official validation primary 0.605400885.
- Exact official-caption Pure subset verified for all 7,583 video IDs.
- One predeclared frozen text representation and one paired early-window test;
  no text representation sweep.
- Winning-goal check: caption semantics are independent content evidence and
  can match related watched videos even when their exact tags differ.

## 2026-08-29 16:23 SGT — attempt 001 rejected

- Candidate validation: 0.616143703, a change of -0.000715017 from the paired
  parent and below the required +0.001.
- Forward validation improved by +0.000962019, but every current-window slice
  regressed: low activity -0.000230860, medium -0.000809225, high
  -0.001954475, early dates -0.000747339, and late dates -0.000624035.
- The successful command used 176.34 wall seconds and 3,878,813,696 maximum
  resident bytes. Public-test labels were not evaluated.
- Scikit-learn emitted overflow/invalid warnings inside randomized SVD. The
  resulting vectors and score were finite, but this adds numerical-risk evidence
  against promotion.
- Decision: reject and stop without tuning vocabulary, n-gram range, SVD width,
  or projection. Preserve the 0.605400885 fallback.
