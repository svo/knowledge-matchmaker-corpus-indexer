from assertpy import assert_that

from knowledge_matchmaker_corpus_indexer.domain.model.ingestion_job import IngestionJob, IngestionStatus


def make_job(**kwargs):
    defaults = {
        "job_id": "test-job-id",
        "document_title": "Test Document",
        "status": IngestionStatus.QUEUED,
    }
    defaults.update(kwargs)
    return IngestionJob(**defaults)


def test_should_have_job_id():
    assert_that(make_job(job_id="abc-123").job_id).is_equal_to("abc-123")


def test_should_have_document_title():
    assert_that(make_job(document_title="My Document").document_title).is_equal_to("My Document")


def test_should_have_status():
    assert_that(make_job(status=IngestionStatus.COMPLETE).status).is_equal_to(IngestionStatus.COMPLETE)


def test_should_default_error_message_to_none():
    assert_that(make_job().error_message).is_none()
