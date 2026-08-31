# Autonomous research reference provenance

Recorded at **2026-08-29 11:59 SGT**, before the official challenge start.
These are unmodified upstream references only. No reference was configured for
Track 2, no judged solution was designed, and no experiment was started during
preparation.

## Preserved sources

| Source | Pinned commit | Licence evidence | Preservation result |
|---|---|---|---|
| [Karpathy autoresearch](https://github.com/karpathy/autoresearch) | `228791fb499afffb54b46200aca536f79142f117` | The pinned README states MIT; the snapshot has no standalone licence file | Complete archive verified and extracted unchanged |
| [AIDE](https://github.com/WecoAI/aideml) | `085899eeb90804314d184fb65b9de0d17c9ce6f0` | Included MIT `LICENSE` | Complete archive verified and extracted unchanged |
| [FML-Bench](https://github.com/qrzou/FML-bench) | `d336651ebea50c622c256f02ded82b68b4451fdc` | Included Apache-2.0 `LICENSE` | Complete archive verified and extracted unchanged |
| [OpenAI MLE-bench](https://github.com/openai/mle-bench) | `507f92e1138bb6e40dac5c6ee7a6758e6424bf97` | Pinned MIT `LICENSE` | Pinned README and licence only; the incomplete full archive was quarantined |

Exact URLs and checksums are in
`manifests/autonomous-research-sources.json`. Original complete archives remain
under ignored `artifacts/third_party/original/`; they are deliberately not
committed. The incomplete MLE-bench transfer and extraction are under ignored
`artifacts/third_party/incomplete/` and must not be treated as usable source.

## Applicability and boundaries

Karpathy's upstream system is a useful loop pattern: keep a fixed evaluator,
let an agent modify a bounded work file, run a time-boxed experiment, retain
improvements, and log every attempt. Its included workload is not directly
usable here: the pinned README requires Python 3.10+, `uv`, and one NVIDIA GPU
(tested on H100), while this repository was prepared on an Apple M5 Pro. Its
five-minute experiment budget is an upstream design choice, not a Track 2 rule.

AIDE and the two benchmark repositories are preserved as additional reference
implementations. “OpenAI MLE-bench” and “FML-Bench” are separate projects; the
latter is from `qrzou`, not OpenAI. Their presence does not prove compatibility,
performance, or permission to use any external competition dataset. No API
credentials were added, and no dependency installation or remote service call
was performed for these tools.

## Verification commands

The complete archives were downloaded from their pinned GitHub codeload URLs,
checked for absolute paths and parent-directory traversal before extraction,
and hashed with:

```bash
shasum -a 256 artifacts/third_party/original/*.tar.gz
```

Observed SHA-256 values:

```text
20008d6be1661850317d3825403c4e58922467e4117577836dbb6c6659b69b09  karpathy-autoresearch-228791f.tar.gz
94e534bebefbcbb7263ddab21db6fc3fc08fa1416405b418eac8b781677ed371  wecoai-aideml-085899e.tar.gz
4f8ed5bb0c46367bc161338dad940f86bfc4a47f5f66b9492588f84e37920cac  qrzou-fml-bench-d336651.tar.gz
```

The first OpenAI MLE-bench codeload transfer failed `tar -tzf` with an
unexpected end-of-file error. It was not accepted or represented as a complete
snapshot. The pinned fallback files were separately hashed; their values are in
the manifest.
