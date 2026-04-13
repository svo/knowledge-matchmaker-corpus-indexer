from typing import Dict, Sequence, cast

import chromadb
import openai

from knowledge_matchmaker_corpus_indexer.domain.model.corpus_document import CorpusDocument
from knowledge_matchmaker_corpus_indexer.domain.model.ingestion_job import IngestionJob, IngestionStatus
from knowledge_matchmaker_corpus_indexer.domain.service.corpus_indexer import CorpusIndexer


class ChromaCorpusIndexer(CorpusIndexer):
    def __init__(self) -> None:
        self._client = chromadb.EphemeralClient()
        self._collection = self._client.get_or_create_collection("corpus")
        self._jobs: Dict[str, IngestionJob] = {}

    def index(self, document: CorpusDocument, job_id: str) -> None:
        embedding_response = openai.OpenAI().embeddings.create(
            input=document.content,
            model="text-embedding-3-small",
        )
        embedding = embedding_response.data[0].embedding

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
            status=IngestionStatus.COMPLETED,
        )

    def get_job_status(self, job_id: str) -> IngestionJob:
        return self._jobs[job_id]
