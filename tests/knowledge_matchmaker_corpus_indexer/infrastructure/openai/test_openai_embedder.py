from unittest.mock import Mock, patch

from assertpy import assert_that

from knowledge_matchmaker_corpus_indexer.infrastructure.openai.openai_embedder import OpenAIEmbedder


class TestOpenAIEmbedder:
    @patch("knowledge_matchmaker_corpus_indexer.infrastructure.openai.openai_embedder.openai")
    def test_should_return_embedding_vector_when_embed_is_called(self, mock_openai_module) -> None:
        mock_embedding = Mock()
        mock_embedding.embedding = [0.1, 0.2, 0.3]
        mock_response = Mock()
        mock_response.data = [mock_embedding]
        mock_openai_module.OpenAI.return_value.embeddings.create.return_value = mock_response
        embedder = OpenAIEmbedder()

        result = embedder.embed("test text")

        assert_that(result).is_equal_to([0.1, 0.2, 0.3])

    @patch("knowledge_matchmaker_corpus_indexer.infrastructure.openai.openai_embedder.openai")
    def test_should_call_openai_with_provided_text_when_embed_is_called(self, mock_openai_module) -> None:
        mock_embedding = Mock()
        mock_embedding.embedding = [0.1]
        mock_response = Mock()
        mock_response.data = [mock_embedding]
        mock_client = mock_openai_module.OpenAI.return_value
        mock_client.embeddings.create.return_value = mock_response
        embedder = OpenAIEmbedder()

        embedder.embed("my document text")

        assert_that(mock_client.embeddings.create.call_args.kwargs["input"]).is_equal_to("my document text")

    @patch("knowledge_matchmaker_corpus_indexer.infrastructure.openai.openai_embedder.openai")
    def test_should_use_configured_model_when_embed_is_called(self, mock_openai_module) -> None:
        mock_embedding = Mock()
        mock_embedding.embedding = [0.1]
        mock_response = Mock()
        mock_response.data = [mock_embedding]
        mock_client = mock_openai_module.OpenAI.return_value
        mock_client.embeddings.create.return_value = mock_response
        embedder = OpenAIEmbedder(model="text-embedding-3-large")

        embedder.embed("text")

        assert_that(mock_client.embeddings.create.call_args.kwargs["model"]).is_equal_to("text-embedding-3-large")
