# Run 11 strategic review 000

Run 11 is not a repeat of ordinary pair/list training. The strong parent is
retained, and only its final representation is fine-tuned with swap weights
derived from the exact top-5 discount while the pairwise component matches the
organizer GAUC aggregation. Hard negatives focus compute on items that can
actually enter the top of the user list.

This is selected after distinct failures: generic LightGBM LambdaRank lacked
the neural history representation; Run 5 BPR/listwise did not weight swaps by
the metric; Run 9 capacity and Run 10 watch-time auxiliary both regressed. The
experiment is one fixed configuration, not a loss sweep.
