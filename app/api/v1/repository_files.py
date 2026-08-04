from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.container import AppContainer
from app.db.session import get_db
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

router = APIRouter(tags=["Repository Files"], prefix="/repository-files")


@router.get(
    "/{repository_id}/files",
    response_model=list[RepositoryFileResponse],
)
async def list_repository_files(
    repository_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    container = AppContainer(db)

    try:
        return await container.repository_file_service.list_files(
            repository_id,
        )

    except RepositoryNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/{repository_file_id}",
    response_model=RepositoryFileContentResponse,
)
async def get_repository_file(
    repository_file_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    container = AppContainer(db)

    try:
        return await container.repository_file_service.get_file_content(
            repository_file_id,
        )

    except RepositoryFileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except RepositoryNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
