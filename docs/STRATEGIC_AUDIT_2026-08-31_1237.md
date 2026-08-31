# Strategic audit — 2026-08-31 12:37 SGT

## Evidence after Run76

Run76's user-grouped LambdaMART produced complementary forward and nDCG@5
signal, but its fixed consensus improved validation primary only
`+0.0000588416694892`, with weaker GAUC and mixed activity slices. The exact
tree, feature, and blend family is closed. Run4 already measured the separate
random-exposure log and rejected three direct debiasing changes, so treating
exposure correction as an untested direction would be false.

## Remaining organizer-aligned mechanism

The workshop's strongest modeling clue is candidate-aware history: what a user
watched previously should affect how the current candidate is scored. The Pure
model used target-aware attention, but no 27K run has placed target-aware
attention on top of the protected Run52 representation. Runs57 and 58 merely
inserted recent-history IDs as ordinary FM fields or linear fields; they did
not let the candidate select the relevant part of the history.

Run77 therefore freezes Run52 and trains only a compact residual. The
candidate primary tag attends over the user's five most recent strictly earlier
long-view-positive primary tags using the standard DIN combination
`[history, target, history-target, history*target]`. Tab, duration bucket, and
time since the last positive event are bounded context. No raw video, author,
or user identity is added to the residual. The final residual layer starts at
zero, making epoch zero exactly equal to Run52 and providing automatic
rollback.

## Controls and third-person check

History length five and the causal archive are inherited unchanged from
Run57; embedding width 16, hidden widths 64/32, dropout 0.1, learning rate
0.001, three maximum epochs, and patience one are frozen before scoring. There
is no feature subset, attention type, blend weight, epoch count, or learning-
rate search. A 4,096-row smoke test reproduced the preserved parent archive
with maximum absolute error `0.0`; all 80 tests pass. Source SHA-256 is
`5673d2ece1b8619bfb335a5a0764d5ed24ee87571a16e8e65fa5294ab5ff4e4a`.

This is higher-value than another FM or tree variation because it implements a
missing mechanism explicitly supported by the talk, while exact-parent
initialization bounds downside. The main risk is that five coarse tags contain
too little information or the residual overfits the fixed sample. Require
validation and forward transfer, component and slice safety, later windows,
and three seeds before promotion. Run52 remains immutable.
