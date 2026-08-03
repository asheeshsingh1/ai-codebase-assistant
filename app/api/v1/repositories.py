from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.container import AppContainer
from app.db.session import get_db
from app.schemas.repository import (
    RepositoryCreate,
    RepositoryResponse,
)
from app.services.repository.exceptions import (
    RepositoryAlreadyExistsError,
    RepositoryNotFoundError,
)

router = APIRouter(
    prefix="/repositories",
    tags=["Repositories"],
)


@router.get(
    "",
    response_model=list[RepositoryResponse],
)
async def list_repositories(
    db: AsyncSession = Depends(get_db),
):
    container = AppContainer(db)
    service = container.repository_service

    return await service.list_repositories()


@router.post(
    "",
    response_model=RepositoryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_repository(
    payload: RepositoryCreate,
    db: AsyncSession = Depends(get_db),
):
    container = AppContainer(db)

    try:
        return await container.repository_service.create_repository(
            payload,
        )

    except RepositoryAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{repository_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_repository(
    repository_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    container = AppContainer(db)

    try:
        await container.repository_service.delete_repository(
            repository_id,
        )

    except RepositoryNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
