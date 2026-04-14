import openai

from knowledge_matchmaker_corpus_indexer.domain.service.embedder import Embedder


class OpenAIEmbedder(Embedder):
    def __init__(self, model: str = "text-embedding-3-small") -> None:
        self._client = openai.OpenAI()
        self._model = model

    def embed(self, text: str) -> list[float]:
        response = self._client.embeddings.create(
            input=text,
            model=self._model,
        )
        return response.data[0].embedding
