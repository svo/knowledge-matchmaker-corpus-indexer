from assertpy import assert_that

from knowledge_matchmaker_corpus_indexer.domain.model.corpus_document import CorpusDocument
from knowledge_matchmaker_corpus_indexer.domain.model.ingestion_job import IngestionJob, JobStatus


class TestIngestionJob:
    def _make_doc(self) -> CorpusDocument:
        return CorpusDocument(title="T", author="A", source_url="http://x.com", full_text="text")

    def test_should_store_job_id_when_created(self) -> None:
        job = IngestionJob(job_id="abc", status=JobStatus.queued, document=self._make_doc())

        assert_that(job.job_id).is_equal_to("abc")

    def test_should_store_status_when_created(self) -> None:
        job = IngestionJob(job_id="abc", status=JobStatus.queued, document=self._make_doc())

        assert_that(job.status).is_equal_to(JobStatus.queued)

    def test_should_store_document_when_created(self) -> None:
        doc = self._make_doc()
        job = IngestionJob(job_id="abc", status=JobStatus.queued, document=doc)

        assert_that(job.document).is_equal_to(doc)
