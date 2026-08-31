# Repository-local OpenMP runtime provenance

Run76 requires the already-installed LightGBM Python package, whose macOS
binary links to `@rpath/libomp.dylib`. No compatible runtime was present in the
workspace bundles, `/opt/homebrew`, `/opt/local`, or the active virtual
environment. Homebrew itself is not installed, so no system package manager or
global path was changed.

- Component: Homebrew `libomp` bottle, LLVM OpenMP runtime
- Version: `23.1.0`
- Platform bottle: `arm64_tahoe`
- Formula API observed: `https://formulae.brew.sh/api/formula/libomp.json`
- Bottle URL:
  `https://ghcr.io/v2/homebrew/core/libomp/blobs/sha256:462a36670e56b7804c607e16c4d1b013bbca2a531b39b612a28d8f1bb0c1a37c`
- Bottle SHA-256:
  `462a36670e56b7804c607e16c4d1b013bbca2a531b39b612a28d8f1bb0c1a37c`
- Formula licence metadata: MIT
- Extracted LLVM `LICENSE.TXT`: Apache-2.0 with LLVM exceptions
- Upstream: `https://openmp.llvm.org/`
- Formula metadata generated: `2026-08-30`

The ignored archive and extracted runtime live below `.deps/`. The bottle
contains `LICENSE.TXT` and `sbom.spdx.json`; both are preserved alongside the
runtime. `scripts/acquire_libomp_runtime.sh` fetches an anonymous short-lived
GHCR pull token, verifies the exact checksum, and extracts only after a match.
The token is never written or printed. Commands opt into the local runtime with
`DYLD_LIBRARY_PATH=.deps/libomp/23.1.0/lib`; nothing is installed system-wide.

Observed host at acquisition: Apple Silicon, macOS 26.6.2 build 25G83.

## LightGBM binary

- Package: `lightgbm==4.6.0` (already pinned in `requirements.txt`)
- Upstream: `https://github.com/microsoft/LightGBM`
- Licence: MIT
- Apple-silicon wheel filename:
  `lightgbm-4.6.0-py3-none-macosx_12_0_arm64.whl`
- Wheel SHA-256:
  `2dafd98d4e02b844ceb0b61450a660681076b1ea6c7adb8c566dfd66832aafad`
- Installed `lib_lightgbm.dylib` SHA-256:
  `50f62eef76a25c7dbd5b79c998d59a5dff4874c595f7fb8d197826c2bfbd8a92`
- Extracted `libomp.dylib` SHA-256:
  `fb209ffe83554f5a4af68f469a3fa331f52a5c3bc17289bdaa452c4e07328591`

An import check reported LightGBM `4.6.0`. A two-query synthetic
`lambdarank` fit completed two boosting rounds and returned six finite
predictions with the repository-local runtime enabled.
