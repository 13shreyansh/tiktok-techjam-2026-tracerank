# Run 84 protocol: label-blind clean-room Pure reconstruction

Declared: **2026-08-31 17:05 SGT**, before any Run84 model execution.

## Purpose and fixed construction

Run84 does not search a new model family. It reconstructs the validation-selected
Run82 architecture through the corrected final-test boundary, from fresh model
initialization and without reusing any historical checkpoint or prediction.

Exactly six members are fixed in advance: seeds `2026`, `2027`, `2028`, `2029`,
`2030`, and `2031`. Every member uses the official split and the exact causal
sequence-NFM settings previously selected only from development evidence:

- training labels: `long_view` from standard 8–21 April rows only;
- validation labels: standard 22–28 April rows only;
- final-test rows: feature-only 29 April–8 May records;
- history: within-user chronological, last 20 positive long-view videos and
  tags, dot attention;
- embeddings 16, hidden units 128, dropout 0.2, neural FM term;
- batch 4096, AdamW rate 0.0005, weight decay 0.00001;
- at most 12 epochs, validation patience 4, Apple MPS;
- final construction: equal mean of within-user percentile ranks across all
  six members. No subset, weight, blend, seed, epoch, or feature search.

The random-exposure log and KuaiRand-1K/27K are prohibited from training or
initialization. No historical model/prediction artifact is an input.

## Predeclared gates and stopping

- Planned floor: seven successful attempts (six fresh members and one fixed
  consensus). Construction failure stops the run and preserves no candidate.
- Convergence declaration: epsilon `0.00005`, window `N=3`, minimum floor 7.
  Because this is a finite construction rather than iterative model search, the
  run stops immediately when the seventh fixed attempt passes; it does not add
  artificial post-construction attempts merely to fill a convergence window.
- Hard stops remain 50 attempts and six hours. Every failed attempt consumes
  both limits but does not advance or reset the convergence window.
- Each member must exit zero, explicitly report that official test outcomes were
  not loaded, produce finite aligned validation/test arrays, and score at least
  `0.6035` validation primary.
- The six-member consensus must score at least `0.6053`, with GAUC at least
  `0.6723`, nDCG@5 at least `0.5380`, and no fixed robustness slice below the
  previously accepted Run82 reference by more than `0.001`.
- The feature-only submission checker and label-boundary unit test must pass.
- The validation-best checkpoint at stop is the scored checkpoint. Final-test
  outcomes are never scored locally.

No upload, submission, push, repository visibility change, or organizer contact
is authorized by this protocol.
