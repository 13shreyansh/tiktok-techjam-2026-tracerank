# Strategic review 000 — temporal context

## Evidence

- The organizer starter names `hourmin`, `date`, and train/test distribution
  drift as untested headroom.
- The selected model fields are user, video, author, tag combination, tab, and
  duration bucket; it does not represent time.
- Raw date identity would be unknown in future periods and is unsafe. Weekday
  repeats across splits and hour-of-day has a stable meaning, so these are the
  first leakage-safe temporal fields.
- Both fields enter the same embeddings and FM interactions as other context,
  allowing user-hour and item-time effects without a separate architecture.

## Decision

Test hour plus weekday together as one coherent context hypothesis on the early
window and its forward window. Do not add raw date. If the result is positive
but below +0.001, stop the configuration rather than tune category granularity.
