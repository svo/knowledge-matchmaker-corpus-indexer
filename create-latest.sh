#!/usr/bin/env bash

image=$1

docker manifest rm "svanosselaer/knowledge-matchmaker-corpus-indexer-${image}:latest" 2>/dev/null || true

docker manifest create \
  "svanosselaer/knowledge-matchmaker-corpus-indexer-${image}:latest" \
  --amend "svanosselaer/knowledge-matchmaker-corpus-indexer-${image}:amd64" \
  --amend "svanosselaer/knowledge-matchmaker-corpus-indexer-${image}:arm64" &&
docker manifest push "svanosselaer/knowledge-matchmaker-corpus-indexer-${image}:latest"
