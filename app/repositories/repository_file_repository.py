from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.repository_file import RepositoryFile


class RepositoryFileRepository:
    """
    Repository for RepositoryFile database operations.
    """

    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        self.db = db

    async def get_by_repository_id(
        self,
        repository_file_id: UUID,
    ) -> RepositoryFile | None:
        """
        Retrieve a repository file by its ID.
        """

        result = await self.db.execute(
            select(RepositoryFile).where(
                RepositoryFile.id == repository_file_id,
            )
        )

        return result.scalar_one_or_none()

    async def list_by_repository(
        self,
        repository_id: UUID,
    ) -> list[RepositoryFile]:
        """
        List all files belonging to a repository.
        """

        result = await self.db.execute(
            select(RepositoryFile)
            .where(
                RepositoryFile.repository_id == repository_id,
            )
            .order_by(
                RepositoryFile.relative_path,
            )
        )

        return list(result.scalars().all())
