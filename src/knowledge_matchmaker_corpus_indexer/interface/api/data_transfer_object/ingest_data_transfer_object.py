from pydantic import BaseModel


class IngestRequest(BaseModel):
    title: str
    author: str
    source_url: str
    content: str
    publication_date: str = ""


class IngestResponse(BaseModel):
    job_id: str
    status: str


class JobStatusResponse(BaseModel):
    job_id: str
    status: str
