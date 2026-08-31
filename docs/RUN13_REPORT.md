# Run 13 report: official caption-content history

## Decision

Rejected after one predeclared attempt. The candidate failed the +0.001 paired
validation gate and regressed every current-window robustness slice. It was not
replicated, added to an ensemble, or evaluated on public-test labels. The
protected Run 2 fallback remains unchanged at official validation primary
0.605400885.

## Audited input and method

The exact 7,583-video caption subset was extracted from the official Zenodo
source using a reproducible HTTP range request. URLs, source MD5, local SHA-256,
licence, coverage, and the acquisition command are recorded in
`docs/KUAIRAND_CAPTION_PROVENANCE.md`.

The candidate fitted one label-free character 2-4 gram TF-IDF representation
over the complete item-text catalog, compressed it to 16 dimensions with fixed
seed Truncated SVD, L2-normalized each nonzero vector, and froze the resulting
video table. A learned projection added the same content vector to candidate and
positive-history video representations. All ranking-model settings matched the
Run 8 early parent.

## Results

| Measure | Parent | Caption candidate | Change |
|---|---:|---:|---:|
| Early validation primary | 0.616858721 | 0.616143703 | -0.000715017 |
| Forward validation primary | 0.603960752 | 0.604922771 | +0.000962019 |
| Low-activity primary | 0.627429026 | 0.627198166 | -0.000230860 |
| Medium-activity primary | 0.615288915 | 0.614479690 | -0.000809225 |
| High-activity primary | 0.566792935 | 0.564838460 | -0.001954475 |
| Early-date primary | 0.613376257 | 0.612628919 | -0.000747339 |
| Late-date primary | 0.611074791 | 0.610450757 | -0.000624035 |

The run completed successfully in 176.34 subprocess seconds with maximum RSS
3,878,813,696 bytes. The 16 SVD components explained 0.0810223 of TF-IDF
variance. Scikit-learn emitted divide-by-zero, overflow, and invalid-value
warnings inside randomized SVD; final vectors and predictions remained finite.
This is disclosed as a reproducibility and numerical-stability caveat.

Exact command, stdout/stderr tails, hashes, metrics, slices, resource use, and
the public-test lock are stored in `experiments/run13/ledger.jsonl`. Large input
and output artifacts remain ignored.
