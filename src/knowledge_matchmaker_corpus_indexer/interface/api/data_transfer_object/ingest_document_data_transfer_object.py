from typing import Any, Optional

from pydantic import BaseModel


class IngestDocumentRequestDto(BaseModel):
    title: str
    author: str
    source_url: str
    publication_date: str
    full_text: str

    @classmethod
    def from_domain_model(cls, domain_model: Any) -> "IngestDocumentRequestDto":
        return cls(
            title=domain_model.title,
            author=domain_model.author,
            source_url=domain_model.source_url,
            publication_date=domain_model.publication_date,
            full_text=domain_model.full_text,
        )


class IngestionJobResponseDto(BaseModel):
    job_id: str
    document_title: str
    status: str
    error_message: Optional[str] = None

    @classmethod
    def from_domain_model(cls, domain_model: Any) -> "IngestionJobResponseDto":
        return cls(
            job_id=domain_model.job_id,
            document_title=domain_model.document_title,
            status=domain_model.status.value,
            error_message=domain_model.error_message,
        )
