# app/repositories/chunk_embedding_repository.py
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.chunk_embedding import ChunkEmbedding


class ChunkEmbeddingRepository:

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def bulk_create(
        self,
        embeddings: list[ChunkEmbedding],
    ) -> None:

        if not embeddings:
            return

        self.session.add_all(embeddings)
        await self.session.flush()

    async def get_by_chunk_ids(
        self,
        chunk_ids: list[UUID],
    ) -> list[ChunkEmbedding]:

        if not chunk_ids:
            return []

        result = await self.session.execute(
            select(ChunkEmbedding).where(ChunkEmbedding.chunk_id.in_(chunk_ids))
        )

        return list(result.scalars().all())
