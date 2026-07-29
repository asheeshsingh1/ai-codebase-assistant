from __future__ import annotations

from .base_chunker import BaseChunker
from .models import Chunk
from .utils import ChunkUtils


class GenericChunker(BaseChunker):
    """
    Generic text chunker using a sliding window.
    """

    def __init__(
        self,
        chunk_size: int = 1200,
        overlap: int = 200,
    ):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(
        self,
        text: str,
    ) -> list[Chunk]:
        if not text.strip():
            return []

        chunks: list[Chunk] = []

        start = 0
        chunk_index = 0

        while start < len(text):
            end = min(start + self.chunk_size, len(text))

            content = text[start:end]

            start_line = text[:start].count("\n") + 1
            end_line = start_line + ChunkUtils.line_count(content) - 1

            chunks.append(
                Chunk(
                    chunk_index=chunk_index,
                    content=content,
                    start_line=start_line,
                    end_line=end_line,
                    token_count=ChunkUtils.estimate_tokens(content),
                    content_hash=ChunkUtils.content_hash(content),
                )
            )

            chunk_index += 1

            if end == len(text):
                break

            start = end - self.overlap

        return chunks