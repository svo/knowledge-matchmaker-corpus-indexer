from unittest.mock import Mock

from assertpy import assert_that

from knowledge_matchmaker_corpus_indexer.application.use_case.get_job_use_case import GetJobUseCase
from knowledge_matchmaker_corpus_indexer.domain.model.corpus_document import CorpusDocument
from knowledge_matchmaker_corpus_indexer.domain.model.ingestion_job import IngestionJob, JobStatus
from knowledge_matchmaker_corpus_indexer.domain.port.job_repository_port import JobRepositoryPort


class TestGetJobUseCase:
    def _make_job(self) -> IngestionJob:
        doc = CorpusDocument(title="T", author="A", source_url="http://x.com", full_text="text")
        return IngestionJob(job_id="abc", status=JobStatus.complete, document=doc)

    def test_should_return_job_when_found(self) -> None:
        mock_repo = Mock(spec=JobRepositoryPort)
        mock_repo.find.return_value = self._make_job()
        use_case = GetJobUseCase(job_repository=mock_repo)

        result = use_case.execute("abc")

        assert_that(result.job_id).is_equal_to("abc")

    def test_should_call_repository_when_getting_job(self) -> None:
        mock_repo = Mock(spec=JobRepositoryPort)
        mock_repo.find.return_value = self._make_job()
        use_case = GetJobUseCase(job_repository=mock_repo)

        use_case.execute("abc")

        mock_repo.find.assert_called_once_with("abc")
