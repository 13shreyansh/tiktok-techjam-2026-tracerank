# Run 36 protocol: conservative rare-identity pooling

## Hypothesis

The full-density FM overfits video and author identities that occur only a few
times in training. Mapping identities with fewer than five training occurrences
to a shared learned cold bucket can improve transfer while preserving frequent
identity and causal history signals.

## Frozen change

- Keep the exact Run 34 full-density rank-8 `history_item` FM, BCE objective,
  learning rate `0.001`, epochs/patience, batching, seeds, cache, evaluator,
  evaluation rows, and robustness definitions.
- Define `seen_video` and `seen_author` from training-only frequency counts.
  Require count at least 5 for both. User, tag, tab, duration, causal history,
  and causal item-history encoding remain unchanged.
- Rare training identities and truly unseen evaluation identities share the
  existing unknown field bucket, allowing its linear and latent weights to be
  learned from rare training rows. Do not compress or reorder field dimensions.
- The threshold 5 is fixed before scoring from labels-blind coverage and a
  conservative minimum-support rule; no threshold sweep is allowed in Run 36.

## Evidence and gates

The official training prefix has 15,293,075 seen videos and 4,948,795 seen
authors. Of 2,222,628 fixed official-development rows, 1,377,905 have an unseen
training video; counts 1–4 add 111,978 rows, so threshold 5 pools 1,489,883.
For authors, 208,209 are unseen and counts 1–4 add 112,112, so threshold 5
pools 320,321 rows. No outcome labels were read for this coverage audit.

1. Run early shadow first. Continue only for validation `>= +0.0005`, forward
   `>= -0.0005`, and every fixed slice `>= -0.001` versus Run 34.
2. If early passes, repeat middle and late unchanged. At least two of three
   must pass with no material transfer failure.
3. Only then run official seeds 2027–2029. Promote for paired mean gain
   `>= +0.0005`, no seed below `-0.0005`, and score span `<= 0.002`.
4. Stop on the first failed gate or after six successful attempts. Existing
   wrapper limits remain 50 attempts and six wall-clock hours.

All scores remain deterministic development-sample evidence, not hidden-test,
full-benchmark, submission, or leaderboard evidence. No external action is
authorized.
