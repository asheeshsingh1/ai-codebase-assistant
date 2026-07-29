from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.container import AppContainer
from app.db.session import get_db
from app.schemas.repository import RepositoryCreate
from app.schemas.repository import RepositoryResponse

router = APIRouter(
    prefix="/repositories",
    tags=["Repositories"],
)


@router.post(
    "",
    response_model=RepositoryResponse,
    status_code=201,
)
async def create_repository(
    payload: RepositoryCreate,
    db: AsyncSession = Depends(get_db),
):
    container = AppContainer(db)
    service = container.repository_service

    try:
        return await service.create_repository(payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        )
