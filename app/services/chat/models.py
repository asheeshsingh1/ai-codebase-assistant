from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True, frozen=True)
class Citation:
    """
    Represents a source citation used to answer a question.
    """

    repository_file_id: UUID
    file_path: str
    start_line: int
    end_line: int


@dataclass(slots=True)
class ChatResult:
    """
    Result returned by ChatService.
    """

    answer: str
    citations: list[Citation]
