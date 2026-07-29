from __future__ import annotations

from uuid import UUID

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.db.models.chunk_embedding import ChunkEmbedding
from app.db.models.file_chunk import FileChunk
from app.db.models.repository_file import RepositoryFile
from app.services.search.models import SearchResult


class SearchRepository:
    """
    Repository responsible for semantic search queries.

    Unlike entity repositories, this repository performs read queries
    spanning multiple tables.
    """

    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        self.db = db

    async def similarity_search(
        self,
        repository_id: UUID,
        embedding: list[float],
        limit: int = 10,
    ) -> list[SearchResult]:
        """
        Return the most similar chunks within a repository.

        Results are ordered by cosine similarity.
        """

        similarity = (1 - ChunkEmbedding.embedding.cosine_distance(embedding)).label(
            "similarity"
        )

        stmt: Select = (
            select(
                FileChunk,
                similarity,
            )
            .join(
                ChunkEmbedding,
                ChunkEmbedding.chunk_id == FileChunk.id,
            )
            .join(
                RepositoryFile,
                RepositoryFile.id == FileChunk.repository_file_id,
            )
            .where(
                RepositoryFile.repository_id == repository_id,
            )
            .options(
                joinedload(FileChunk.repository_file),
            )
            .order_by(similarity.desc())
            .limit(limit)
        )

        result = await self.db.execute(stmt)

        return [
            SearchResult(
                chunk=chunk,
                similarity=float(similarity),
            )
            for chunk, similarity in result.all()
        ]
