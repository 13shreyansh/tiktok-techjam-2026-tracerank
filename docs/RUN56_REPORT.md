# Run 56 report: rank-32 hard-pair fine-tune rejected

Run56 applied the previously audited deterministic hard within-user pair
update to the exact Run52 rank-32 repeat-affinity early checkpoint. It used
only training labels, 128,765 pairs from 25,883 usable users, the frozen
learning rate and pair cap, and validation-gated rollback/selection.

Pairwise epoch 1 produced a small validation gain of
`+0.0000582707474815`; epochs 2 and 3 deteriorated. Forward primary changed
`-0.0001621568851012`. GAUC changed `-0.0000530960836893`, nDCG@5
`+0.0001696375786523`, and all slice movements were noise-sized between
`-0.0000462041496362` and `+0.0001079474280712`. The frozen `+0.00025`
continuation gate therefore failed.

The one counted attempt took `45.352509` subprocess seconds and peaked at
`42,110,435,328` bytes RSS. The ignored 3,786,952,349-byte checkpoint SHA-256
is `331d6e70ae1724d9e12b533e38581b2b7f0c7e0e0fb3f4dc8fe1776f4fb6d602`;
the ignored 6,601,075-byte prediction SHA-256 is
`3d95019d09cdd0ebce42efb188ff7de22f85586fc75863f72ed5aa46bdaa9d52`.

No later shadow, official seed, loss/sampler/rate search, or ensemble followed.
Run52 remains protected at local primary `0.6534977984044839`. These are fixed
1/32 development-sample results, not the full benchmark, hidden test,
submission, or leaderboard. No public-test labels or external action occurred;
the campaign continues.
