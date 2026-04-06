from knowledge_matchmaker_corpus_indexer.domain.model.ingestion_job import IngestionJob
from knowledge_matchmaker_corpus_indexer.domain.port.job_repository_port import JobRepositoryPort


class GetJobUseCase:
    def __init__(self, job_repository: JobRepositoryPort) -> None:
        self._job_repository = job_repository

    def execute(self, job_id: str) -> IngestionJob:
        return self._job_repository.find(job_id)
