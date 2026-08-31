# Run 38 report: causal user-creator/video repeat affinity

## Decision

Run 38 closed at the six-hour wall-clock boundary after five successful
attempts. It added four strictly causal fields to the protected Run 34 model:
prior user-author count and long-view rate, plus prior user-video count and
long-view rate. All three chronological shadows improved validation, their
forward periods, and every fixed activity/date slice.

Two official-development seeds completed before the wall-clock guard. Both
improved their exact Run 34 seed parent:

| Seed | Run 34 parent | Run 38 candidate | Change |
|---|---:|---:|---:|
| 2027 | 0.644615073 | 0.648551700 | +0.003936627 |
| 2028 | 0.645083464 | 0.649016563 | +0.003933099 |

Their mean is 0.648784131, paired mean gain is +0.003934863, and score span is
0.000464863. Every fixed slice improved for both seeds. Nevertheless, Run 38
is **not promoted** because its predeclared gate requires three official seeds.
The unchanged seed-2029 command was rejected before execution after the run
crossed six hours, so it did not consume an iteration. Run 34 remains protected
until a separately disclosed confirmation run completes the missing evidence.

Subsequent Run 39 completed the unchanged seed-2029 confirmation and passed
the campaign-level three-seed gate. That promotes the repeat-affinity candidate
at campaign level while preserving Run 38's historical status as closed and
not independently promoted.

## Validity boundary

The candidate was fixed before evaluation. Feature state used only earlier
timestamps within training and was frozen at each split cutoff. Rows sharing a
user/entity/timestamp saw the same prior state before their grouped update.
The official development sample is deterministic but is not the organizer
hidden test, full KuaiRand-27K benchmark, submission, or leaderboard.

The feature archives cover all 207,446,146 cache rows. Their SHA-256 values are
`7059bddf2ae238130d3657088ad2c4aefb0817067a0068a6122865d93753e725`
(early), `692f95e3a9f5d091129c3994e1386231b2577213fb137acf7e96be5498ed89dc`
(middle), `5c3791c6aff438acd1433c78b38ccdf258daeeb67f2c98209ea0787479b6fcb4`
(late), and `b67e0e2ef0f5034df06c01db2c171a875be4bd929913375fe9fbb471c2bb90c2`
(official). The ranker source SHA-256 is
`85b160894516b5e300c59bda78a1d414bb8b25694f07c637744218f27cacafb1`.

## Accounting and artifacts

Five counted model attempts completed successfully in 6,129.929 subprocess
seconds; peak subprocess RSS was 21,875,490,816 bytes. Four feature builds took
4,792.234 recorded seconds. Run 38 started at 2026-08-30 07:17:18 SGT; the
wall-clock guard later prevented another attempt after six hours.

The ignored seed-2027 checkpoint is 1,053,516,085 bytes with SHA-256
`da249e7998918db2717d7a5c539fd5471d81bce0ae31bf636165e75335278d4b`;
its 8,035,668-byte prediction archive has SHA-256
`28750178342e69dca1b44eaddd5715a931ce9fed78bbfdca3cf4819fc5e8881b`.
The ignored seed-2028 checkpoint is 1,053,516,085 bytes with SHA-256
`4cc674104bc7daf8163b0abe174b7bddaf75034defa1522d3f74e6035e976465`;
its 8,029,704-byte prediction archive has SHA-256
`7ec69a8fb701948f0397aa4946f9d1c8c0b91e39a6d4704c56704795c0012327`.

The ledger field named `model_sha256` is the hash of the model entrypoint
source, not a checkpoint hash; direct artifact hashes above are authoritative.
No public-test labels, hidden labels, upload, submission, push, contact, or
public release occurred.
