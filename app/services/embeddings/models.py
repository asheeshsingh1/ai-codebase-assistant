# app/services/embeddings/models.py
from enum import StrEnum


class EmbeddingProviderType(StrEnum):
    OPENAI = "openai"
    GEMINI = "gemini"
    VOYAGE = "voyage"
    OPENROUTER = "openrouter"
