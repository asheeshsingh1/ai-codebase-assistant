from collections.abc import Sequence

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.repository_file import RepositoryFile


class RepositoryFileRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def bulk_create(
        self,
        files: list[RepositoryFile],
    ) -> None:
        self.db.add_all(files)
        await self.db.commit()

    async def get_by_repository_id(
        self,
        repository_id: int,
    ) -> Sequence[RepositoryFile]:
        result = await self.db.execute(
            select(RepositoryFile).where(RepositoryFile.repository_id == repository_id)
        )
        return result.scalars().all()

    async def delete_by_repository_id(
        self,
        repository_id,
    ) -> None:
        await self.db.execute(
            delete(RepositoryFile).where(RepositoryFile.repository_id == repository_id)
        )
        await self.db.commit()
