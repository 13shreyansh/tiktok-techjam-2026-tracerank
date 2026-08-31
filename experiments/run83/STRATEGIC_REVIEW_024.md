# Run 83 strategic review after attempt 24

Reviewed: **2026-08-31 16:35 SGT**.

## Decisive late-window result

Attempts 17–24 completed the frozen `shadow_late` comparison. All succeeded;
the official validation, public test, and hidden test remained locked.

| Measure | Source consensus | Causal consensus | Causal - source |
|---|---:|---:|---:|
| validation primary | 0.5929243443 | 0.5929336492 | +0.0000093049 |
| validation GAUC | 0.6668876869 | 0.6670921482 | +0.0002044613 |
| validation nDCG@5 | 0.5189610017 | 0.5187751502 | -0.0001858515 |
| forward primary | 0.6040430430 | 0.6041838833 | +0.0001408403 |
| forward GAUC | 0.6709289294 | 0.6709547131 | +0.0000257837 |
| forward nDCG@5 | 0.5371571567 | 0.5374130536 | +0.0002558968 |

Paired validation-primary changes are `+0.0006430149`, `+0.0000200868`, and
`+0.0002339482`; all three are positive and their mean is `+0.0002990166`.
Paired forward-primary changes are `+0.0007791519`, `-0.0004150867`, and
`-0.0001872778`, with mean `+0.0000589291`.

Validation-slice primary changes are: cold/low activity `-0.0006832093`,
medium activity `+0.0007928237`, high activity `+0.0001128251`, early dates
`+0.0007298075`, and late dates `-0.0003978953`. All stay above the `-0.001`
floor. The only aggregate component regression is validation nDCG@5 at
`-0.0001858515`, inside the frozen `-0.0005` tolerance. The late window
therefore **supports causal selection**, narrowly but completely under the
precommitted gates.

## Final cross-window decision

- `shadow_early`: supports causal.
- `shadow_middle`: fails because forward primary regresses, without a
  catastrophic floor.
- `shadow_late`: supports causal.

Two of three windows support causal and no window crosses a catastrophic
component, primary, or slice floor. Therefore select the already frozen Run82
six-causal official artifact as the final Pure candidate. Its verified local
official-validation result is GAUC `0.6727584133`, nDCG@5 `0.5382840360`, and
primary `0.6055212247`. The exact Run2 mixed candidate at primary
`0.6054008850` remains an immutable fallback.

This is a provenance/generalization selection, not a claim of a large score
improvement. The selected candidate gains only `+0.0001203396` on official
validation, and hidden-test performance remains unknown. Run83 did not tune or
re-score the official artifact; it supplied independent chronological evidence
for choosing between two previously frozen artifacts.

Cumulative Run83 accounting: 24/50 attempts, 24 successful, 764.313 summed
command-seconds, 3,977,576,448-byte maximum RSS, zero public-test evaluations,
and no submission or upload.
