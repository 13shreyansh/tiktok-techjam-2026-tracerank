#!/bin/sh
set -eu

url='https://zenodo.org/records/18159199/files/kuairand_video_categories.csv'
expected_prefix_sha256='c91886658c1fc1897ebd6e808ebcc87acfddb4548d5acb8faa70ee8ccd3a091c'
expected_subset_sha256='45dd0fb396d4622ddd14e6aca2c28c2e57c220a18499cfed742abba794e6e439'
output_dir='data/kuairand-supplemental'
task_tmp_dir="$(mktemp -d)"
trap 'rm -rf "$task_tmp_dir"' EXIT

curl --fail --location --range 0-2097151 \
  --output "$task_tmp_dir/categories.prefix.csv" "$url"

prefix_size="$(wc -c < "$task_tmp_dir/categories.prefix.csv" | tr -d ' ')"
test "$prefix_size" = '2097152'
prefix_sha256="$(shasum -a 256 "$task_tmp_dir/categories.prefix.csv" | awk '{print $1}')"
test "$prefix_sha256" = "$expected_prefix_sha256"

head -n 7584 "$task_tmp_dir/categories.prefix.csv" > "$task_tmp_dir/categories.pure.csv"
awk -F, '
  NR == 1 { next }
  $1 != NR - 2 { exit 1 }
  END { if (NR != 7584) exit 1 }
' "$task_tmp_dir/categories.pure.csv"
subset_sha256="$(shasum -a 256 "$task_tmp_dir/categories.pure.csv" | awk '{print $1}')"
test "$subset_sha256" = "$expected_subset_sha256"

mkdir -p "$output_dir"
mv "$task_tmp_dir/categories.prefix.csv" "$output_dir/kuairand_video_categories.prefix.csv"
mv "$task_tmp_dir/categories.pure.csv" "$output_dir/kuairand_video_categories_pure.csv"

printf '%s\n' "verified rows=7583 ids=0..7582 sha256=$subset_sha256"
