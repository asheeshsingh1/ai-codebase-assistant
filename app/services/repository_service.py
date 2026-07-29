from pathlib import Path
from urllib.parse import urlparse
import traceback

from app.core.config import settings
from app.db.models.repository import Repository, RepositoryStatus
from app.repositories.repository import RepositoryRepository
from app.schemas.repository import RepositoryCreate
from app.services.chunking.chunk_service import ChunkService
from app.services.git_service import GitService
from app.services.file_indexer_service import FileIndexerService

class RepositoryService:

    def __init__(
        self,
        repository_repo: RepositoryRepository,
        git_service: GitService,
        file_indexer: FileIndexerService,
        chunk_service: ChunkService,
    ) -> None:
        self.repository_repo = repository_repo
        self.git_service = git_service
        self.file_indexer = file_indexer
        self.chunk_service = chunk_service

    async def create_repository(
        self,
        payload: RepositoryCreate,
    ) -> Repository:

        existing = await self.repository_repo.get_by_git_url(
            str(payload.git_url)
        )

        if existing:
            raise ValueError("Repository already exists")

        repo_name = self._extract_repo_name(str(payload.git_url))

        repository = Repository(
            name=repo_name,
            git_url=str(payload.git_url),
        )


        repository = await self.repository_repo.create(repository)

        repository.status = RepositoryStatus.CLONING
        await self.repository_repo.update(repository)

        storage_path = (
            Path(settings.repository_storage_path)
            / str(repository.id)
        )

        try:
            self.git_service.clone(
                repository.git_url,
                storage_path,
            )

            repository.local_path = str(storage_path)
            await self.repository_repo.update(repository)
            await self.file_indexer.index_repository(
                repository,
            )
            await self.chunk_service.chunk_repository(
                repository
            )
            repository.status = RepositoryStatus.READY

        except Exception as e:
            traceback.print_exc()

            await self.repository_repo.db.rollback()

            repository.status = RepositoryStatus.FAILED

            try:
                await self.repository_repo.update(repository)
            except Exception:
                pass

            raise

        finally:
            await self.repository_repo.update(repository)

        return repository

    @staticmethod
    def _extract_repo_name(url: str) -> str:
        path = urlparse(url).path
        return path.rstrip("/").split("/")[-1].removesuffix(".git")