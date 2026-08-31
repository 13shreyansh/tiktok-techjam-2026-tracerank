# KuaiRand-27K bonus benchmark provenance

Audit time: **2026-08-29 20:02 SGT**.

## Official source evidence

- Project: <https://kuairand.com/>
- Zenodo record: <https://zenodo.org/records/10439422>
- Archive:
  <https://zenodo.org/records/10439422/files/KuaiRand-27K.tar.gz>
- DOI: <https://doi.org/10.1145/3511808.3557624>

The official project describes KuaiRand-27K as the complete version with
27,285 users, 32,038,725 items, and 322,278,385 interactions. Its published
layout is approximately 23 GB of logs plus 23 GB of features. A live HTTP HEAD
request returned 9,892,191,178 compressed bytes and
`Last-Modified: Tue, 11 Nov 2025 06:52:14 GMT`. The official archive MD5 is
`3e3c799a24e2d23a4d2c757fbf9adf59`.

## Verified local receipt

The acquisition command completed successfully on **2026-08-29 21:27 SGT**:

```text
/usr/bin/time -l scripts/acquire_kuairand_27k.sh
```

Observed results:

- compressed bytes: `9,892,191,178` (exact expected value);
- MD5: `3e3c799a24e2d23a4d2c757fbf9adf59` (exact official value);
- SHA-256: `b8a8a5b777e564202cff6b96676959ee0d6baccc7ad7376bcb4af6767362d41b`;
- acquisition, safety inspection, and extraction exit status: zero;
- acquisition wall time: `6,280.91 s`;
- acquisition maximum resident set size: `7,913,472 bytes`;
- extracted size reported by `du -sh`: `46G`;
- observed archive members: ten published CSV files plus `load_data_27k.py`;
- loader SHA-256:
  `1a26d6dc3aabd9da0f87385afe78a7a578799b0634fc1a9e4586f2e587cb388e`.

The read-only inspection receipt is stored in the ignored
`outputs/kuairand-27k-inspection.json`. All five log files have the official
19-column interaction schema. The basic video table spans observed endpoint
IDs 0 through 32,038,724, and the user table spans endpoint IDs 0 through
27,284. These are endpoint observations and schema checks, not full ordering or
row-count proofs.

The Track 2 statement explicitly names KuaiRand-27K as an optional bonus
benchmark. It does not publish a 27K-specific baseline, bonus formula, hidden
delivery route, split loader, format checker, or submission schema. These are
unresolved contract gaps; no local convention is represented as organizer
approval.

## Acquisition and safety procedure

Run:

```text
/usr/bin/time -l scripts/acquire_kuairand_27k.sh
```

The script downloads to the ignored `data/` directory, resumes a partial
transfer, verifies the exact byte count and official MD5 before renaming, then
rejects absolute paths, parent traversal, links, devices, and any archive entry
other than a regular file or directory before extraction. The 9.9 GB archive,
roughly 46 GB extracted data, partial download, caches, checkpoints, and model
outputs remain ignored.

At audit time, 608 GiB was free on the data volume and the workstation had 64
GiB of unified memory. Storage is feasible, but model and evaluator feasibility
is not yet established. No 27K baseline has been reproduced and no 27K model
score is claimed until a documented command succeeds.

## Licence boundary

At the **2026-08-29 21:11 SGT** live recheck, the rendered Zenodo record exposed
a `Rights / License` heading but no licence value. The official KuaiRand GitHub
repository identifies itself as CC BY-SA 4.0, and the Pure and 1K archives from
the same record embed CC BY-SA 4.0. The 27K archive licence cannot be claimed
until the checksum-verified extract is inspected. This repository therefore
does not infer CC BY 4.0 or silently transfer a neighbouring archive's licence
to 27K. The verified 27K extract contains no licence or licence-named file, so
that unresolved boundary remains in force.
