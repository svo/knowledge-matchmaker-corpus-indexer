from unittest.mock import Mock

from assertpy import assert_that

from knowledge_matchmaker_corpus_indexer.application.use_case.ingest_document_use_case import IngestDocumentUseCase
from knowledge_matchmaker_corpus_indexer.domain.model.corpus_document import CorpusDocument
from knowledge_matchmaker_corpus_indexer.domain.model.ingestion_job import JobStatus
from knowledge_matchmaker_corpus_indexer.domain.port.document_indexer_port import DocumentIndexerPort
from knowledge_matchmaker_corpus_indexer.domain.port.job_repository_port import JobRepositoryPort


class TestIngestDocumentUseCase:
    def _make_doc(self) -> CorpusDocument:
        return CorpusDocument(title="T", author="A", source_url="http://x.com", full_text="text")

    def test_should_return_complete_status_when_indexing_succeeds(self) -> None:
        mock_indexer = Mock(spec=DocumentIndexerPort)
        mock_repo = Mock(spec=JobRepositoryPort)
        use_case = IngestDocumentUseCase(indexer=mock_indexer, job_repository=mock_repo)

        result = use_case.execute(self._make_doc())

        assert_that(result.status).is_equal_to(JobStatus.complete)

    def test_should_call_indexer_when_ingesting(self) -> None:
        mock_indexer = Mock(spec=DocumentIndexerPort)
        mock_repo = Mock(spec=JobRepositoryPort)
        use_case = IngestDocumentUseCase(indexer=mock_indexer, job_repository=mock_repo)

        use_case.execute(self._make_doc())

        assert_that(mock_indexer.index.call_count).is_equal_to(1)

    def test_should_save_job_to_repository_when_ingesting(self) -> None:
        mock_indexer = Mock(spec=DocumentIndexerPort)
        mock_repo = Mock(spec=JobRepositoryPort)
        use_case = IngestDocumentUseCase(indexer=mock_indexer, job_repository=mock_repo)

        use_case.execute(self._make_doc())

        assert_that(mock_repo.save.call_count).is_greater_than(0)

    def test_should_return_job_with_job_id_when_ingesting(self) -> None:
        mock_indexer = Mock(spec=DocumentIndexerPort)
        mock_repo = Mock(spec=JobRepositoryPort)
        use_case = IngestDocumentUseCase(indexer=mock_indexer, job_repository=mock_repo)

        result = use_case.execute(self._make_doc())

        assert_that(result.job_id).is_not_empty()
