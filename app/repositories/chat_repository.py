from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.chat_message import ChatMessage


class ChatRepository:

    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        self.db = db

    async def create(
        self,
        message: ChatMessage,
    ) -> ChatMessage:
        self.db.add(message)

        await self.db.commit()
        await self.db.refresh(message)

        return message

    async def list_by_repository(
        self,
        repository_id: UUID,
    ) -> list[ChatMessage]:

        stmt = (
            select(ChatMessage)
            .where(
                ChatMessage.repository_id == repository_id,
            )
            .order_by(
                ChatMessage.created_at.asc(),
            )
        )

        result = await self.db.execute(stmt)

        return list(result.scalars().all())

    async def delete_by_repository(
        self,
        repository_id: UUID,
    ) -> None:

        messages = await self.list_by_repository(
            repository_id,
        )

        for message in messages:
            await self.db.delete(message)

        await self.db.commit()
