from enum import Enum
from typing import Optional

from pydantic import BaseModel


class IngestionStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETE = "complete"
    FAILED = "failed"


class IngestionJob(BaseModel):
    job_id: str
    document_title: str
    status: IngestionStatus
    error_message: Optional[str] = None
