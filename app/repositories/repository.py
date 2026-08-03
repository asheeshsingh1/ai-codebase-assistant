from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.repository import Repository


class RepositoryRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list(self):
        stmt = select(Repository).order_by(Repository.created_at.desc())

        result = await self.db.execute(stmt)

        return result.scalars().all()

    async def create(self, repository: Repository) -> Repository:
        self.db.add(repository)
        await self.db.commit()
        await self.db.refresh(repository)
        return repository

    async def get_by_git_url(self, git_url: str) -> Repository | None:
        result = await self.db.execute(
            select(Repository).where(Repository.git_url == git_url)
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, repository_id):
        result = await self.db.execute(
            select(Repository).where(Repository.id == repository_id)
        )
        return result.scalar_one_or_none()

    async def update(self, repository: Repository) -> Repository:
        await self.db.commit()
        await self.db.refresh(repository)
        return repository
