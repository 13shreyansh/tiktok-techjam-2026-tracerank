#!/bin/sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
data_root="$repo_root/data"
archive="$data_root/KuaiRand-1K.tar.gz"
partial="$archive.part"
source_url="https://zenodo.org/records/10439422/files/KuaiRand-1K.tar.gz"
expected_bytes="1135436720"
expected_md5="6b0b9c8222d67fcd4c676218edca3f1f"

md5_value() {
  if command -v md5 >/dev/null 2>&1; then
    md5 -q "$1"
  else
    md5sum "$1" | awk '{print $1}'
  fi
}

file_bytes() {
  if stat -f '%z' "$1" >/dev/null 2>&1; then
    stat -f '%z' "$1"
  else
    stat -c '%s' "$1"
  fi
}

verify_archive() {
  actual_bytes=$(file_bytes "$1")
  if [ "$actual_bytes" != "$expected_bytes" ]; then
    echo "Archive size mismatch: $actual_bytes" >&2
    echo "Expected: $expected_bytes" >&2
    exit 1
  fi
  actual_md5=$(md5_value "$1")
  if [ "$actual_md5" != "$expected_md5" ]; then
    echo "Archive checksum mismatch: $actual_md5" >&2
    echo "Expected: $expected_md5" >&2
    exit 1
  fi
}

mkdir -p "$data_root"

if [ -f "$archive" ]; then
  verify_archive "$archive"
else
  curl -L --fail --show-error --retry 5 --retry-delay 5 \
    --continue-at - --output "$partial" "$source_url"
  verify_archive "$partial"
  mv "$partial" "$archive"
fi

if ! tar -tzf "$archive" | awk '
  BEGIN { bad = 0 }
  /^\// || /(^|\/)\.\.($|\/)/ { print "unsafe path: " $0; bad = 1 }
  END { exit bad }
'; then
  echo "Archive path safety check failed" >&2
  exit 1
fi

if ! tar -tvzf "$archive" | awk '
  BEGIN { bad = 0 }
  substr($1, 1, 1) != "-" && substr($1, 1, 1) != "d" {
    print "unexpected entry type: " $0
    bad = 1
  }
  END { exit bad }
'; then
  echo "Archive entry-type safety check failed" >&2
  exit 1
fi

tar -xzf "$archive" -C "$data_root"
echo "KuaiRand-1K ready at $data_root/KuaiRand-1K"
echo "Bytes verified: $expected_bytes"
echo "MD5 verified: $expected_md5"

