from __future__ import annotations

from pathlib import Path
from uuid import UUID

from app.repositories.repository import RepositoryRepository
from app.repositories.repository_file import RepositoryFileRepository
from app.schemas.repository_file import (
    RepositoryFileContentResponse,
    RepositoryFileResponse,
)
from app.services.repository.exceptions import (
    RepositoryNotFoundError,
)
from app.services.repository_file.exceptions import (
    RepositoryFileNotFoundError,
)


class RepositoryFileService:
    """
    Handles repository file operations.
    """

    def __init__(
        self,
        repository_repository: RepositoryRepository,
        repository_file_repository: RepositoryFileRepository,
    ) -> None:
        self.repository_repository = repository_repository
        self.repository_file_repository = repository_file_repository

    async def list_files(
        self,
        repository_id: UUID,
    ) -> list[RepositoryFileResponse]:

        repository = await self.repository_repository.get_by_id(
            repository_id,
        )

        if repository is None:
            raise RepositoryNotFoundError("Repository not found.")

        files = await self.repository_file_repository.get_by_repository_id(
            repository_id,
        )

        return [RepositoryFileResponse.model_validate(file) for file in files]

    async def get_file_content(
        self,
        repository_file_id: UUID,
    ) -> RepositoryFileContentResponse:

        repository_file = await self.repository_file_repository.get_by_id(
            repository_file_id,
        )

        if repository_file is None:
            raise RepositoryFileNotFoundError("Repository file not found.")

        repository = await self.repository_repository.get_by_id(
            repository_file.repository_id,
        )

        if repository is None:
            raise RepositoryNotFoundError("Repository not found.")

        full_path = Path(repository.local_path) / repository_file.relative_path

        if not full_path.exists():
            raise FileNotFoundError(f"{full_path} does not exist.")

        content = full_path.read_text(
            encoding="utf-8",
            errors="replace",
        )

        return RepositoryFileContentResponse(
            id=repository_file.id,
            relative_path=repository_file.relative_path,
            language=repository_file.language,
            extension=repository_file.extension,
            content=content,
        )
