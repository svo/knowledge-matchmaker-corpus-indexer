from unittest.mock import Mock

from assertpy import assert_that

from knowledge_matchmaker_corpus_indexer.interface.api.data_transfer_object.ingest_document_data_transfer_object import (
    IngestDocumentRequestDto,
)


class TestIngestDocumentRequestDtoFromDomainModel:
    def test_should_map_title_from_domain_model(self) -> None:
        domain_model = Mock()
        domain_model.title = "Test Title"
        domain_model.author = "Author"
        domain_model.source_url = "http://example.com"
        domain_model.publication_date = "2024-01-01"
        domain_model.full_text = "Some content"

        result = IngestDocumentRequestDto.from_domain_model(domain_model)

        assert_that(result.title).is_equal_to("Test Title")
