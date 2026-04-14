from unittest.mock import Mock

import pytest
from assertpy import assert_that
from fastapi import FastAPI
from fastapi.testclient import TestClient

from knowledge_matchmaker_corpus_indexer.application.use_case.ingest_document_use_case import (
    GetIngestionJobUseCase,
    IngestDocumentUseCase,
)
from knowledge_matchmaker_corpus_indexer.domain.model.ingestion_job import IngestionJob, IngestionStatus
from knowledge_matchmaker_corpus_indexer.interface.api.controller.ingest_document_controller import (
    IngestDocumentController,
)


class TestIngestDocumentController:
    @pytest.fixture
    def mock_ingest_use_case(self) -> Mock:
        return Mock(spec=IngestDocumentUseCase)

    @pytest.fixture
    def mock_get_job_use_case(self) -> Mock:
        return Mock(spec=GetIngestionJobUseCase)

    @pytest.fixture
    def controller(self, mock_ingest_use_case, mock_get_job_use_case) -> IngestDocumentController:
        return IngestDocumentController(
            ingest_document_use_case=mock_ingest_use_case,
            get_ingestion_job_use_case=mock_get_job_use_case,
        )

    @pytest.fixture
    def app(self, controller) -> FastAPI:
        app = FastAPI()
        app.include_router(controller.router)
        return app

    @pytest.fixture
    def client(self, app) -> TestClient:
        return TestClient(app)

    @pytest.fixture
    def sample_request_body(self):
        return {
            "title": "Test Document",
            "author": "Test Author",
            "source_url": "https://example.com",
            "publication_date": "2024-01-01",
            "full_text": "Test content",
        }

    @pytest.fixture
    def sample_job(self):
        return IngestionJob(
            job_id="test-job-id-123",
            document_title="Test Document",
            status=IngestionStatus.COMPLETE,
        )

    def test_should_return_201_when_ingest_is_called(
        self, client, mock_ingest_use_case, sample_request_body, sample_job
    ):
        mock_ingest_use_case.execute.return_value = sample_job

        response = client.post("/ingest", json=sample_request_body)

        assert_that(response.status_code).is_equal_to(201)

    def test_should_return_job_id_in_response(self, client, mock_ingest_use_case, sample_request_body, sample_job):
        mock_ingest_use_case.execute.return_value = sample_job

        response = client.post("/ingest", json=sample_request_body)

        assert_that(response.json()["job_id"]).is_equal_to("test-job-id-123")

    def test_should_return_200_when_getting_job_status(self, client, mock_get_job_use_case, sample_job):
        mock_get_job_use_case.execute.return_value = sample_job

        response = client.get("/jobs/test-job-id-123")

        assert_that(response.status_code).is_equal_to(200)

    def test_should_return_404_when_job_not_found(self, client, mock_get_job_use_case):
        mock_get_job_use_case.execute.side_effect = KeyError("not found")

        response = client.get("/jobs/nonexistent-job-id")

        assert_that(response.status_code).is_equal_to(404)
