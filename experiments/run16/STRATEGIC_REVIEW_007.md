# Run 16 fresh-context review — after official sparse-FM ensemble

## Evidence gained

The 1K benchmark is computationally practical and the baseline is stable:
three official seeds scored `0.640000–0.643082`, and their fixed rank ensemble
scored `0.644227425`. This is meaningful independent progress, but the absence
of an organizer 1K baseline or bonus formula prevents a claim that the absolute
number is competitive.

## Most likely structural error

The base encoder maps validation videos and authors unseen during training to
unknown. With 4.37 million items, cold candidates are common. The archive's
basic table provides content categories that remain usable for unseen videos.
Testing primary tag, upload type, and video type is therefore a causal
generalization hypothesis, not a validation micro-tune.

## Risks and gate

Metadata vocabularies may be noisy or too coarse, and constructing them from
the complete item table must not leak labels. Only identity dictionaries are
global; train-seen masks still control learned categorical slots. Compare the
fixed content FM to exact recorded base metrics on early, middle, and late
validation plus forward windows. Require at least two clear two-sided wins and
no meaningful activity collapse before official seeds. If it fails twice,
stop. A longer sequential-history family remains the next independent path,
not an excuse to tune content subsets.
