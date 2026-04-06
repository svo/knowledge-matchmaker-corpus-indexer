from knowledge_matchmaker_corpus_indexer.domain.model.corpus_document import CorpusDocument
from knowledge_matchmaker_corpus_indexer.domain.port.document_indexer_port import DocumentIndexerPort


class InMemoryDocumentIndexer(DocumentIndexerPort):
    def __init__(self) -> None:
        self._indexed: list[tuple[str, CorpusDocument]] = []

    def index(self, job_id: str, document: CorpusDocument) -> None:
        self._indexed.append((job_id, document))

    @property
    def indexed(self) -> list[tuple[str, CorpusDocument]]:
        return self._indexed
