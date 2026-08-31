# Strategic audit: Run87 chronological residual rank correction

Recorded: **2026-08-31 18:09 SGT**, before implementation or scoring.

## Residual opportunity

Run85 and Run86 both added real behavioral information but produced the same
failure pattern: roughly `+0.0001` early primary, a small nDCG improvement,
and GAUC/high-activity trade-offs. Further history thresholds, auxiliary
weights, expert counts, or feedback unions would be micro-tuning those closed
families.

The protected model is optimized with pointwise BCE and only converted to
within-user ranks after inference. Earlier BPR, sampled listwise, and neural
Lambda fine-tunes updated the high-cardinality representation directly and did
not improve it. A separate low-capacity residual ranker asks a different
question: can the parent remain frozen while a tree learns repeatable ordering
errors from causally separated parent predictions?

Run76 tested a related residual LambdaMART mechanism on the non-transferable
27K development sample. It improved forward nDCG but missed aggregate
materiality, so Run87 must be both cheaper and more strongly separated in time.
The Pure benchmark has never tested a residual tree trained on out-of-time
predictions from the selected causal ensemble.

## Decision

Freeze one cross-fit correction:

- meta-train: 12--14 April labels and parent predictions from a model trained
  only on 8--11 April;
- meta-validation/early stopping: 15--17 April from the same frozen parent;
- independent opening target: 18--21 April parent predictions;
- inputs: within-user parent percentile rank plus the already audited causal
  aggregate matrix frozen from the corresponding training state;
- objective: user-grouped LightGBM LambdaMART at nDCG@5 with one standard fixed
  configuration and the parent rank supplied as initial score;
- output: parent rank plus learned raw residual; no coefficient, route, feature,
  tree, iteration, or normalization search.

The first scored gate requires both the meta-validation correction and the
independent target window to improve materially. A miss closes the family.
Run84 remains untouched.

