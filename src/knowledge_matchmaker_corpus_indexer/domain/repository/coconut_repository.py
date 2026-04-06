import uuid

from abc import ABC, abstractmethod

from knowledge_matchmaker_corpus_indexer.domain.model.coconut import Coconut


class CoconutQueryRepository(ABC):
    @abstractmethod
    def read(self, id: uuid.UUID) -> Coconut:
        raise NotImplementedError()


class CoconutCommandRepository(ABC):
    @abstractmethod
    def create(self, id: Coconut) -> uuid.UUID:
        raise NotImplementedError()
