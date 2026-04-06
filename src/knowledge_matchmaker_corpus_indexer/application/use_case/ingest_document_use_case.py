import uuid

from knowledge_matchmaker_corpus_indexer.domain.model.corpus_document import CorpusDocument
from knowledge_matchmaker_corpus_indexer.domain.model.ingestion_job import IngestionJob, IngestionStatus
from knowledge_matchmaker_corpus_indexer.domain.service.corpus_indexer import CorpusIndexer


class IngestDocumentUseCase:
    def __init__(self, corpus_indexer: CorpusIndexer) -> None:
        self._corpus_indexer = corpus_indexer

    def execute(self, document: CorpusDocument) -> IngestionJob:
        job_id = str(uuid.uuid4())
        job = IngestionJob(job_id=job_id, document_title=document.title, status=IngestionStatus.PROCESSING)
        self._corpus_indexer.index(document, job_id)
        return IngestionJob(job_id=job_id, document_title=document.title, status=IngestionStatus.COMPLETED)


class GetIngestionJobUseCase:
    def __init__(self, corpus_indexer: CorpusIndexer) -> None:
        self._corpus_indexer = corpus_indexer

    def execute(self, job_id: str) -> IngestionJob:
        return self._corpus_indexer.get_job_status(job_id)
