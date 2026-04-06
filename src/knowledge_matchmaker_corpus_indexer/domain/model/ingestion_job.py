from enum import Enum

from pydantic import BaseModel

from knowledge_matchmaker_corpus_indexer.domain.model.corpus_document import CorpusDocument


class JobStatus(str, Enum):
    queued = "queued"
    processing = "processing"
    complete = "complete"
    failed = "failed"


class IngestionJob(BaseModel):
    job_id: str
    status: JobStatus
    document: CorpusDocument
