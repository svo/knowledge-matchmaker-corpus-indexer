import chromadb

from knowledge_matchmaker_corpus_indexer.domain.model.corpus_document import CorpusDocument
from knowledge_matchmaker_corpus_indexer.domain.port.document_indexer_port import DocumentIndexerPort


class ChromaDocumentIndexer(DocumentIndexerPort):
    def __init__(self, client: chromadb.ClientAPI, collection_name: str = "corpus") -> None:
        self._collection = client.get_or_create_collection(collection_name)

    def index(self, job_id: str, document: CorpusDocument) -> None:
        self._collection.add(
            ids=[job_id],
            documents=[document.full_text],
            metadatas=[
                {
                    "title": document.title,
                    "author": document.author,
                    "source_url": document.source_url,
                    "publication_date": document.publication_date,
                }
            ],
        )
