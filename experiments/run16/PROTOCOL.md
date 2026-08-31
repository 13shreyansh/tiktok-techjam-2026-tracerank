# Run 16 protocol: KuaiRand-1K sparse-FM bonus benchmark

Started: **2026-08-29 17:22 SGT**

## Win-aligned question

Can the organizer-authorized KuaiRand-1K bonus benchmark provide a material,
independent judging advantage now that fifteen KuaiRand-Pure hypothesis
families have plateaued, while retaining the protected Pure candidate at
`0.6054008850379737` unchanged?

KuaiRand-1K is a separate benchmark run. It has its own 50-attempt and six-hour
limits. Acquisition and cache preparation are included in total project
resource accounting but are not model iterations. Every command that trains or
scores a learned 1K candidate is a counted Run 16 attempt.

## Fixed first family

The first family is a memory-safe sparse Factorization Machine that retains the
organizer baseline's five fields: user, video, author, tab, and training-derived
duration bucket. It uses sparse CPU updates so the 4.37-million-item embedding
table does not allocate a full dense gradient for every minibatch. The official
organizer evaluator remains unchanged; a faster evaluator is permitted only
after exact synthetic equivalence is proven.

The development cache retains only 2022-04-08 through 2022-04-28. Rows after
April 28 are rejected from the date column before `long_view` is accessed, and
no test labels are retained. Unseen validation users, videos, and authors map to
the training-only unknown slot.

## Gates and attempt order

1. Build and verify the ignored development cache. This is an engineering
   command, not a model attempt, but its time and memory are recorded.
2. Run one fixed rank-16 sparse FM on `shadow_early`, with seed 2027, learning
   rate 0.001, batch 65,536, at most 20 epochs, and four-epoch early stopping.
3. If the command fails for engineering reasons, one repaired rerun may use the
   identical hypothesis and still counts. If it runs, record validation,
   forward, date slices, and activity slices.
4. Continue the unchanged model through middle and late windows only if the
   first run is feasible and materially above random. A three-window shadow
   gate requires stable validation and forward behavior in at least two of
   three windows, with no unexplained collapse in an activity slice.
5. Official validation remains mechanically locked until the shadow gate is
   explicitly marked passed in `run_state.json` after a fresh strategic audit.
6. Promotion as a bonus candidate requires official validation, robustness
   slices, and three independent seeds. It does not replace or modify the Pure
   fallback.
   The three fixed seeds enter one equal mean within-user-percentile-rank
   ensemble; no member selection, weights, or alternative aggregation is
   searched.
7. Organizer convergence epsilon `0.002` over `N=3` consecutive attempts is
   binding. Stop an unproductive family early; do not spend 50 attempts merely
   because they exist.

## Hard boundaries

- Maximum 50 counted attempts and six hours from Run 16 start.
- Fresh strategic review after each family or every eight attempts.
- No row after 2022-04-28 is present in the cache; no test-label evaluation,
  submission, upload, push, contact, credential use, registration change, or
  visibility change.
- Exact commands, metrics, hashes, elapsed time, maximum RSS, failures, and
  recovery decisions are append-only evidence.
