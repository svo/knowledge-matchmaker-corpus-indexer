from fastapi import APIRouter, HTTPException, status

from knowledge_matchmaker_corpus_indexer.application.use_case.ingest_document_use_case import (
    GetIngestionJobUseCase,
    IngestDocumentUseCase,
)
from knowledge_matchmaker_corpus_indexer.domain.model.corpus_document import CorpusDocument
from knowledge_matchmaker_corpus_indexer.interface.api.data_transfer_object.ingest_document_data_transfer_object import (
    IngestionJobResponseDto,
    IngestDocumentRequestDto,
)


class IngestDocumentController:
    def __init__(
        self,
        ingest_document_use_case: IngestDocumentUseCase,
        get_ingestion_job_use_case: GetIngestionJobUseCase,
    ) -> None:
        self._ingest_document_use_case = ingest_document_use_case
        self._get_ingestion_job_use_case = get_ingestion_job_use_case
        self.router = APIRouter(tags=["ingest"])
        self._register_routes()

    def _register_routes(self) -> None:
        self.router.add_api_route(
            "/ingest",
            self.ingest_document,
            methods=["POST"],
            response_model=IngestionJobResponseDto,
            status_code=status.HTTP_201_CREATED,
        )
        self.router.add_api_route(
            "/jobs/{job_id}",
            self.get_job,
            methods=["GET"],
            response_model=IngestionJobResponseDto,
        )

    async def ingest_document(self, request: IngestDocumentRequestDto) -> IngestionJobResponseDto:
        document = CorpusDocument(
            title=request.title,
            author=request.author,
            source_url=request.source_url,
            publication_date=request.publication_date,
            full_text=request.full_text,
        )
        job = self._ingest_document_use_case.execute(document)
        return IngestionJobResponseDto.from_domain_model(job)

    async def get_job(self, job_id: str) -> IngestionJobResponseDto:
        try:
            job = self._get_ingestion_job_use_case.execute(job_id)
            return IngestionJobResponseDto.from_domain_model(job)
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Job with id {job_id} not found",
            )


def create_ingest_document_controller(
    ingest_document_use_case: IngestDocumentUseCase,
    get_ingestion_job_use_case: GetIngestionJobUseCase,
) -> IngestDocumentController:
    return IngestDocumentController(
        ingest_document_use_case=ingest_document_use_case,
        get_ingestion_job_use_case=get_ingestion_job_use_case,
    )
