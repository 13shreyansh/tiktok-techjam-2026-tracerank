#!/bin/sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
data_root="$repo_root/data"
archive="$data_root/KuaiRand-Pure.tar.gz"
partial="$archive.part"
source_url="https://zenodo.org/records/10439422/files/KuaiRand-Pure.tar.gz"
expected_md5="0820331067a3784d9691136f772b35a7"

md5_value() {
  if command -v md5 >/dev/null 2>&1; then
    md5 -q "$1"
  else
    md5sum "$1" | awk '{print $1}'
  fi
}

mkdir -p "$data_root"

if [ -f "$archive" ]; then
  actual_md5=$(md5_value "$archive")
  if [ "$actual_md5" != "$expected_md5" ]; then
    echo "Existing archive checksum mismatch: $actual_md5" >&2
    echo "Expected: $expected_md5" >&2
    exit 1
  fi
else
  curl -L --fail --show-error --retry 3 --output "$partial" "$source_url"
  actual_md5=$(md5_value "$partial")
  if [ "$actual_md5" != "$expected_md5" ]; then
    echo "Downloaded archive checksum mismatch: $actual_md5" >&2
    echo "Expected: $expected_md5" >&2
    exit 1
  fi
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
echo "KuaiRand-Pure ready at $data_root/KuaiRand-Pure"
echo "MD5 verified: $expected_md5"
