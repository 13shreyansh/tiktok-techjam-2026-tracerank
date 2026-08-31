# Run90 decision journal

## 2026-08-31 18:40 SGT — family frozen

- Preserve the exact selected long-history path and add only a separately
  normalized last-five positive-history profile.
- Opening gate is paired seed 2027 on the early chronological window. Require
  `+0.0005` validation and nonnegative forward transfer with hard floors.
- A failed gate closes the family without recent-length, projection, capacity,
  label, action, loss, optimizer, seed, window, or blend rescue.
- Run84 remains protected and official final-test outcomes remain locked.

## 2026-08-31 18:42 SGT — implementation verification passed

- Twelve targeted tests and the complete 104-test suite passed; Python
  compilation, CLI discovery, and `git diff --check` passed.
- The new unit test verifies the recent mask averages only eligible positions
  and returns a finite zero profile for an empty history.
- No model or benchmark score was produced. Commit the exact implementation and
  protocol before the first counted seed-2027 execution.

## 2026-08-31 19:43 SGT — opening gate failed; family closed

- The exact committed seed-2027 early-shadow attempt completed successfully in
  `44.584516` seconds with maximum RSS `3,424,583,680` bytes.
- Validation primary improved from `0.6169077754` to `0.6174653769`, a gain of
  `+0.0005576015`; GAUC gained `+0.0001991391` and nDCG@5 gained
  `+0.0009160638`.
- Forward primary changed from `0.6040810347` to `0.6040716171`, a loss of
  `-0.0000094175`. Forward GAUC lost `-0.0001958013`, while forward nDCG@5
  gained `+0.0001769662`.
- The high-activity slice lost `-0.0012083505`, also exceeding the frozen
  `-0.001` floor. Cold/low and medium activity improved, but late dates lost
  `-0.0003148116`.
- The opening gate required nonnegative forward primary and no slice loss below
  `-0.001`. Both conditions failed. The family is closed after one counted
  attempt without a second seed, recent-length search, tuning, or blend.
- The raw immutable ledger omitted the structured `forward_valid` field because
  the Pure campaign wrapper did not project it, although the authoritative
  ignored result JSON and the ledger's captured stdout contain it. The ledger
  was not rewritten. The wrapper is corrected prospectively and unit-tested;
  this report records the historical omission transparently.
- No official-test outcomes were loaded, no official candidate was generated,
  and Run84 remains protected at primary `0.605374519999571`.
