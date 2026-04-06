import pytest
from assertpy import assert_that

from knowledge_matchmaker_corpus_indexer.domain.model.ingestion_job import IngestionJob, IngestionStatus
from knowledge_matchmaker_corpus_indexer.infrastructure.persistence.in_memory.in_memory_job_repository import InMemoryJobRepository


class TestInMemoryJobRepository:
    def _make_job(self, job_id: str = "abc") -> IngestionJob:
        return IngestionJob(job_id=job_id, document_title="Test Doc", status=IngestionStatus.PENDING)

    def test_should_return_job_when_saved_and_found(self) -> None:
        repo = InMemoryJobRepository()
        job = self._make_job()
        repo.save(job)

        result = repo.find("abc")

        assert_that(result.job_id).is_equal_to("abc")

    def test_should_raise_key_error_when_job_not_found(self) -> None:
        repo = InMemoryJobRepository()

        assert_that(repo.find).raises(KeyError).when_called_with("missing")

    def test_should_update_job_when_saved_again(self) -> None:
        repo = InMemoryJobRepository()
        repo.save(self._make_job())
        updated_job = IngestionJob(job_id="abc", document_title="Test Doc", status=IngestionStatus.COMPLETED)
        repo.save(updated_job)

        result = repo.find("abc")

        assert_that(result.status).is_equal_to(IngestionStatus.COMPLETED)
