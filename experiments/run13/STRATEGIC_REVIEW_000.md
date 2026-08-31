# Run 13 strategic review 000

Caption content is a materially different signal from the previously rejected
category path: it preserves fine-grained semantics and can connect related
videos whose organizer tags differ. It also directly addresses the workshop
clue that the task should use a person's watched sequence rather than score
each video in isolation.

The main risk is that a compact 16-component representation destroys useful
text detail or that the trainable projection is too weak to influence ranking.
The opposite risk is spurious early-window improvement from text distribution
shift. Therefore one representation is frozen before any score is observed,
and promotion requires both the paired early validation gate and forward/date/
activity robustness. The full catalog text is used without labels; this is an
explicit unsupervised item-content assumption available at inference time.
