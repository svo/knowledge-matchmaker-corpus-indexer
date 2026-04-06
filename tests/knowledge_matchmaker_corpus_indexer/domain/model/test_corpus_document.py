from assertpy import assert_that

from knowledge_matchmaker_corpus_indexer.domain.model.corpus_document import CorpusDocument


def make_document(**kwargs):
    defaults = {
        "title": "Test Title",
        "author": "Test Author",
        "source_url": "https://example.com",
        "publication_date": "2024-01-01",
        "content": "Test content",
    }
    defaults.update(kwargs)
    return CorpusDocument(**defaults)


def test_should_have_title():
    assert_that(make_document(title="My Title").title).is_equal_to("My Title")


def test_should_have_author():
    assert_that(make_document(author="Jane Doe").author).is_equal_to("Jane Doe")


def test_should_have_source_url():
    assert_that(make_document(source_url="https://test.com").source_url).is_equal_to("https://test.com")


def test_should_have_publication_date():
    assert_that(make_document(publication_date="2023-06-15").publication_date).is_equal_to("2023-06-15")


def test_should_have_content():
    assert_that(make_document(content="Some content here").content).is_equal_to("Some content here")
