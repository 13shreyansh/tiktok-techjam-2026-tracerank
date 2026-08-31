# Strategic review 000 — efficient ranking alignment

## Fresh evidence

- The organizer starter explicitly ranks pairwise/listwise loss first among its
  untested directions because pointwise logloss is misaligned with GAUC and
  nDCG@5.
- Run 1's BPR fine-tune completed but did not improve the selected neural
  history model.
- Run 2's listwise pass timed out after 602 seconds. It processed every
  impression for every eligible user for up to three epochs and therefore did
  not provide a competitive score.
- The listwise implementation restores the best pointwise checkpoint when a
  fine-tune does not improve, protecting against destructive updates.

## Third-person decision

The missing experiment is not another unbounded retry. Cap each user list to
five positives and twenty negatives sampled afresh per epoch, use larger user
mini-batches, and begin with two fine-tuning epochs. This directly preserves
the per-user softmax objective while reducing its row count to at most about
650,000 per epoch.

Reject quickly if the first early-window attempt cannot beat its freshly
reproduced parent by 0.001 or harms the forward window by more than 0.0005.
