# Run 76 report: causal dense LambdaMART below gate

Run76 tested a new 27K model class: deterministic LightGBM LambdaMART trained
on user-grouped lists and 21 audited causal dense features, then given one
equal within-user rank vote with the matching exact Run52 prediction. Raw
user/video/author identity, dates, future labels, failed feature families,
parameter search, and blend weights were excluded.

Attempt 1 failed before model construction because LightGBM limits a query to
10,000 rows and one user had 10,583. No score or artifact existed. A tested,
row-conserving compatibility adapter split only oversized users into contiguous
same-user chunks of at most 10,000. Attempt 2 then trained all 41,010,906 rows,
26,070 users, 26,239 bounded queries, and selected boosting iteration 186.

The fixed consensus was mildly complementary but failed its materiality gate.
Versus exact Run52, validation primary changed only
`+0.0000588416694892`, GAUC `-0.0004182642620896`, and nDCG@5
`+0.0005359476010679`. Forward primary changed
`+0.0006535903495063`, GAUC `-0.0001944458850165`, and nDCG@5
`+0.0015016265840292`. Slice deltas were cold/low
`-0.0007184615913072`, medium `+0.0022727603006051`, high
`-0.0006881855008379`, early dates `-0.0002454797947051`, and late dates
`+0.0003241950257481`.

The forward and nDCG signal is real local evidence, but validation missed the
predeclared `+0.0005` continuation gate. No later window, official model,
tree parameter, feature subset, blend weight, route, or calibration was tried.
The successful command took `198.295398` wrapper seconds and peaked at
`14,816,526,336` bytes RSS; the failed construction consumed `15.585875`
seconds and peaked at `13,281,886,208` bytes.

The ignored 688,713-byte tree SHA-256 is
`e3332dce0ba7f85814dc65662ef2b1e2cac54db9dc3b6d370d04ed6fde87d5b9`;
the ignored 4,456,283-byte prediction SHA-256 is
`63cb2c673e82b122ea1c98b7bbeb2b3b90985db17894bce2a0254cc617a4a292`.
Runtime URLs, versions, checksums, licence, and SBOM are preserved separately.

Run52 remains protected at local primary `0.6534977984044839`. These scores
are deterministic 1/32 development-sample evidence, not the full benchmark,
hidden test, submission, or leaderboard. Closing Run76 closes only this exact
hypothesis; the 72-hour campaign continues.
