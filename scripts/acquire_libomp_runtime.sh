#!/bin/sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
RUNTIME_VERSION="23.1.0"
BOTTLE_SHA256="462a36670e56b7804c607e16c4d1b013bbca2a531b39b612a28d8f1bb0c1a37c"
BOTTLE_URL="https://ghcr.io/v2/homebrew/core/libomp/blobs/sha256:${BOTTLE_SHA256}"
CACHE_DIR="${ROOT_DIR}/.deps/cache"
ARCHIVE_PATH="${CACHE_DIR}/libomp-${RUNTIME_VERSION}.arm64_tahoe.bottle.tar.gz"
INSTALL_DIR="${ROOT_DIR}/.deps/libomp/${RUNTIME_VERSION}"

if [ "$(uname -m)" != "arm64" ]; then
  echo "This acquisition record is locked to Apple Silicon." >&2
  exit 1
fi
mkdir -p "${CACHE_DIR}" "${ROOT_DIR}/.deps/libomp"
if [ ! -f "${ARCHIVE_PATH}" ]; then
  TASK_LIBOMP_TOKEN=$(
    curl -fsSL "https://ghcr.io/token?scope=repository:homebrew/core/libomp:pull" |
      /usr/bin/python3 -c 'import json,sys; print(json.load(sys.stdin)["token"])'
  )
  curl -fL --retry 3 \
    -H "Authorization: Bearer ${TASK_LIBOMP_TOKEN}" \
    -o "${ARCHIVE_PATH}.part" "${BOTTLE_URL}"
  mv "${ARCHIVE_PATH}.part" "${ARCHIVE_PATH}"
fi
OBSERVED_SHA256=$(shasum -a 256 "${ARCHIVE_PATH}" | awk '{print $1}')
if [ "${OBSERVED_SHA256}" != "${BOTTLE_SHA256}" ]; then
  echo "libomp bottle checksum mismatch" >&2
  exit 1
fi
if [ ! -f "${INSTALL_DIR}/lib/libomp.dylib" ]; then
  tar -xzf "${ARCHIVE_PATH}" -C "${ROOT_DIR}/.deps"
fi
test -f "${INSTALL_DIR}/LICENSE.TXT"
test -f "${INSTALL_DIR}/sbom.spdx.json"
test -f "${INSTALL_DIR}/lib/libomp.dylib"
echo "libomp ${RUNTIME_VERSION} ready: ${INSTALL_DIR}"
