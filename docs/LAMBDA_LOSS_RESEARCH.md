# Neural LambdaLoss research note

Primary source: Xuanhui Wang, Cheng Li, Nadav Golbandi, Mike Bendersky, and
Marc Najork, *The LambdaLoss Framework for Ranking Metric Optimization*, CIKM
2018: <https://research.google/pubs/the-lambdaloss-framework-for-ranking-metric-optimization/>

The paper formalizes metric-driven pairwise losses and explains the LambdaRank
idea of weighting a positive/negative ordering error by the change in nDCG if
the two items swap rank. Run 11 applies this only as a short fine-tune of the
already strong history neural model; it does not import or redistribute paper
code.

For each sampled training user, the implementation uses up to five positives
and the current model's twenty highest-scored negatives. Its loss mirrors the
official primary metric:

- one half is pairwise logistic loss averaged per user and then weighted by
  that user's number of sampled positives, approximating organizer GAUC;
- one half is pairwise logistic loss weighted by the absolute change in
  binary nDCG@5 caused by swapping the pair, averaged per user.

This differs from the rejected Run 5 objectives: BPR weighted every sampled
pair equally, while listwise softmax spread probability over positives without
using the top-5 discount or the GAUC aggregation rule.
