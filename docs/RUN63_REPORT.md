# Run 63 report: exact fallback narrowly below forward gate

Run63 used the tested exact router to retain Run61 outside the fixed
high-activity cohort and protected Run52 inside it. The implementation was
committed independently and all 59 tests passed before scoring.

The attempt completed successfully. Validation primary improved
`+0.0002591555143150`, GAUC `+0.0001451720717213`, and nDCG@5
`+0.0003731389569087`. The high-activity regression was eliminated and all
fixed slices stayed within the tighter `-0.0005` guard. Forward primary,
however, improved only `+0.0002031095226152`, missing the frozen `+0.00025`
threshold by `0.0000468904773848`.

The attempt took `6.468082` seconds and peaked at `3,361,636,352` bytes RSS.
The ignored 4,161,718-byte prediction SHA-256 is
`d1186b6eb351fb88874eff45dc37f391407438f16c15d953e70e22345c921e61`.

Run63 therefore stops without middle, late, official, threshold, or route
variation. Run52 remains protected at local primary `0.6534977984044839`.
These are fixed 1/32 development-sample results, not the full benchmark,
hidden test, submission, or leaderboard. The 72-hour campaign continues.
