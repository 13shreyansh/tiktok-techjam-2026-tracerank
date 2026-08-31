# Run 59 report: variance-normalized rank 64 rejected

Run59 corrected the initialization-scale confound in Run53. Rank 64 used
`latent_init_std=0.008408964152537145`, preserving the protected rank-32 FM's
initial dot-product variance; every other feature, optimizer, split, seed, and
evaluation setting was unchanged. All 58 tests passed before scoring.

The one attempt completed successfully. Normalization improved early primary
only `+0.0000618384191967` over unnormalized Run53, while remaining
`-0.0006031548353358` below exact Run52. Forward primary was
`-0.0001996377400483` below Run52 and `-0.0000842095639938` below Run53.
Versus Run52, GAUC regressed `-0.0005659334909706`, nDCG@5 regressed
`-0.0006403761797010`, and all fixed slices regressed.

The subprocess took `805.203233` seconds and peaked at `45,375,324,160` bytes
RSS. The ignored 7,431,533,965-byte checkpoint SHA-256 is
`0b9aa1ff1e85ce2d69bb571eb4e1d0b967edef53f9b04bc8e4400ce7f5624629`;
the ignored 6,614,981-byte prediction SHA-256 is
`f2e24e3951e3838bc822e5f1b9f5343f721aea376c021dfcf495a01b6a7d28ab`.

This corrected comparison closes rank-64 capacity without middle, late,
official, other-rank, alternate-initialization, or consensus search. Run52
remains protected at local primary `0.6534977984044839`. These are fixed 1/32
development-sample results, not the full benchmark, hidden test, submission,
or leaderboard. The 72-hour optimization campaign continues in a new bounded
run.
