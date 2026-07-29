from __future__ import annotations

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.file_chunk import FileChunk


class FileChunkRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    async def bulk_create(
        self,
        chunks: list[FileChunk],
    ) -> None:
        """
        Bulk insert file chunks.
        """
        if not chunks:
            return

        self.db.add_all(chunks)
        await self.db.commit()

    async def get_by_repository_file(
        self,
        repository_file_id,
    ) -> list[FileChunk]:
        """
        Fetch all chunks belonging to a repository file.
        """
        result = await self.db.execute(
            select(FileChunk)
            .where(
                FileChunk.repository_file_id == repository_file_id
            )
            .order_by(FileChunk.chunk_index)
        )

        return list(result.scalars().all())

    async def delete_by_repository_file(
        self,
        repository_file_id,
    ) -> None:
        """
        Delete all chunks belonging to a repository file.
        """
        await self.db.execute(
            delete(FileChunk).where(
                FileChunk.repository_file_id == repository_file_id
            )
        )

        await self.db.commit()