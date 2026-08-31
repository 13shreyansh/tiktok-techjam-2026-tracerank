# Run 62 report: exact safety route construction failed

Run62 attempted the frozen two-input high-activity safety route: Run61 for
ordinary users and exact Run52 for users above the training-activity upper
tertile. The subprocess returned code 1 before evaluation because the existing
router requires at least four inputs and blends the final specialist with three
base members; it cannot express the predeclared exact two-input fallback.

The failed attempt took `0.993456` seconds and peaked at `3,226,222,592` bytes
RSS. It produced no prediction output, validation metric, forward metric,
robustness metric, hidden-test result, or public-test evaluation. Run61's score
is not attributed to this run.

Run62 closes at its construction-failure stop after one counted failed attempt.
A tested exact-fallback router and any score require a fresh bounded run. Run52
remains protected at local primary `0.6534977984044839`; the 72-hour campaign
continues.
