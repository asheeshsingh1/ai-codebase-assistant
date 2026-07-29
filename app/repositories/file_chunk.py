from __future__ import annotations

from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.file_chunk import FileChunk


class FileChunkRepository:
    """
    Repository for FileChunk persistence operations.
    """

    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        self.db = db

    async def bulk_create(
        self,
        chunks: list[FileChunk],
    ) -> None:
        """
        Persist a collection of chunks.
        """
        if not chunks:
            return

        self.db.add_all(chunks)

        await self.db.commit()

    async def delete_by_repository_file_id(
        self,
        repository_file_id: int,
    ) -> None:
        """
        Delete all chunks belonging to a repository file.
        """
        await self.db.execute(
            delete(FileChunk).where(FileChunk.repository_file_id == repository_file_id)
        )

        await self.db.commit()

    async def get_by_repository_file(
        self,
        repository_file_id: int,
    ) -> list[FileChunk]:
        """
        Retrieve all chunks for a repository file.
        """
        result = await self.db.execute(
            select(FileChunk)
            .where(FileChunk.repository_file_id == repository_file_id)
            .order_by(FileChunk.chunk_index)
        )

        return list(result.scalars().all())

    async def get_by_symbol(
        self,
        symbol_name: str,
    ) -> list[FileChunk]:
        """
        Retrieve chunks by symbol name.
        """
        result = await self.db.execute(
            select(FileChunk)
            .where(FileChunk.symbol_name == symbol_name)
            .order_by(FileChunk.chunk_index)
        )

        return list(result.scalars().all())

    async def get_by_chunk_type(
        self,
        chunk_type: str,
    ) -> list[FileChunk]:
        """
        Retrieve chunks by semantic type.
        """
        result = await self.db.execute(
            select(FileChunk)
            .where(FileChunk.chunk_type == chunk_type)
            .order_by(
                FileChunk.repository_file_id,
                FileChunk.chunk_index,
            )
        )

        return list(result.scalars().all())
