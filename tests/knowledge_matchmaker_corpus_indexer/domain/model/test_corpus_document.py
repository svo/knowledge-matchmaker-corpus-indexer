from assertpy import assert_that

from knowledge_matchmaker_corpus_indexer.domain.model.corpus_document import CorpusDocument


class TestCorpusDocument:
    def test_should_store_title_when_created(self) -> None:
        doc = CorpusDocument(title="Test", author="Author", source_url="http://example.com", full_text="text")

        assert_that(doc.title).is_equal_to("Test")

    def test_should_store_author_when_created(self) -> None:
        doc = CorpusDocument(title="Test", author="Author", source_url="http://example.com", full_text="text")

        assert_that(doc.author).is_equal_to("Author")

    def test_should_store_source_url_when_created(self) -> None:
        doc = CorpusDocument(title="Test", author="Author", source_url="http://example.com", full_text="text")

        assert_that(doc.source_url).is_equal_to("http://example.com")

    def test_should_store_full_text_when_created(self) -> None:
        doc = CorpusDocument(title="Test", author="Author", source_url="http://example.com", full_text="text")

        assert_that(doc.full_text).is_equal_to("text")

    def test_should_have_empty_publication_date_by_default(self) -> None:
        doc = CorpusDocument(title="Test", author="Author", source_url="http://example.com", full_text="text")

        assert_that(doc.publication_date).is_equal_to("")
