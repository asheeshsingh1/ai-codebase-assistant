# app/services/embedding_service.py
from collections.abc import Iterable
from itertools import islice

from app.repositories.chunk_embedding_repository import ChunkEmbeddingRepository
from app.services.embeddings.base import EmbeddingProvider


class EmbeddingService:

    def __init__(
        self,
        provider: EmbeddingProvider,
        chunk_embedding_repository: ChunkEmbeddingRepository,
        batch_size: int = 100,
    ):
        self.provider = provider
        self.chunk_embedding_repository = chunk_embedding_repository
        self.batch_size = batch_size

    def _batched(
        iterable: Iterable,
        size: int,
    ):
        iterator = iter(iterable)

        while batch := list(islice(iterator, size)):
            yield batch

    async def embed_query(
        self,
        query: str,
    ) -> list[float]:
        return await self.provider.embed_one(query)
