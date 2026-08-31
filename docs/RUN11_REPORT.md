# Run 11: neural LambdaLoss audit

Run 11 fine-tuned the strong target-aware history model with a metric-driven
pairwise loss. Its two halves approximated the organizer primary: positive-
weighted per-user pair loss for GAUC and swap-weighted binary nDCG@5 loss.

The first LambdaLoss epoch reduced its own pointwise checkpoint from
0.616981924 to 0.616863608, so patience stopped training and restored the
pointwise state. That restored result scored 0.616981924 versus the separately
run paired parent's 0.616858721 (+0.000123203), while forward validation changed
by only +0.000021100. The apparent gain is below the +0.001 gate and arises
before the new loss, so it is treated as run variation rather than progress.

The attempt used 390.93 wall seconds and 16,949,690,368 maximum resident bytes.
No public-test labels were evaluated. No learning-rate, pair-count, or metric-
weight search followed. The protected fallback remains the exact Run 2
six-seed within-user rank ensemble at 0.605400885.
