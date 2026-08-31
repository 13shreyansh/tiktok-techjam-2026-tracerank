# Run 68 report: fixed half-pass checkpoint rejected

Run68 tested whether the protected rank-32 repeat-affinity FM peaks before its
first complete pass. It trained on exactly the deterministic first half of the
seed-2027 permutation with every other Run52 setting unchanged. The one
fraction and all gates were frozen before scoring, and all 64 tests passed.

The single attempt completed successfully but regressed early primary
`-0.0034939040967517654`, GAUC `-0.0028782767651519547`, nDCG@5
`-0.004109531428351576`, and forward primary `-0.003366629552301492` versus
exact Run52. Every fixed slice regressed; high activity was worst at
`-0.005253312527342957`.

The attempt took `77.320852` seconds and peaked at `28,638,707,712` bytes RSS.
The ignored 3,786,952,285-byte checkpoint SHA-256 is
`087c04f27e681bedc051a8fb5bce27a48b7e31499ef95bf05b8c72c69d6098e2`;
the ignored 6,610,005-byte prediction SHA-256 is
`bb7170596b512d2848fa684ce1fbda09b57d57365025aef422e4694dc34133d4`.

The latter half of the first pass supplies material signal, so the
fractional-epoch family closes without alternate fractions, later windows,
official seeds, or interpolation. Run52 remains protected at local primary
`0.6534977984044839`. These are fixed 1/32 development-sample results, not the
full benchmark, hidden test, submission, or leaderboard. The 72-hour campaign
continues with a different hypothesis.

## Retrospective parent-drift correction

Run72 later proved that Run60's neutral unknown-row initialization remained the
default. Run68's half-pass candidate therefore also inherited that change. It
remains decisively rejected versus exact Run60 at `-0.003111295128201408`
validation, `-0.003046081487439789` forward, and
`-0.004621535081916983` worst slice; the result is not presented as an isolated
fractional-pass effect.
