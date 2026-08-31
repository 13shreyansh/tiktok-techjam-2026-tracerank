# Run 75 report: frozen video-profile consensus rejected

Run75 tested a materially new recommender mechanism without retraining Run52.
For each user, it averaged unit-normalized frozen Run52 video vectors from all
long-view-positive training exposures, then used candidate/profile cosine
similarity to reorder only the parent rank slots held by supported videos.
Unsupported videos retained their exact parent slots. The final score gave one
equal rank vote to the parent and one to the slot-preserving profile vote.

The first frozen gate failed decisively. Versus exact Run52, validation primary
changed `-0.0148223688068639`, GAUC `-0.0172306770585478`, and nDCG@5
`-0.0124140605551800`. Forward primary changed `-0.0084229486199109`, forward
GAUC `-0.0098365973097395`, and forward nDCG@5
`-0.0070092999300823`. Every fixed slice regressed: cold/low activity
`-0.0150560108441291`, medium `-0.0146357731594104`, high
`-0.0153969365590679`, early dates `-0.0187810747725783`, and late dates
`-0.0121832853933422`.

The training-only profile used 10,582,174 positive exposures from 25,904
users. It supported 422,189 validation rows from 23,470 users and 300,735
forward rows from 23,810 users. The result shows the FM's latent video vectors
are useful interaction parameters but their cosine geometry is not a reliable
item-similarity space. No repeat, later window, official seed, profile variant,
weight change, or route is justified.

The counted command exited zero in `10.479538` wrapper seconds and peaked at
`6,708,346,880` bytes RSS. The ignored 4,303,105-byte prediction SHA-256 is
`9cb0251c63ee1f3f3e48d3de386ec554a811e20fbba8050267533f04947fc46c`.
The exact input checkpoint and parent prediction SHA-256 values were
`a55600b5348abcf1d959576efbcbd0b7612c4d3dadd03d7cb479cbe077cdf3d8`
and `8d2392915731af585177bbb79287fc391629dea2fbce9f1faab0c965db911872`.

Run52 remains protected at local primary `0.6534977984044839`. These are fixed
deterministic 1/32 development-sample metrics, not the full benchmark, hidden
test, submission, or leaderboard. Closing Run75 closes only this hypothesis;
the 72-hour campaign continues.
