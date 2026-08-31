# Strategic review 006 — Run 3 closeout

## Fresh evidence audit

This review was written after reading the immutable Run 3 records and Run 2
report, without assuming that the most recent model should be kept.

| Family | Early validation gain | Early forward gain | Decision |
|---|---:|---:|---|
| Standalone causal aggregate tree | -0.003108561 | -0.001999920 | reject |
| Neural plus causal aggregates | -0.000165164 | -0.001170516 | reject |
| Latest click/engagement context | +0.000518560 | +0.000256121 | reject |

The third family also reduced the high-activity slice by 0.001382117. None met
the +0.001 family promotion gate, and none demonstrated the >0.002 material
improvement required to keep this campaign open.

## Third-person assessment

An agent optimizing for visible activity would continue tuning the small
positive result. An agent optimizing for winning should not: its effect is
smaller than observed seed variation, its weakest user segment regressed, and
the existing six-seed fallback already obtains most of its gain through
variance reduction. The missing opportunity is not another near-identical
feature on the standard exposure log.

The strongest untested source of genuinely different information is the
authorized KuaiRand random-exposure log. It was collected under random
recommendations rather than the production recommender, so it may reveal user
or item preferences hidden by the standard system's selection bias. This is a
new hypothesis family, not a continuation of Run 3.

## Decision

Stop Run 3 after six counted attempts and zero public-test evaluations. Commit
the code and evidence. Begin a separately bounded Run 4 only after auditing the
random log's schema, overlap, label rates, users, videos, dates, and legal
provenance. The first Run 4 experiment must be a small, leakage-safe auxiliary
signal with paired chronological controls; no random-log feature may use a row
that would be chronologically unavailable to the target impression.

Run 2's exact packaged six-seed rank ensemble remains the protected fallback.
