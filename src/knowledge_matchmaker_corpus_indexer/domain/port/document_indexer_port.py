from abc import ABC, abstractmethod

from knowledge_matchmaker_corpus_indexer.domain.model.corpus_document import CorpusDocument


class DocumentIndexerPort(ABC):
    @abstractmethod
    def index(self, job_id: str, document: CorpusDocument) -> None:
        raise NotImplementedError
