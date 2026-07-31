from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ChatRequest(BaseModel):
    """
    Request payload for repository chat.
    """

    question: str = Field(
        ...,
        min_length=1,
        max_length=10_000,
        description="Question about the repository.",
    )


class CitationResponse(BaseModel):
    """
    Citation returned with a chat response.
    """

    file_path: str
    start_line: int
    end_line: int

    model_config = ConfigDict(
        frozen=True,
    )


class ChatResponse(BaseModel):
    """
    Response payload for repository chat.
    """

    answer: str

    citations: list[CitationResponse] = Field(
        default_factory=list,
    )

    model_config = ConfigDict(
        frozen=True,
    )
