from unittest.mock import Mock, patch

from assertpy import assert_that

from knowledge_matchmaker_corpus_indexer.domain.model.corpus_document import CorpusDocument
from knowledge_matchmaker_corpus_indexer.domain.model.ingestion_job import IngestionStatus
from knowledge_matchmaker_corpus_indexer.infrastructure.chroma.chroma_corpus_indexer import ChromaCorpusIndexer


def _make_document() -> CorpusDocument:
    return CorpusDocument(
        title="Test Title",
        author="Test Author",
        source_url="http://example.com",
        publication_date="2024-01-01",
        content="Test content",
    )


def _make_mock_embedding_response() -> Mock:
    mock_embedding = Mock()
    mock_embedding.embedding = [0.1, 0.2, 0.3]
    mock_response = Mock()
    mock_response.data = [mock_embedding]
    return mock_response


class TestChromaCorpusIndexer:
    @patch("knowledge_matchmaker_corpus_indexer.infrastructure.chroma.chroma_corpus_indexer.openai")
    @patch("knowledge_matchmaker_corpus_indexer.infrastructure.chroma.chroma_corpus_indexer.chromadb")
    def test_should_store_job_with_completed_status_when_indexing(self, mock_chromadb, mock_openai) -> None:
        mock_openai.OpenAI.return_value.embeddings.create.return_value = _make_mock_embedding_response()
        indexer = ChromaCorpusIndexer()

        indexer.index(_make_document(), "job-1")
        result = indexer.get_job_status("job-1")

        assert_that(result.status).is_equal_to(IngestionStatus.COMPLETED)

    @patch("knowledge_matchmaker_corpus_indexer.infrastructure.chroma.chroma_corpus_indexer.openai")
    @patch("knowledge_matchmaker_corpus_indexer.infrastructure.chroma.chroma_corpus_indexer.chromadb")
    def test_should_store_document_title_in_job_when_indexing(self, mock_chromadb, mock_openai) -> None:
        mock_openai.OpenAI.return_value.embeddings.create.return_value = _make_mock_embedding_response()
        indexer = ChromaCorpusIndexer()

        indexer.index(_make_document(), "job-1")
        result = indexer.get_job_status("job-1")

        assert_that(result.document_title).is_equal_to("Test Title")

    @patch("knowledge_matchmaker_corpus_indexer.infrastructure.chroma.chroma_corpus_indexer.openai")
    @patch("knowledge_matchmaker_corpus_indexer.infrastructure.chroma.chroma_corpus_indexer.chromadb")
    def test_should_add_embedding_to_collection_when_indexing(self, mock_chromadb, mock_openai) -> None:
        mock_collection = Mock()
        mock_chromadb.EphemeralClient.return_value.get_or_create_collection.return_value = mock_collection
        mock_openai.OpenAI.return_value.embeddings.create.return_value = _make_mock_embedding_response()
        indexer = ChromaCorpusIndexer()

        indexer.index(_make_document(), "job-1")

        assert_that(mock_collection.add.call_count).is_equal_to(1)

    @patch("knowledge_matchmaker_corpus_indexer.infrastructure.chroma.chroma_corpus_indexer.openai")
    @patch("knowledge_matchmaker_corpus_indexer.infrastructure.chroma.chroma_corpus_indexer.chromadb")
    def test_should_raise_key_error_when_job_not_found(self, mock_chromadb, mock_openai) -> None:
        indexer = ChromaCorpusIndexer()

        assert_that(indexer.get_job_status).raises(KeyError).when_called_with("missing")
