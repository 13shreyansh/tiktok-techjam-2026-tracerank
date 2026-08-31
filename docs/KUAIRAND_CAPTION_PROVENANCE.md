# KuaiRand supplementary caption provenance

Source record: <https://zenodo.org/records/18159199>

- Record title: *Kuairand Supplementary Files: Video Captions and Categories*
- Source file: `kuairand_video_captions.csv`
- Source URL:
  <https://zenodo.org/records/18159199/files/kuairand_video_captions.csv>
- Source size: 3,222,932,768 bytes
- Source MD5 published by Zenodo: `9fd4e7587ffd0c8dc289d013858fb229`
- Zenodo record licence: CC BY 4.0
- Record created: 2026-01-06T16:25:03.455999+00:00
- Record modified: 2026-01-06T17:57:35.434953+00:00

The source is ordered by `final_video_id`. KuaiRand-Pure uses exactly IDs 0
through 7582, so downloading the complete 3.22 GB file is unnecessary. The
acquisition script requests HTTP byte range 0-4,194,303. Zenodo returned `206
PARTIAL_CONTENT`, `Content-Range: bytes 0-4194303/3222932768`, and
`Accept-Ranges: bytes` on 2026-08-29.

Verified local acquisition:

| Artifact | Bytes/rows | SHA-256 |
|---|---:|---|
| byte-range prefix | 4,194,304 bytes | `d8db383fb1a92477c837c1cf3e9f5f26adbd41e89212ee245198e06a6b39318f` |
| Pure subset | 7,583 data rows | `7593a7e1497951a16ca29126605b751869cf66df5a2f845f7690b2f6c1f4ba2c` |

The subset has 7,583 unique, contiguous, ordered video IDs. Of these, 7,498
have a nonempty caption, 944 have nonempty cover text, 6,485 mention a
hashtag, and only 65 have neither caption nor cover text. Mean combined text
length is 43.04 characters; the maximum is 856.

Both acquired CSVs remain under ignored `data/`. Reproduce them with:

```text
.venv/bin/python scripts/acquire_kuairand_captions.py
```
