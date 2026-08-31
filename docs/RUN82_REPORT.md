# Run 82 report: fully causal Pure consensus below promotion gate

Run82 addressed the largest provenance caveat in the required KuaiRand-Pure
candidate. The protected six-member ensemble mixes three legacy history
members with three fully chronological causal members. The legacy construction
did not use validation labels, but a training row could see a later training
event. Run82 froze an exact replacement before scoring: reuse causal seeds
2026–2028, train identical seeds 2029–2031, and average within-user percentile
ranks across all six. No seed, member, weight, architecture, feature, epoch, or
blend was chosen after results were observed.

The first counted attempt failed before model construction because the sandbox
hid MPS and the older `auto` branch passed the literal device name. The exact
retry was counted rather than erased. Seeds 2029, 2030, and 2031 then succeeded
at primary `0.6047424077987671`, `0.6044953465461731`, and
`0.6044344902038574`; all cleared the `0.6035` floor. Across causal seeds
2026–2031, the primary span was `0.0005623102188111`, below the frozen `0.002`
limit. The three new checkpoints and valid/test prediction archives are finite,
aligned, and hashed below.

The fixed six-causal consensus reached GAUC `0.6727584132959411`, nDCG@5
`0.5382840360094916`, and primary `0.6055212246527164`. Versus the protected
mixed result (`0.6723790951304006`, `0.5384226749455467`, and
`0.6054008850379737`), the deltas are `+0.0003793181655405`,
`-0.0001386389360551`, and `+0.0001203396147427`. It passed the component
limits and every fixed slice limit: cold/low activity `+0.0002657950720065`,
medium `+0.0006487423536874`, high `-0.0003317436574168`, early dates
`-0.0000152311667896`, and late dates `-0.0001402559032749`. However, its
primary gain missed the precommitted `+0.0002` promotion gate by
`0.0000796603852573`. It is therefore a provenance-safer alternate, not the
promoted candidate. The protected mixed ensemble remains unchanged.

Artifact verification:

- Seed 2029 checkpoint: 3,579,912 bytes, SHA-256
  `dd31f120dca89a87ed199ee88293e3011744acabacdfdcf1d5495b1a197427da`;
  prediction archive: 1,075,638 bytes, SHA-256
  `09c72e4819dedb693fae30d7bc2d0ccadc367d89a0186f6ea9bc7ac0c9426e53`.
- Seed 2030 checkpoint: 3,579,912 bytes, SHA-256
  `72dbf9905c66fcd0e2f69964580a1adff520b001d225dafd5436a79f554b37f3`;
  prediction archive: 1,075,174 bytes, SHA-256
  `b7d6b547c74a502492cd6d6ce90bc87be1f300033951d685efd22d874360bd1b`.
- Seed 2031 checkpoint: 3,579,912 bytes, SHA-256
  `0c2a411fa1d876b6d4eed33597458cad790186d605fb0a71eafa0ef76b1fec1f`;
  prediction archive: 1,074,985 bytes, SHA-256
  `eef6d03dc48c446a2b5bcca111d72615cbf4fc9eeb63040319d6e59525e1f2da`.
- Six-causal archive: 493,479 bytes, SHA-256
  `3ec4fd06fb02ded236264c49954154e7f3e53c1e632afd6674a0fd82144d1a6d`.
  It contains finite `float32` arrays of 124,909 validation and 170,588
  unlabeled test rows.

Run82 used five counted attempts and stopped at the frozen gate. No public-test
or hidden-test labels were evaluated, and nothing was submitted. These are
local official-validation results, not hidden-test or leaderboard evidence.
Closing this hypothesis does not end the broader optimization campaign.
