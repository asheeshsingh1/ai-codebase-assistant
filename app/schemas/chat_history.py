from pydantic import BaseModel


class ChatMessageResponse(BaseModel):
    role: str
    content: str
    citations: list | None = None


class ChatHistoryResponse(BaseModel):
    messages: list[ChatMessageResponse]
