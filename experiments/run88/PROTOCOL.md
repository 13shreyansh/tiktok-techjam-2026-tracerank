# Run88 protocol: majority pairwise rank consensus

Declared and committed: **2026-08-31 18:26:25 SGT**, before any Run88 score.

## Frozen question

Can majority pairwise preference across independent causal sequence-NFM members
improve whole-list ordering more reliably than equal mean within-user rank?

For `shadow_early`, `shadow_middle`, and `shadow_late`, use exactly the three
existing Run83 causal seed archives 2026–2028. The parent is their existing
equal mean within-user percentile-rank consensus. The candidate is fixed:

1. convert each member to within-user percentile ranks;
2. for every candidate pair, award one point to the strict member-majority
   winner or half a point to each side when the vote ties;
3. order candidates by total pairwise points, using mean member rank multiplied
   by `1e-6` only to break an exact Copeland tie.

No model is retrained. No threshold, coefficient, member subset, weight,
calibration, alternative voting rule, or tie-breaker is searched.

## Sequential gates

- A shadow window passes only if candidate primary improves by at least
  `0.0002` on both validation and its later forward split; neither GAUC nor
  nDCG@5 may regress by more than `0.0005` on either split; and no fixed
  activity/date slice may regress by more than `0.001`.
- Require at least two passing windows out of three. Stop once two failures make
  that impossible.
- Only after two-of-three transfer passes, apply the unchanged rule once to the
  six clean Run84 official member archives. Promotion requires at least
  `+0.0002` primary over `0.605374519999571`, no GAUC or nDCG@5 regression, no
  fixed slice loss beyond `0.001`, finite aligned validation/final-row scores,
  and a passing label-blind submission checker.
- Count every wrapper launch. Stop at the gate, convergence, 50 attempts, six
  campaign hours, or any label-boundary/alignment failure.

The supplied official test rows are final judged rows. Their outcomes must not
be loaded, evaluated, summarized, or used for selection. No upload, submission,
push, public release, organizer contact, registration change, or visibility
change is authorized.
