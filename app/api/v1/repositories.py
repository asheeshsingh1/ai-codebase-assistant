from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.repository import RepositoryRepository
from app.schemas.repository import RepositoryCreate
from app.schemas.repository import RepositoryResponse
from app.services.repository_service import RepositoryService
from app.repositories.repository_file import RepositoryFileRepository
from app.services.git_service import GitService

router = APIRouter(prefix="/repositories", tags=["Repositories"])


@router.post(
    "",
    response_model=RepositoryResponse,
    status_code=201,
)
async def create_repository(
    payload: RepositoryCreate,
    db: AsyncSession = Depends(get_db),
):

    service = RepositoryService(
        repository_repo=RepositoryRepository(db),
        repository_file_repo=RepositoryFileRepository(db),
        git_service=GitService(),
    )

    try:
        return await service.create_repository(payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        )