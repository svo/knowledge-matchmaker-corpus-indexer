from abc import ABC, abstractmethod

from knowledge_matchmaker_corpus_indexer.domain.model.ingestion_job import IngestionJob


class JobRepositoryPort(ABC):
    @abstractmethod
    def save(self, job: IngestionJob) -> None:
        raise NotImplementedError

    @abstractmethod
    def find(self, job_id: str) -> IngestionJob:
        raise NotImplementedError
