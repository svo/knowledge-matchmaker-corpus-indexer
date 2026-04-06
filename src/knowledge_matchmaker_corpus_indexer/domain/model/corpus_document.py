from pydantic import BaseModel


class CorpusDocument(BaseModel):
    title: str
    author: str
    source_url: str
    full_text: str
    publication_date: str = ""
