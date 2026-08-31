# Run 9 strategic review 001

## Fresh-context verdict

Reject and stop this family. The two-layer full-rank cross tower did not
improve the paired official-style validation window and made every recorded
activity/date slice slightly worse. Its later-window gain is useful evidence
that explicit crosses can alter temporal generalization, but it is not enough
to justify selection or parameter search.

## Evidence

| Measurement | Parent | Candidate | Change |
|---|---:|---:|---:|
| Validation primary | 0.616858721 | 0.616292357 | -0.000566363 |
| Forward primary | 0.603960752 | 0.604613423 | +0.000652671 |
| Low-activity primary | 0.627429026 | 0.627165379 | -0.000263647 |
| Medium-activity primary | 0.615288915 | 0.614661144 | -0.000627771 |
| High-activity primary | 0.566792935 | 0.565453014 | -0.001339921 |
| Early-date primary | 0.613376257 | 0.612881564 | -0.000494693 |
| Late-date primary | 0.611074791 | 0.610788467 | -0.000286324 |

The command returned zero after 215.64 seconds. Maximum resident memory was
3,815,112,704 bytes. The evaluator checksum was
`ecfde28392eb14fec4f488083251df50624e1af2b86278b962daecfb42d195de`.
Public-test labels were not evaluated.

## Autoresearch discipline

The result failed the protocol's +0.001 validation requirement. Changing
layer count, projection rank, width, or learning rate after seeing this result
would turn one hypothesis into an unplanned local sweep on the same window.
Run 9 therefore ends after one iteration, while the exact Run 2 six-seed
user-rank ensemble remains the protected fallback at 0.605400885.
