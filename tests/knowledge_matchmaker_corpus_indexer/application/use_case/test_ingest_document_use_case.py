from unittest.mock import Mock

import pytest
from assertpy import assert_that

from knowledge_matchmaker_corpus_indexer.application.use_case.ingest_document_use_case import (
    GetIngestionJobUseCase,
    IngestDocumentUseCase,
)
from knowledge_matchmaker_corpus_indexer.domain.model.corpus_document import CorpusDocument
from knowledge_matchmaker_corpus_indexer.domain.model.ingestion_job import IngestionJob, IngestionStatus
from knowledge_matchmaker_corpus_indexer.domain.service.corpus_indexer import CorpusIndexer


class TestIngestDocumentUseCase:
    @pytest.fixture
    def mock_corpus_indexer(self) -> Mock:
        return Mock(spec=CorpusIndexer)

    @pytest.fixture
    def use_case(self, mock_corpus_indexer) -> IngestDocumentUseCase:
        return IngestDocumentUseCase(mock_corpus_indexer)

    @pytest.fixture
    def sample_document(self) -> CorpusDocument:
        return CorpusDocument(
            title="Sample Title",
            author="Sample Author",
            source_url="https://example.com",
            publication_date="2024-01-01",
            full_text="Sample content",
        )

    def test_should_call_indexer_with_document(self, use_case, mock_corpus_indexer, sample_document):
        use_case.execute(sample_document)

        mock_corpus_indexer.index.assert_called_once()
        assert_that(mock_corpus_indexer.index.call_args[0][0]).is_equal_to(sample_document)

    def test_should_return_queued_job(self, use_case, mock_corpus_indexer, sample_document):
        result = use_case.execute(sample_document)

        assert_that(result.status).is_equal_to(IngestionStatus.QUEUED)

    def test_should_return_job_with_document_title(self, use_case, mock_corpus_indexer, sample_document):
        result = use_case.execute(sample_document)

        assert_that(result.document_title).is_equal_to(sample_document.title)


class TestGetIngestionJobUseCase:
    def test_should_return_job_status_from_indexer(self) -> None:
        mock_indexer = Mock(spec=CorpusIndexer)
        expected_job = IngestionJob(job_id="job-1", document_title="Doc", status=IngestionStatus.COMPLETE)
        mock_indexer.get_job_status.return_value = expected_job
        use_case = GetIngestionJobUseCase(mock_indexer)

        result = use_case.execute("job-1")

        assert_that(result).is_equal_to(expected_job)
