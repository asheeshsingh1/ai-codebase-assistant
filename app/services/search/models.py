from __future__ import annotations

from dataclasses import dataclass

from app.db.models.file_chunk import FileChunk


@dataclass(slots=True, frozen=True)
class SearchResult:
    """
    Represents a semantic search result.

    Attributes:
        chunk: The matched file chunk.
        similarity: Cosine similarity score in the range [0, 1].
    """

    chunk: FileChunk
    similarity: float
