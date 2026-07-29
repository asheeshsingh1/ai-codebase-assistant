from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ChunkType(str, Enum):
    """
    Represents the semantic type of a chunk.
    """

    TEXT = "text"
    IMPORTS = "imports"
    CLASS = "class"
    METHOD = "method"
    FUNCTION = "function"


@dataclass(slots=True)
class Chunk:
    """
    Domain model representing a chunk of source code or text.

    This model is independent of persistence (SQLAlchemy) and is used by
    chunkers to return semantic chunks to the ChunkService.
    """

    chunk_index: int

    chunk_type: ChunkType

    content: str

    start_line: int

    end_line: int

    token_count: int

    content_hash: str

    symbol_name: str | None = None
