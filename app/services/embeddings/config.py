# app/services/embeddings/config.py
from dataclasses import dataclass
from pydantic import SecretStr

from app.services.embeddings.models import EmbeddingProviderType


@dataclass(slots=True)
class EmbeddingProviderConfig:
    provider: EmbeddingProviderType
    api_key: SecretStr
    model: str
