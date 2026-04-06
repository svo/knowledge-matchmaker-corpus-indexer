#!/usr/bin/env bash

docker run --rm -v "$(pwd)":/working-dir svanosselaer/knowledge-matchmaker-corpus-indexer-builder:latest
