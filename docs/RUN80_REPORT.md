# Run 80 report: frozen-embedding DeepFM residual rejected

Run80 tested the workshop's standard categorical-embedding-plus-shallow-MLP
idea without relearning any sparse identities. The exact Run52 rank-32
seed-2027 early checkpoint supplied all 24 frozen field embeddings and the
parent logit. A fixed 768→32→16→1 residual tower started at exactly zero. Its
architecture, dropout, optimizer, rate, batches, seed, three-epoch maximum,
patience-one rollback, and gates were frozen before scoring.

The epoch-zero reconstruction matched the stored parent predictions with
maximum absolute error `0.0`. The first trained epoch then reduced validation
GAUC from `0.7028987283878007` to `0.6995229674369844`, nDCG@5 from
`0.5674319496776296` to `0.5642114570814302`, and primary from
`0.6351653390327151` to `0.6318672122592073`. The primary delta was
`-0.0032981267735078`, far below the required `+0.0003`, and both components
also failed their `-0.0005` safety floors. The fixed rollback therefore selected
epoch zero and did not evaluate the trained residual on the forward window.

The successful wrapper took `81.0618839263916` seconds and peaked at
`20,103,299,072` bytes RSS. The ignored rollback checkpoint is 104,433 bytes,
SHA-256 `4cb71e849b676542ecd4414f79db031ccdda1ec38f438508960286e2e8299b36`.
The ignored finite prediction archive is 6,607,883 bytes, SHA-256
`8d2392915731af585177bbb79287fc391629dea2fbce9f1faab0c965db911872`,
exactly matching the parent prediction hash. Run80 stops at attempt one with no
hyperparameter or blend search. Run52 remains protected at local official-sample
primary `0.6534977984044839`. These scores are deterministic development-sample
results, not the full benchmark, hidden test, submission, or leaderboard.
Closing Run80 closes only this hypothesis; the 72-hour campaign continues.
