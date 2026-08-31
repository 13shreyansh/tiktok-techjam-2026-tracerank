# Strategic review 000 — unbiased validation

## Organizer clue

The official starter lists `log_random_4_22_to_5_08_pure.csv` as unexplored
headroom and specifically says it can be used as an additional unbiased
validation set to check whether a model only overfits biased traffic.

## Data audit

- Random log: 1,186,059 rows, 27,285 users, 7,583 videos, April 22-May 8.
- Standard training: 1,141,112 rows, 26,210 users, 7,538 videos, April 9-21.
- Every standard-training user and video appears in the random log, while exact
  user-video pair overlap is only 624 pairs.
- Random long-view rate is 0.084961 versus 0.336620 in standard training;
  random click rate is 0.176158 versus 0.463447.
- Random file SHA-256 is
  `60b80994da969cd53da4d50c37ba3dafd6fb185df804c92c8410df34845a9d2c`.

The large label shift confirms that standard traffic is highly selected. The
tiny exact-pair overlap means the random log is not merely duplicating the
standard impressions.

Five uniform-random scoring audits on the random log produced primary
0.309854-0.311760; constant scores produced 0.311636 and label-oracle scores
produced 0.837328. These are diagnostic bounds, not model attempts.

## Third-person decision

First measure the unchanged causal-history parent on both validation sets. Do
not assume its standard-validation gain transfers to random traffic. Only then
test model changes designed to reduce reliance on exposure-specific IDs, such
as controlled regularization or representation mixtures. Reject any direction
that buys random score by materially harming the official validation metric.
