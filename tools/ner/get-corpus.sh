#!/bin/bash

set -e

script_dir=$(cd "$(dirname ${BASH_SOURCE[0]})"; pwd);
corpus_dir=$(cd "$script_dir"; cd ../..; pwd)/corpus

if [[ -z "$SPIDER_SOURCE_URL" ]]; then
  echo 'Please set \$SPIDER_SOURCE_URL env var'
  exit -1
fi

mkdir -p corpus_dir
pushd "$script_dir"
psql "$SPIDER_SOURCE_URL" < export.sql

echo "Sorting and deuplicating data"

mv company.csv "$corpus_dir/company-news.csv"

popd

