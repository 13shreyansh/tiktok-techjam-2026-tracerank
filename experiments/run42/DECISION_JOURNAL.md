# Run 42 decision journal

## 2026-08-30 21:08 SGT — capacity family reopened on a materially new regime

- The overall goal is still active. Runs 40 and 41 rejected creator-specific
  action rates and recency after one frozen early shadow each; neither changed
  the protected repeat-affinity candidate.
- Run 27 is the only prior rank-16 test. It used 1/32 training density and no
  user-entity repeat fields, yielding a stable but immaterial `+0.000217721`.
  Run 34 subsequently showed that density scaling remained strongly positive,
  and Runs 38-39 established repeat affinity as a separate winning signal.
- Rank 8 now compresses 24 categorical fields and full-density evidence into
  the same latent width used before those changes. Testing rank 16 once is a
  higher-value, cleaner question than adding another fragile hand-built field.
- The active `history_item_repeat` execution path is unchanged from protected
  commit `21af016`; the current source hash differs only because two rejected,
  unselected feature alternatives were added. Current ranker SHA-256 is
  `3546226f7af3307fa3051f19794d0fff54aa02e20748a27e34f9afaab85f25d1`.
- The machine reports 68,719,476,736 bytes of physical memory. Rank-8 full-data
  attempts peaked around 23.4 GB. Rank 16 is expected to be materially larger,
  so resource use will be observed and recorded, but no batch/rank change will
  be made after score inspection.

This advances the winning objective only if the extra capacity transfers
chronologically and across every fixed slice. Start with early shadow only;
official development remains locked.

## 2026-08-30 21:24 SGT — small stable gain misses materiality; run closed

- Attempt 1 completed successfully in 1,013.211 seconds with peak subprocess
  RSS 19,093,716,992 bytes and selected epoch 1.
- Early primary moved from `0.6328858732963454` to
  `0.6332970622427874`, a gain of `+0.0004111889464420`. This is positive but
  below the frozen `+0.0005` continuation gate. GAUC changed
  `-0.000021206`, while nDCG@5 improved `+0.000843584`.
- Forward improved `+0.000391538`. Slice deltas were cold/low
  `+0.000362968`, medium `-0.000562948`, high `+0.003015185`, early dates
  `-0.000081344`, and late dates `+0.000020060`; none breached its guard.
- The rank-16 result is stable and directionally interesting, especially for
  high-activity users, but not large enough to justify middle/late/official
  compute under the declared rule. Do not sweep another rank or tune learning
  rate in this run. Preserve the rank-8 repeat-affinity candidate and continue
  the overall campaign with a fresh hypothesis.
- The initial state timestamp was accidentally written 60 seconds after the
  actual command start, so the ledger records a `-60.109174`-second campaign
  offset. The state timestamp is corrected to the observed command start;
  attempt elapsed time and model accounting are unaffected.
