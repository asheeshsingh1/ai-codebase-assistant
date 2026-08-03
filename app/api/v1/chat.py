from __future__ import annotations

from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.container import AppContainer
from app.db.session import get_db

from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    CitationResponse,
)

from app.services.chat.exceptions import (
    ChatError,
    RepositoryNotIndexedError,
)

router = APIRouter(
    prefix="/repositories",
    tags=["Chat"],
)


@router.post(
    "/{repository_id}/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
)
async def chat(
    repository_id: UUID,
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
) -> ChatResponse:
    """
    Ask a natural language question about a repository.
    """

    container = AppContainer(db)
    try:

        result = await container.chat_service.ask(
            repository_id=repository_id,
            question=request.question,
        )

        return ChatResponse(
            answer=result.answer,
            citations=[
                CitationResponse(
                    file_path=citation.file_path,
                    start_line=citation.start_line,
                    end_line=citation.end_line,
                )
                for citation in result.citations
            ],
        )

    except RepositoryNotIndexedError as exc:
        print("1", exc)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    except ChatError as exc:
        print("2", exc)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        print("3", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to answer repository question.",
        ) from exc
