from __future__ import annotations

from uuid import UUID

from app.db.models.chat_message import ChatMessage
from app.repositories.chat_repository import ChatRepository


class ChatHistoryService:

    def __init__(
        self,
        chat_repository: ChatRepository,
    ) -> None:
        self.chat_repository = chat_repository

    async def save_user_message(
        self,
        repository_id: UUID,
        content: str,
    ) -> ChatMessage:

        message = ChatMessage(
            repository_id=repository_id,
            role="user",
            content=content,
        )

        return await self.chat_repository.create(message)

    async def save_assistant_message(
        self,
        repository_id: UUID,
        content: str,
        citations: list | None = None,
    ) -> ChatMessage:

        message = ChatMessage(
            repository_id=repository_id,
            role="assistant",
            content=content,
            citations=citations,
        )

        return await self.chat_repository.create(message)

    async def get_messages(
        self,
        repository_id: UUID,
    ) -> list[ChatMessage]:

        return await self.chat_repository.list_by_repository(
            repository_id,
        )
