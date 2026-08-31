# Strategic review 004 — Run 4 closeout

## Fresh evidence audit

| Family | Standard gain | Random gain | Decision |
|---|---:|---:|---|
| Remove explicit FM crosses | +0.000058055 | -0.003163785 | reject |
| User/video embedding dropout | +0.000204027 | -0.001672864 | reject |
| Watch-ratio auxiliary task | +0.000328422 | -0.000573814 | reject |

Every attempted robustness intervention marginally improved the standard split
but harmed the organizer-recommended random validation. None achieved the
+0.002 random-validation gate.

## Third-person assessment

Continuing to tune regularization or auxiliary weights would optimize a trend
opposite to the campaign objective. The correct conclusion is not that random
validation is useless: the parent scored 0.388762, materially above the
0.309854-0.311760 random-score range. Rather, its signal comes from more than
simple ID memorization, and the tested regularizers removed useful structure.

## Decision

Stop Run 4 after four counted attempts and zero public-test evaluations. The
next high-upside hypothesis is an efficient ranking-aligned objective. The
organizer ranks pairwise/listwise losses first among unexplored directions; the
previous listwise code timed out because it processed every row in every user
list. A new campaign may test capped positive/negative samples per user with
vectorized mini-batches, preserving the unchanged pointwise parent and exact
fallback.
