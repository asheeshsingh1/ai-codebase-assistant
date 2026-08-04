from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict


class RepositoryFileResponse(BaseModel):
    """
    Basic metadata about a repository file.
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    relative_path: str
    language: str | None
    extension: str


class RepositoryFileContentResponse(BaseModel):
    """
    Complete file contents returned to the frontend.
    """

    id: UUID
    relative_path: str
    language: str | None
    extension: str
    content: str
