# Strategic review 000 — diversity before complexity

## Evidence synthesis

- KuaiRand's paper identifies random-exposure debiasing, long sequential
  modeling, and multitask learning as intended directions. Runs 3, 4, and 7
  tested these categories without robust promotion.
- Industrial multitask references report value but also task conflict and
  instability. The local watch-ratio and click auxiliary tasks did not improve
  the selected target, so a larger MMoE-style system is not justified yet.
- User-listwise softmax and BPR were tested directly in Run 5 and reduced their
  pointwise checkpoints. Final slate diversity is outside the challenge.
- Run 6's hour-plus-weekday model gained 0.001240 on early validation and
  improved all five robustness slices, but lost 0.000693 forward. This is the
  only rejected candidate with broad complementary gains.
- Run 2 found that within-user rank averaging across genuinely different seeds
  produced the strongest official validation candidate.

## Decision

Use the autoresearch rule to revisit a near-miss only for demonstrated diversity.
Freshly reproduce parent and temporal predictions, then test exactly one
equal-weight within-user rank blend. Do not search blend weights on validation.
