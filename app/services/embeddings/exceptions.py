# app/services/embeddings/exceptions.py
class EmbeddingProviderError(Exception):
    """Base exception for embedding providers."""


class EmbeddingProviderConfigurationError(EmbeddingProviderError):
    """Raised when provider configuration is invalid."""


class EmbeddingGenerationError(EmbeddingProviderError):
    """Raised when embedding generation fails."""
