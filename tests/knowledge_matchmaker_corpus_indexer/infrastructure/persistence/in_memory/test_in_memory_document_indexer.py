from assertpy import assert_that

from knowledge_matchmaker_corpus_indexer.domain.model.corpus_document import CorpusDocument
from knowledge_matchmaker_corpus_indexer.infrastructure.persistence.in_memory.in_memory_document_indexer import InMemoryDocumentIndexer


class TestInMemoryDocumentIndexer:
    def test_should_index_document_when_index_called(self) -> None:
        indexer = InMemoryDocumentIndexer()
        doc = CorpusDocument(title="T", author="A", source_url="http://x.com", publication_date="2024-01-01", content="text")

        indexer.index("job1", doc)

        assert_that(len(indexer.indexed)).is_equal_to(1)

    def test_should_store_job_id_with_document_when_indexed(self) -> None:
        indexer = InMemoryDocumentIndexer()
        doc = CorpusDocument(title="T", author="A", source_url="http://x.com", publication_date="2024-01-01", content="text")

        indexer.index("job1", doc)

        assert_that(indexer.indexed[0][0]).is_equal_to("job1")
