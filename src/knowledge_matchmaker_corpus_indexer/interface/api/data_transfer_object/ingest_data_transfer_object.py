from enum import Enum

from pydantic import BaseModel


class JobStatusDTO(str, Enum):
    queued = "queued"
    processing = "processing"
    complete = "complete"
    failed = "failed"


class IngestRequest(BaseModel):
    title: str
    author: str
    source_url: str
    full_text: str
    publication_date: str = ""


class IngestResponse(BaseModel):
    job_id: str
    status: JobStatusDTO


class JobStatusResponse(BaseModel):
    job_id: str
    status: JobStatusDTO
