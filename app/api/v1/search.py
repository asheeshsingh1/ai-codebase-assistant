from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.container import AppContainer
from app.db.session import get_db

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/{repository_id}")
async def search(
    repository_id: str,
    query: str,
    db: AsyncSession = Depends(get_db),
):
    container = AppContainer(db)

    results = await container.retrieval_service.retrieve(
        repository_id=repository_id,
        query=query,
        limit=5,
    )
    return results
