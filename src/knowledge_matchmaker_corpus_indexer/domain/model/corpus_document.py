from pydantic import BaseModel


class CorpusDocument(BaseModel):
    title: str
    author: str
    source_url: str
    publication_date: str
    content: str
