# app/services/embeddings/provider_factory.py

from app.services.embeddings.base import EmbeddingProvider
from app.services.embeddings.config import EmbeddingProviderConfig
from app.services.embeddings.models import EmbeddingProviderType
from app.services.embeddings.openai_provider import OpenAIEmbeddingProvider
from app.services.embeddings.gemini_provider import GeminiEmbeddingProvider
from app.services.embeddings.voyage_provider import VoyageEmbeddingProvider


class EmbeddingProviderFactory:

    @staticmethod
    def create(
        config: EmbeddingProviderConfig,
    ) -> EmbeddingProvider:

        match config.provider:

            case EmbeddingProviderType.OPENAI:
                return OpenAIEmbeddingProvider(config)

            case EmbeddingProviderType.GEMINI:
                return GeminiEmbeddingProvider(config)

            case EmbeddingProviderType.VOYAGE:
                return VoyageEmbeddingProvider(config)

        raise NotImplementedError(
            f"Embedding provider '{config.provider}' is not supported."
        )
