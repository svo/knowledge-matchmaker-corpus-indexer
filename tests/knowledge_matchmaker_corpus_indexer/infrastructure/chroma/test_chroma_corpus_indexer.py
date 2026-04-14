from assertpy import assert_that

from knowledge_matchmaker_corpus_indexer.domain.model.corpus_document import CorpusDocument
from knowledge_matchmaker_corpus_indexer.domain.model.ingestion_job import IngestionStatus
from knowledge_matchmaker_corpus_indexer.domain.service.embedder import Embedder
from knowledge_matchmaker_corpus_indexer.infrastructure.chroma.chroma_corpus_indexer import ChromaCorpusIndexer


class StubEmbedder(Embedder):
    def embed(self, text: str) -> list[float]:
        return [0.1, 0.2, 0.3]


def _make_document() -> CorpusDocument:
    return CorpusDocument(
        title="Test Title",
        author="Test Author",
        source_url="http://example.com",
        publication_date="2024-01-01",
        full_text="Test content",
    )


class TestChromaCorpusIndexer:
    def test_should_store_job_with_complete_status_when_indexing(self, tmp_path) -> None:
        indexer = ChromaCorpusIndexer(embedder=StubEmbedder(), chroma_data_path=str(tmp_path))

        indexer.index(_make_document(), "job-1")
        result = indexer.get_job_status("job-1")

        assert_that(result.status).is_equal_to(IngestionStatus.COMPLETE)

    def test_should_store_document_title_in_job_when_indexing(self, tmp_path) -> None:
        indexer = ChromaCorpusIndexer(embedder=StubEmbedder(), chroma_data_path=str(tmp_path))

        indexer.index(_make_document(), "job-1")
        result = indexer.get_job_status("job-1")

        assert_that(result.document_title).is_equal_to("Test Title")

    def test_should_persist_embedding_in_collection_when_indexing(self, tmp_path) -> None:
        indexer = ChromaCorpusIndexer(embedder=StubEmbedder(), chroma_data_path=str(tmp_path))

        indexer.index(_make_document(), "job-1")
        results = indexer._collection.get(ids=["job-1"])

        assert_that(results["ids"]).contains("job-1")

    def test_should_raise_key_error_when_job_not_found(self, tmp_path) -> None:
        indexer = ChromaCorpusIndexer(embedder=StubEmbedder(), chroma_data_path=str(tmp_path))

        assert_that(indexer.get_job_status).raises(KeyError).when_called_with("missing")

    def test_should_use_embedder_to_compute_embedding_when_indexing(self, tmp_path) -> None:
        call_log: list[str] = []

        class TrackingEmbedder(Embedder):
            def embed(self, text: str) -> list[float]:
                call_log.append(text)
                return [0.1, 0.2, 0.3]

        indexer = ChromaCorpusIndexer(embedder=TrackingEmbedder(), chroma_data_path=str(tmp_path))

        indexer.index(_make_document(), "job-1")

        assert_that(call_log).contains("Test content")
