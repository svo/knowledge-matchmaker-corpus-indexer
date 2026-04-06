from fastapi import APIRouter, HTTPException

from knowledge_matchmaker_corpus_indexer.application.use_case.get_job_use_case import GetJobUseCase
from knowledge_matchmaker_corpus_indexer.application.use_case.ingest_document_use_case import IngestDocumentUseCase
from knowledge_matchmaker_corpus_indexer.domain.model.corpus_document import CorpusDocument
from knowledge_matchmaker_corpus_indexer.interface.api.data_transfer_object.ingest_data_transfer_object import (
    IngestRequest,
    IngestResponse,
    JobStatusDTO,
    JobStatusResponse,
)


def create_ingest_controller(ingest_use_case: IngestDocumentUseCase, get_job_use_case: GetJobUseCase) -> APIRouter:
    router = APIRouter()

    @router.post("/ingest", response_model=IngestResponse, status_code=202)
    async def ingest(request: IngestRequest) -> IngestResponse:
        try:
            document = CorpusDocument(
                title=request.title,
                author=request.author,
                source_url=request.source_url,
                full_text=request.full_text,
                publication_date=request.publication_date,
            )
            job = ingest_use_case.execute(document)
            return IngestResponse(job_id=job.job_id, status=JobStatusDTO(job.status.value))
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @router.get("/jobs/{job_id}", response_model=JobStatusResponse)
    async def get_job(job_id: str) -> JobStatusResponse:
        try:
            job = get_job_use_case.execute(job_id)
            return JobStatusResponse(job_id=job.job_id, status=JobStatusDTO(job.status.value))
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=f"Job {job_id} not found") from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    return router
