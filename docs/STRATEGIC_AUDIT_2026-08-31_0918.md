# Strategic audit — 2026-08-31 09:18 SGT

## Remaining organizer-aligned gap

Run68 rules out stopping halfway through the protected first pass. The
strongest materially new clue is the workshop's outcome funnel: impressions
lead to clicks, then deeper outcomes. On the exact early training split,
`long_view` prevalence is `0.2580331681`, click prevalence is `0.3761665007`,
and `P(click | long_view)` is `0.9927932578`. Long view is therefore almost,
but not perfectly, downstream of click.

Prior runs used click as history context or an auxiliary target on an older
neural Pure model. They did not train the protected 27K rank-32 FM as an
entire-space probability funnel. The primary ESMM paper models sequential
actions by learning click probability and a conditional downstream probability,
then multiplying them over all impressions:
<https://arxiv.org/abs/1804.07931>.

## Run69 decision

Use the protected Run52 fields and rank with one shared sparse FM interaction
representation, a conditional-long-view linear head, and a click linear head.
Train the unweighted sum of click BCE and joint-long-view BCE, where
`P(long_view)=P(click)*P(long_view|click)`. Rank by log joint probability. No
auxiliary coefficient or task subset is introduced.

## Risks and third-person check

The funnel assumption is violated by about `0.72%` of long-view positives.
Shared interactions may also create task conflict, and an extra sparse linear
head increases memory. Require validation and forward transfer, both metric
components, every fixed activity/date slice, and the 60 GB guard before any
later window. Run52 remains untouched.

An independent reviewer would consider this a distinct, high-value test: it
uses an official logged action, directly matches the workshop funnel, follows
a primary published method, and has no tuned auxiliary weight. It is still
development-sample evidence, not hidden-test or leaderboard evidence.
