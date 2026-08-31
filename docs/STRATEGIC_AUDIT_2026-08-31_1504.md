# Strategic audit — 2026-08-31 15:04 SGT

## Required-benchmark priority correction

The official statement makes KuaiRand-Pure required and labels 1K/27K optional
bonus benchmarks. The protected Pure candidate improves published validation
primary by only `0.0038008850`, while the protected 27K branch has already
survived extensive optional-benchmark research. Expected judging value is now
higher on Pure than on another 27K family.

## Protected-candidate caveat

The six-member Pure rank ensemble deliberately mixes three legacy Run1 members
with three members trained using fully chronological causal histories. Run1 did
not use validation labels, but one training example could see a later training
interaction because the CSV is not globally chronological or user-contiguous.
The legacy members add diversity, yet they are the largest unresolved hidden-
transfer risk in the required candidate.

Run82 tests one fixed correction: retain the exact causal architecture and
existing corrected seeds 2026–2028, train three additional corrected seeds
2029–2031 with the identical official command, then average within-user ranks
across all six causal members. All six are included; no member, weight, epoch,
feature, history length, architecture, or seed is selected after scoring.

## Third-person goal check

This experiment can improve the required score while removing a real
provenance caveat. Its risk is that legacy/causal diversity—not merely seed
variance—causes the current gain. Require stable individual members and a fixed
six-causal consensus improvement with metric and slice safety; otherwise keep
the exact protected mixed ensemble. Public-test labels remain locked. This is
validation evidence, not hidden-test or submission evidence.
