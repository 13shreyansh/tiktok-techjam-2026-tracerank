# Run 82 decision journal

## 2026-08-31 15:04 SGT — fully causal replacement frozen

- Refocus from optional 27K to required Pure after Run81 closed.
- Fix seeds 2029–2031 before scoring and require all three; retain existing
  corrected seeds 2026–2028. The exact protected mixed ensemble is untouched.
- Use official validation because the causal architecture already survived
  Run2 chronological screens; this run tests seed expansion and provenance
  correction, not a new architecture.

## 2026-08-31 15:06 SGT — attempt 1 construction failure; identical retry allowed

- Attempt 1 stopped before training, scoring, model creation, or prediction
  creation. In the sandbox, PyTorch was built with MPS but reported it
  unavailable; the legacy `--device auto` branch then passed literal `auto` to
  `torch.device` and raised `RuntimeError`.
- A read-only check outside the sandbox reports MPS built and available. Permit
  one new-ID retry of seed 2029 outside the sandbox with the byte-identical
  command, model source, configuration, seed, outputs, and gates. This is an
  execution-environment correction, not a model attempt reinterpretation.
- Attempt 1 remains counted and immutable. If the identical retry fails, close
  Run82 without trying CPU or altering any model setting.

## 2026-08-31 15:59 SGT — identical seed-2029 retry passes member gate

- Attempt 2 ran the frozen command on MPS and exited zero. Best epoch 4 scored
  GAUC `0.67185378074646`, nDCG@5 `0.537631094455719`, and primary
  `0.6047424077987671`, above the `0.6035` member floor.
- Checkpoint: 3,579,912 bytes, SHA-256
  `dd31f120dca89a87ed199ee88293e3011744acabacdfdcf1d5495b1a197427da`.
  Prediction archive: 1,075,638 bytes, SHA-256
  `09c72e4819dedb693fae30d7bc2d0ccadc367d89a0186f6ea9bc7ac0c9426e53`;
  its 124,909 validation and 170,588 unlabeled-test float32 rows are finite.
- Continue unchanged to predeclared seed 2030. No ensemble has been scored.

## 2026-08-31 16:00 SGT — seed 2030 passes member gate

- Attempt 3 exited zero. Best epoch 4 scored GAUC `0.6712960600852966`,
  nDCG@5 `0.5376946330070496`, and primary `0.6044953465461731`, above the
  `0.6035` member floor.
- Checkpoint: 3,579,912 bytes, SHA-256
  `72dbf9905c66fcd0e2f69964580a1adff520b001d225dafd5436a79f554b37f3`.
  Prediction archive: 1,075,174 bytes, SHA-256
  `b7d6b547c74a502492cd6d6ce90bc87be1f300033951d685efd22d874360bd1b`;
  both arrays are aligned finite float32.
- Continue unchanged to predeclared seed 2031. No ensemble has been scored.

## 2026-08-31 16:01 SGT — seed 2031 and six-member stability gate pass

- Attempt 4 exited zero. Best epoch 4 scored GAUC `0.6713388562202454`,
  nDCG@5 `0.5375301241874695`, and primary `0.6044344902038574`, above the
  `0.6035` member floor.
- Checkpoint: 3,579,912 bytes, SHA-256
  `0c2a411fa1d876b6d4eed33597458cad790186d605fb0a71eafa0ef76b1fec1f`.
  Prediction archive: 1,074,985 bytes, SHA-256
  `eef6d03dc48c446a2b5bcca111d72615cbf4fc9eeb63040319d6e59525e1f2da`;
  both arrays are aligned finite float32.
- Corrected seeds 2026–2031 span primary `0.6041800975799560` to
  `0.6047424077987671`, width `0.0005623102188111`, below the `0.002` gate.
  All member prerequisites pass. Score the one fixed six-causal rank consensus
  next; do not score a subset or alternate weighting.

## 2026-08-31 16:06 SGT — safer alternate preserved but not promoted

- Attempt one failed before model construction because the sandbox hid MPS and
  the legacy `auto` branch passed the literal device name. The exact retry was
  still counted and ran with the repository's already documented environment.
- Seeds 2029, 2030, and 2031 succeeded at primary `0.6047424077987671`,
  `0.6044953465461731`, and `0.6044344902038574`. All exceeded the member floor;
  the six-causal member span was `0.0005623102188111`.
- The predeclared six-causal consensus reached GAUC `0.6727584132959411`,
  nDCG@5 `0.5382840360094916`, and primary `0.6055212246527164`. Relative to
  the protected mixed ensemble, this is `+0.0003793181655405`,
  `-0.0001386389360551`, and `+0.0001203396147427`, respectively.
- All slice limits passed. Primary deltas were cold/low `+0.0002657950720065`,
  medium `+0.0006487423536874`, high `-0.0003317436574168`, early dates
  `-0.0000152311667896`, and late dates `-0.0001402559032749`.
- The primary gain missed the frozen `+0.0002` gate by
  `0.0000796603852573`. Close without member, subset, weight, seed, epoch, or
  blend search. Preserve the causal archive as a provenance-safer alternate,
  but keep the exact mixed ensemble as the protected fallback. Public and
  hidden labels remain untouched; closing Run82 does not end the campaign.
