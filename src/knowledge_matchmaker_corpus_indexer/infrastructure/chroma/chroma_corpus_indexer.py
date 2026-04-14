import os
from typing import Dict, Sequence, cast

import chromadb

from knowledge_matchmaker_corpus_indexer.domain.model.corpus_document import CorpusDocument
from knowledge_matchmaker_corpus_indexer.domain.model.ingestion_job import IngestionJob, IngestionStatus
from knowledge_matchmaker_corpus_indexer.domain.service.corpus_indexer import CorpusIndexer
from knowledge_matchmaker_corpus_indexer.domain.service.embedder import Embedder

CHROMA_DATA_PATH_DEFAULT = "/data/chroma"


class ChromaCorpusIndexer(CorpusIndexer):
    def __init__(self, embedder: Embedder, chroma_data_path: str = "") -> None:
        self._embedder = embedder
        resolved_path = chroma_data_path or os.environ.get("CHROMA_DATA_PATH", CHROMA_DATA_PATH_DEFAULT)
        self._client = chromadb.PersistentClient(path=resolved_path)
        self._collection = self._client.get_or_create_collection("corpus")
        self._jobs: Dict[str, IngestionJob] = {}

    def index(self, document: CorpusDocument, job_id: str) -> None:
        embedding = self._embedder.embed(document.full_text)

        self._collection.add(
            ids=[job_id],
            embeddings=[cast(Sequence[float], embedding)],
            metadatas=[
                {
                    "title": document.title,
                    "author": document.author,
                    "source_url": document.source_url,
                    "publication_date": document.publication_date,
                }
            ],
        )

        self._jobs[job_id] = IngestionJob(
            job_id=job_id,
            document_title=document.title,
            status=IngestionStatus.COMPLETE,
        )

    def get_job_status(self, job_id: str) -> IngestionJob:
        return self._jobs[job_id]
