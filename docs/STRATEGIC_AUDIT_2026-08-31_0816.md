# Strategic audit — 2026-08-31 08:16 SGT

Run59 shows initialization variance was only a minor part of rank 64's deficit;
the capacity branch is closed. During its implementation test, a separate
correctness defect became observable: the model intended to zero each field's
unknown/missing embedding row, but `weight[index_tensor].zero_()` modified an
advanced-indexing copy rather than the parameter. Unknown rows therefore began
with arbitrary random latent values.

Run60 corrects that operation with in-place `index_fill_` while keeping the
protected Run52 rank-32 configuration exact. The unknown rows are initialized
neutrally but remain trainable, preserving aggregate evidence from missing and
unseen values. This tests removal of random initial bias without masking any
field or deleting learned signal.

No rank, initialization scale, learning rate, feature, optimizer, objective,
regularizer, or rescue setting may vary. The corrected implementation was
committed before scoring, source SHA-256 is
`a67dff6a4010eadd7db15942a019bdb082378562461ed32a6887d08c39729e7e`,
and all 58 tests pass. Run52 remains protected.
