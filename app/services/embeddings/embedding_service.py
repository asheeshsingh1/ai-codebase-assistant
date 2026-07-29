from __future__ import annotations

from itertools import islice

from app.db.models.chunk_embedding import ChunkEmbedding
from app.db.models.file_chunk import FileChunk
from app.repositories.chunk_embedding_repository import ChunkEmbeddingRepository
from app.services.embeddings.base import EmbeddingProvider


class EmbeddingService:
    """
    Service responsible for generating and storing embeddings
    for repository file chunks.
    """

    def __init__(
        self,
        provider: EmbeddingProvider,
        chunk_embedding_repo: ChunkEmbeddingRepository,
        batch_size: int = 100,
    ) -> None:
        self.provider = provider
        self.chunk_embedding_repo = chunk_embedding_repo
        self.batch_size = batch_size

    async def embed_chunks(
        self,
        chunks: list[FileChunk],
    ) -> None:
        """
        Generate embeddings for all supplied chunks and persist them.
        """

        if not chunks:
            return

        for batch in self._batched(chunks):

            texts = [chunk.content for chunk in batch]

            vectors = await self.provider.embed(texts)

            db_embeddings = [
                ChunkEmbedding(
                    chunk_id=chunk.id,
                    provider=self.provider.provider_name.value,
                    model=self.provider.model_name,
                    dimensions=self.provider.dimensions,
                    embedding=vector,
                )
                for chunk, vector in zip(batch, vectors)
            ]

            await self.chunk_embedding_repo.bulk_create(
                db_embeddings,
            )

    async def embed_query(
        self,
        query: str,
    ) -> list[float]:
        """
        Generate an embedding for a user query.
        """

        return await self.provider.embed_one(query)

    def _batched(
        self,
        chunks: list[FileChunk],
    ):
        iterator = iter(chunks)

        while batch := list(islice(iterator, self.batch_size)):
            yield batch
