#!/usr/bin/env bash

# shellcheck disable=SC1090,SC1091
source ~/.local/pipx/venvs/knowledge-matchmaker-corpus-indexer/bin/activate &&

python3 -m knowledge_matchmaker_corpus_indexer
