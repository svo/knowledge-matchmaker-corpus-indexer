from unittest.mock import Mock

from assertpy import assert_that
from fastapi import FastAPI
from fastapi.testclient import TestClient

from knowledge_matchmaker_corpus_indexer.application.use_case.get_job_use_case import GetJobUseCase
from knowledge_matchmaker_corpus_indexer.application.use_case.ingest_document_use_case import IngestDocumentUseCase
from knowledge_matchmaker_corpus_indexer.domain.model.ingestion_job import IngestionJob, IngestionStatus
from knowledge_matchmaker_corpus_indexer.interface.api.controller.ingest_controller import create_ingest_controller


def _make_client(ingest_use_case: IngestDocumentUseCase, get_job_use_case: GetJobUseCase) -> TestClient:
    app = FastAPI()
    app.include_router(create_ingest_controller(ingest_use_case, get_job_use_case))
    return TestClient(app)


def _make_complete_job(job_id: str = "abc") -> IngestionJob:
    return IngestionJob(job_id=job_id, document_title="T", status=IngestionStatus.COMPLETED)


class TestIngestController:
    def test_should_return_202_when_ingest_succeeds(self) -> None:
        ingest_uc = Mock(spec=IngestDocumentUseCase)
        ingest_uc.execute.return_value = _make_complete_job()
        get_job_uc = Mock(spec=GetJobUseCase)
        client = _make_client(ingest_uc, get_job_uc)

        response = client.post("/ingest", json={"title": "T", "author": "A", "source_url": "http://x.com", "content": "text", "publication_date": "2024-01-01"})

        assert_that(response.status_code).is_equal_to(202)

    def test_should_return_job_id_when_ingest_succeeds(self) -> None:
        ingest_uc = Mock(spec=IngestDocumentUseCase)
        ingest_uc.execute.return_value = _make_complete_job("my-job-id")
        get_job_uc = Mock(spec=GetJobUseCase)
        client = _make_client(ingest_uc, get_job_uc)

        response = client.post("/ingest", json={"title": "T", "author": "A", "source_url": "http://x.com", "content": "text", "publication_date": "2024-01-01"})

        assert_that(response.json()["job_id"]).is_equal_to("my-job-id")

    def test_should_return_200_when_job_found(self) -> None:
        ingest_uc = Mock(spec=IngestDocumentUseCase)
        get_job_uc = Mock(spec=GetJobUseCase)
        get_job_uc.execute.return_value = _make_complete_job()
        client = _make_client(ingest_uc, get_job_uc)

        response = client.get("/jobs/abc")

        assert_that(response.status_code).is_equal_to(200)

    def test_should_return_404_when_job_not_found(self) -> None:
        ingest_uc = Mock(spec=IngestDocumentUseCase)
        get_job_uc = Mock(spec=GetJobUseCase)
        get_job_uc.execute.side_effect = KeyError("abc")
        client = _make_client(ingest_uc, get_job_uc)

        response = client.get("/jobs/abc")

        assert_that(response.status_code).is_equal_to(404)

    def test_should_return_500_when_ingest_raises_exception(self) -> None:
        ingest_uc = Mock(spec=IngestDocumentUseCase)
        ingest_uc.execute.side_effect = Exception("error")
        get_job_uc = Mock(spec=GetJobUseCase)
        client = _make_client(ingest_uc, get_job_uc)

        response = client.post("/ingest", json={"title": "T", "author": "A", "source_url": "http://x.com", "content": "text", "publication_date": "2024-01-01"})

        assert_that(response.status_code).is_equal_to(500)
