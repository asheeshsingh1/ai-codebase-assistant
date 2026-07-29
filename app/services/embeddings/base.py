# app/services/embeddings/base.py
from abc import ABC, abstractmethod

from app.services.embeddings.config import EmbeddingProviderConfig


class EmbeddingProvider(ABC):

    def __init__(
        self,
        config: EmbeddingProviderConfig,
    ):
        self.config = config

    @property
    def provider(self):
        return self.config.provider

    @property
    def model(self):
        return self.config.model

    @property
    @abstractmethod
    def dimensions(self) -> int: ...

    @abstractmethod
    async def embed(
        self,
        texts: list[str],
    ) -> list[list[float]]: ...

    async def embed_one(
        self,
        text: str,
    ) -> list[float]:
        return (await self.embed([text]))[0]
