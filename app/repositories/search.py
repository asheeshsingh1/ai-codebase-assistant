from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.db.models.chunk_embedding import ChunkEmbedding
from app.db.models.file_chunk import FileChunk
from app.db.models.repository_file import RepositoryFile
from app.services.search.models import SearchResult


class SearchRepository:
    """
    Repository responsible for semantic search queries.

    Performs vector similarity search across repository chunks using pgvector.
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
        *,
        provider: str | None = None,
        model: str | None = None,
        limit: int = 10,
        min_similarity: float | None = 0.3,
    ) -> list[SearchResult]:
        """
        Return the most semantically similar chunks for a repository.

        Args:
            repository_id: Repository to search.
            embedding: Query embedding.
            provider: Optional embedding provider filter.
            model: Optional embedding model filter.
            limit: Maximum number of results.
            min_similarity: Optional minimum similarity threshold.
        """

        similarity = (1 - ChunkEmbedding.embedding.cosine_distance(embedding)).label(
            "similarity"
        )

        stmt = (
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
        )

        if provider is not None:
            stmt = stmt.where(
                ChunkEmbedding.provider == provider,
            )

        if model is not None:
            stmt = stmt.where(
                ChunkEmbedding.model == model,
            )

        if min_similarity is not None:
            stmt = stmt.where(
                similarity >= min_similarity,
            )

        stmt = stmt.order_by(
            similarity.desc(),
        ).limit(limit)

        result = await self.db.execute(stmt)
        rows = result.all()

        print("ROWS:", rows)
        print("ROW COUNT:", len(rows))

        return [
            SearchResult(
                chunk=chunk,
                similarity=float(similarity_score),
            )
            for chunk, similarity_score in rows
        ]

        # return [
        #     SearchResult(
        #         chunk=chunk,
        #         similarity=float(similarity_score),
        #     )
        #     for chunk, similarity_score in result.all()
        # ]
