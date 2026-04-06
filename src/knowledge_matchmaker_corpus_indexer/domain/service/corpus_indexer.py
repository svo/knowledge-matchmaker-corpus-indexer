from abc import ABC, abstractmethod

from knowledge_matchmaker_corpus_indexer.domain.model.corpus_document import CorpusDocument
from knowledge_matchmaker_corpus_indexer.domain.model.ingestion_job import IngestionJob


class CorpusIndexer(ABC):
    @abstractmethod
    def index(self, document: CorpusDocument, job_id: str) -> None:
        pass

    @abstractmethod
    def get_job_status(self, job_id: str) -> IngestionJob:
        pass
