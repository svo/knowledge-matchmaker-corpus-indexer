import uuid

from knowledge_matchmaker_corpus_indexer.domain.model.corpus_document import CorpusDocument
from knowledge_matchmaker_corpus_indexer.domain.model.ingestion_job import IngestionJob, JobStatus
from knowledge_matchmaker_corpus_indexer.domain.port.document_indexer_port import DocumentIndexerPort
from knowledge_matchmaker_corpus_indexer.domain.port.job_repository_port import JobRepositoryPort


class IngestDocumentUseCase:
    def __init__(self, indexer: DocumentIndexerPort, job_repository: JobRepositoryPort) -> None:
        self._indexer = indexer
        self._job_repository = job_repository

    def execute(self, document: CorpusDocument) -> IngestionJob:
        job_id = str(uuid.uuid4())
        job = IngestionJob(job_id=job_id, status=JobStatus.queued, document=document)
        self._job_repository.save(job)
        processing_job = IngestionJob(job_id=job_id, status=JobStatus.processing, document=document)
        self._job_repository.save(processing_job)
        self._indexer.index(job_id, document)
        complete_job = IngestionJob(job_id=job_id, status=JobStatus.complete, document=document)
        self._job_repository.save(complete_job)
        return complete_job
