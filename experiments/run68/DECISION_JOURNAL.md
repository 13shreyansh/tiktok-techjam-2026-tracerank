# Run 68 decision journal

## 2026-08-31 09:10 SGT — midpoint checkpoint frozen

- A fresh strategic audit selected one fixed half-pass checkpoint because
  protected rank-32 learning curves peak at the first scored full pass.
- Use the seed-defined permutation prefix, not a hand-selected or
  validation-selected subset.
- Begin with seed-2027 early only. Preserve Run52.
- All 64 tests passed before opening the run.

## 2026-08-31 09:12 SGT — midpoint checkpoint gate fails

- Attempt 1 completed successfully in `77.320852` seconds with
  `28,638,707,712`-byte peak RSS.
- Early primary regressed `-0.0034939040967517654`, GAUC
  `-0.0028782767651519547`, nDCG@5 `-0.004109531428351576`, and forward
  primary `-0.003366629552301492` versus exact Run52.
- Every fixed slice regressed: cold/low `-0.003548313504587397`, medium
  `-0.00238321817656284`, high `-0.005253312527342957`, early dates
  `-0.0029485854155779645`, and late dates `-0.002683260104284879`.
- The ignored 3,786,952,285-byte checkpoint SHA-256 is
  `087c04f27e681bedc051a8fb5bce27a48b7e31499ef95bf05b8c72c69d6098e2`;
  the ignored 6,610,005-byte prediction SHA-256 is
  `bb7170596b512d2848fa684ce1fbda09b57d57365025aef422e4694dc34133d4`.
- Stop the fractional-epoch family. Do not test another fraction, learning
  rate, seed, later window, or interpolation.
