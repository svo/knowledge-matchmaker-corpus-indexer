from knowledge_matchmaker_corpus_indexer.domain.model.ingestion_job import IngestionJob
from knowledge_matchmaker_corpus_indexer.domain.port.job_repository_port import JobRepositoryPort


class InMemoryJobRepository(JobRepositoryPort):
    def __init__(self) -> None:
        self._jobs: dict[str, IngestionJob] = {}

    def save(self, job: IngestionJob) -> None:
        self._jobs[job.job_id] = job

    def find(self, job_id: str) -> IngestionJob:
        if job_id not in self._jobs:
            raise KeyError(f"Job {job_id} not found")
        return self._jobs[job_id]
