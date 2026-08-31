# Strategic review 000 — behavior sequence

## Evidence map

- Workshop: behavior history and actions such as click, like/dislike, and
  comment are important ranking features.
- Official data: action columns include click, like, follow, comment, forward,
  and `is_hate`; the judged label remains `long_view`.
- Current parent: target-aware attention over the last 20 positive long-view
  videos and tags, but no action identity inside those events.
- Prior attempts: click-only history, past aggregate behavior rates, latest
  click/engagement context, and watch-ratio/click auxiliary tasks did not meet
  robust promotion gates. A unified causal behavior sequence remains untested.
- Ranking objective: Run 5 directly tested user-listwise and BPR fine-tuning;
  both reduced their pointwise checkpoints. Final slate re-ranking is explicitly
  outside the challenge, so this family improves representations rather than
  optimizing diversity of an artificial list.

## Design choice

Store one one-offset seven-bit action mask per past video and decode it into
seven shared binary action embeddings. This avoids seven additional full
history arrays and lets rare actions share their meaning across combinations.
The first attempt keeps exactly the parent's long-view event selection; a
second attempt may include any explicit behavior event if the first result
supports the representation.
