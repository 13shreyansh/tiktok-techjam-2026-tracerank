# Strategic review 002 — multi-behavior family result

## Result

Neither action-aware representation met the promotion rule. Adding action bits
to the same long-view history scored 0.615921021 validation and 0.603857279
forward. Selecting any explicit action event for history scored 0.616259575 and
0.603470147. The paired parent remains 0.616920352 and 0.603989244.

## Interpretation

The experiment implemented the workshop clue rather than dismissing it. The
candidate was compared with causally earlier action-marked videos and tags;
click, like, follow, comment, forward, and `is_hate` were all represented.
However, nearly every long view is already a click, and the richest actions are
very sparse. Expanding the history also introduces many clicked-but-short-view
events. The learned action signal did not compensate for that noise.

This does not establish that behaviors are unimportant in a production system.
It establishes that these two bounded encodings do not improve this benchmark
under chronological validation. Continuing to tune rare-action weights on the
same window would be validation mining.

## Autoresearch decision

Apply the upstream simplicity and keep/discard rule: discard both candidates,
keep the smaller parent, log the failures, and move to an independent
hypothesis family. Do not repeat user-listwise or pairwise losses; Run 5 already
showed both lower their own pointwise checkpoints. Do not implement final-slate
diversity because the organizer explicitly places re-ranking outside this
challenge.
