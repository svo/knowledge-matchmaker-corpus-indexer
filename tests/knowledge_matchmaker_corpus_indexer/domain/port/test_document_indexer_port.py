from abc import ABC

from assertpy import assert_that

from knowledge_matchmaker_corpus_indexer.domain.port.document_indexer_port import DocumentIndexerPort


class TestDocumentIndexerPort:
    def test_should_be_abstract_when_defined(self) -> None:
        assert_that(issubclass(DocumentIndexerPort, ABC)).is_true()
