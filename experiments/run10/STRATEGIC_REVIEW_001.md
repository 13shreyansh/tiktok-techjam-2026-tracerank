# Run 10 strategic review 001

## Fresh-context verdict

Reject and stop. The CWM auxiliary materially worsened every selection view,
so its published watch-time result does not transfer to this fixed official
`long_view` ranking target through the tested auxiliary formulation.

| Measurement | Parent | Candidate | Change |
|---|---:|---:|---:|
| Validation primary | 0.616858721 | 0.613846302 | -0.003012419 |
| Forward primary | 0.603960752 | 0.601552606 | -0.002408147 |
| Low-activity primary | 0.627429026 | 0.625648919 | -0.001780107 |
| Medium-activity primary | 0.615288915 | 0.611311051 | -0.003977864 |
| High-activity primary | 0.566792935 | 0.561873479 | -0.004919455 |
| Early-date primary | 0.613376257 | 0.611097391 | -0.002278866 |
| Late-date primary | 0.611074791 | 0.608007495 | -0.003067296 |

The command returned zero after 296.16 seconds and used 5,373,296,640 maximum
resident bytes. The evaluator checksum was
`ecfde28392eb14fec4f488083251df50624e1af2b86278b962daecfb42d195de`.
Public-test labels were not evaluated.

The result also explains why the upstream reference cannot be copied blindly:
its paper optimizes counterfactual watch time and reconstructs a different
`long_view2` label, while this challenge fixes the native `long_view` label.
Tuning the auxiliary weight or CWM parameters after this broad regression
would be same-window rescue search rather than a new hypothesis.
