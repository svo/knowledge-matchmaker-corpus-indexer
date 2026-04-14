from assertpy import assert_that

from knowledge_matchmaker_corpus_indexer.domain.service.embedder import Embedder


class TestEmbedder:
    def test_should_be_abstract_class(self) -> None:
        assert_that(Embedder.__abstractmethods__).contains("embed")

    def test_should_not_be_instantiable_directly(self) -> None:
        assert_that(Embedder).raises(TypeError).when_called_with()
