# KuaiRand supplementary category provenance

Source record: <https://zenodo.org/records/18159199>

- Record title: *Kuairand Supplementary Files: Video Captions and Categories*
- Source file: `kuairand_video_categories.csv`
- Source URL:
  <https://zenodo.org/records/18159199/files/kuairand_video_categories.csv>
- Source size: 3,687,928,520 bytes
- Source MD5 published by Zenodo: `8a4c772d3d8f8cf65fa1e1eb896f4177`
- Zenodo record licence: CC BY 4.0
- Record created: 2026-01-06T16:25:03.455999+00:00
- Record modified: 2026-01-06T17:57:35.434953+00:00

The source is ordered by `final_video_id`. KuaiRand-Pure uses exactly IDs
0 through 7582, so downloading the complete 3.69 GB file is unnecessary. The
acquisition script requests HTTP byte range 0-2,097,151. Zenodo returned `206
PARTIAL_CONTENT`, `Content-Range: bytes 0-2097151/3687928520`, and
`Accept-Ranges: bytes` on 2026-08-29.

Verified local acquisition:

| Artifact | Bytes/rows | SHA-256 |
|---|---:|---|
| byte-range prefix | 2,097,152 bytes | `c91886658c1fc1897ebd6e808ebcc87acfddb4548d5acb8faa70ee8ccd3a091c` |
| Pure subset | 7,583 data rows | `45dd0fb396d4622ddd14e6aca2c28c2e57c220a18499cfed742abba794e6e439` |

The subset has 7,583 unique, contiguous, ordered IDs and covers the complete
Pure video table. It contains 39 top-level, 157 second-level, 247 third-level,
and 388 distinct three-level category paths. Twelve records have blank
probability fields; Run 12 uses only category IDs. Missing category levels use
the organizer value `-124.0`.

Both acquired CSVs remain under ignored `data/`. Reproduce them with:

```text
sh scripts/acquire_kuairand_categories.sh
```
