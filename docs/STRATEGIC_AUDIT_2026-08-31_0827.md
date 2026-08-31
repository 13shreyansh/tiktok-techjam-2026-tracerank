# Strategic audit — 2026-08-31 08:27 SGT

Run60 shows neutral unknown initialization is cleaner but uniformly weaker;
that branch is closed. The strongest untested low-cost hypothesis is capacity
diversity between the stable rank-16 seed consensus and the protected rank-32
family. This exact composition has not been scored: Run51 combined rank 8 with
rank 16, while Run55 combined Run52 with Run49's mixed rank-8/rank-16 parent.

Run61 assigns one equal within-user rank vote to each capacity group. In each
shadow, the rank-16 side is the already frozen three-seed consensus and the
rank-32 side is the available seed-2027 member. If chronological gates pass,
the official comparison uses the same group structure: one three-seed rank-16
consensus vote and one three-seed rank-32 consensus vote. This avoids giving a
capacity extra weight merely because more member files are available.

All membership, aggregation, ordering, and gates are frozen before scoring.
No subset, weight, calibration, route, seed, rank, or alternative aggregation
may follow. The six shadow source archives were hash-verified before opening.
Run52 remains protected.
