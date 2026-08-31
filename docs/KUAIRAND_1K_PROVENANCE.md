# KuaiRand-1K bonus benchmark provenance

Audit time: **2026-08-29 18:25 SGT**.

## Official source evidence

- Project: <https://kuairand.com/>
- Zenodo record: <https://zenodo.org/records/10439422>
- Archive:
  <https://zenodo.org/records/10439422/files/KuaiRand-1K.tar.gz>
- DOI: <https://doi.org/10.1145/3511808.3557624>

The official project page publishes the archive MD5 as
`6b0b9c8222d67fcd4c676218edca3f1f` and describes KuaiRand-1K as 1,000 users,
4,369,953 items, and 11,713,045 interactions, with about 829 MB of logs and
3.5 GB of features. A live HTTP HEAD request reported 1,135,436,720 compressed
bytes and `Last-Modified: Tue, 11 Nov 2025 06:52:28 GMT`.

The dataset is an organizer-authorized optional bonus benchmark, not external
training data. The official Track 2 statement says it uses the same task and
metrics as KuaiRand-Pure, but does not publish a bonus formula, exact hidden-test
route, or starter-integrated 1K split loader. Those are unresolved contract
gaps rather than assumptions this repository silently fills.

## Reproducible acquisition

```text
/usr/bin/time -l scripts/acquire_kuairand_1k.sh
```

The command completed successfully in 741.03 seconds. The verified archive is
1,135,436,720 bytes with MD5
`6b0b9c8222d67fcd4c676218edca3f1f` and SHA-256
`dfaafbb5fd16e9e6d2f9a6adaa4ea25df20a14bc26a90961c136e26c00a7bb2c`.
The acquisition command reported maximum RSS of 7,979,008 bytes.

The script downloads into ignored `data/`, resumes a partial transfer, requires
the exact byte size and official MD5 before renaming, rejects absolute or
parent-traversal paths and non-file/directory archive entries, and only then
extracts. The archive, extracted dataset, partial transfers, caches, models,
predictions, and outputs remain ignored.

## Licence status

The shared Zenodo record advertises `cc-by-4.0`, while the checksum-verified
KuaiRand-1K archive embeds CC BY-SA 4.0. Its embedded licence is byte-identical
to the already preserved Pure licence at
`docs/licenses/KuaiRand-Pure-LICENSE.txt`, SHA-256
`187442db4df3afd21f2f0525739fd4beac28a62daaba3ee8d3533f60e7c33ec7`.
Both claims are preserved; the repository does not silently choose between
them.

## Compute feasibility before acquisition

The workstation had 638 GiB free, far above the observed 4.3 GB extracted
size. The archive contains all 11,713,045 published interaction rows, but its
basic video table has 4,371,868 rows with maximum reindexed ID 4,371,899 and 32
ID holes. That differs from the project page's 4,369,953-item summary; both
published and observed counts are recorded rather than reconciled by guess.

A memory-bounded cache of April 8–28 development rows completed successfully:
5,055,984 training rows and 2,524,980 validation rows. It skipped 4,132,081
later rows by date without retaining their `long_view` label. The final
deterministic cache rebuild completed in 87.55 seconds with 790,282,240-byte
peak RSS. Its format-5 manifest SHA-256 is
`718f309372561ac3340fdebf70aacc3f441b4c19ce05303788073df73ac6acd1`;
all original base/content/date/label arrays retained their earlier hashes while
later rejected families added separate history and metadata arrays. Run 16
trained the sparse-FM family and fixed content extension under 3.36 GB peak RSS,
establishing local feasibility. No organizer 1K baseline score exists, so this
is a verified local benchmark run, not a claimed organizer-baseline
reproduction.

The 3.1 GB monthly aggregate statistics table was excluded entirely. Its README
defines values over the full month and the table includes the judged
long-time-play concept without a date column, so it cannot be joined causally to
the April development windows. The label-free basic video table was used only
for catalogue attributes.
