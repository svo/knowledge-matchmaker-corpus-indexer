from unittest.mock import Mock

from assertpy import assert_that
import chromadb

from knowledge_matchmaker_corpus_indexer.domain.model.corpus_document import CorpusDocument
from knowledge_matchmaker_corpus_indexer.infrastructure.chroma.chroma_document_indexer import ChromaDocumentIndexer


class TestChromaDocumentIndexer:
    def test_should_call_collection_add_when_indexing(self) -> None:
        mock_collection = Mock()
        mock_client = Mock(spec=chromadb.ClientAPI)
        mock_client.get_or_create_collection.return_value = mock_collection
        indexer = ChromaDocumentIndexer(client=mock_client)
        doc = CorpusDocument(
            title="T", author="A", source_url="http://x.com", publication_date="2024-01-01", content="text"
        )

        indexer.index("job1", doc)

        assert_that(mock_collection.add.call_count).is_equal_to(1)

    def test_should_use_job_id_as_document_id_when_indexing(self) -> None:
        mock_collection = Mock()
        mock_client = Mock(spec=chromadb.ClientAPI)
        mock_client.get_or_create_collection.return_value = mock_collection
        indexer = ChromaDocumentIndexer(client=mock_client)
        doc = CorpusDocument(
            title="T", author="A", source_url="http://x.com", publication_date="2024-01-01", content="text"
        )

        indexer.index("job1", doc)

        assert_that(mock_collection.add.call_args.kwargs["ids"]).contains("job1")
