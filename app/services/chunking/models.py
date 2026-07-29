from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Chunk:
    """
    Represents a logical chunk of a source file.

    This is a domain model used by the chunking pipeline before
    persistence into the database.
    """

    chunk_index: int
    content: str
    start_line: int
    end_line: int
    token_count: int
    content_hash: str