from __future__ import annotations

import ast

from .base_chunker import BaseChunker
from .generic_chunker import GenericChunker
from .models import Chunk
from .utils import ChunkUtils


class PythonChunker(BaseChunker):
    """
    AST-aware chunker for Python source files.

    Chunking strategy:
        - Imports (all import statements together)
        - One chunk per top-level function
        - One chunk per top-level class

    If parsing fails, falls back to GenericChunker.
    """

    def __init__(self) -> None:
        self.generic_chunker = GenericChunker()

    def chunk(
        self,
        text: str,
    ) -> list[Chunk]:
        if not text.strip():
            return []

        try:
            tree = ast.parse(text)
        except SyntaxError:
            return self.generic_chunker.chunk(text)

        lines = text.splitlines()

        chunks: list[Chunk] = []
        chunk_index = 0

        # -----------------------------
        # Imports
        # -----------------------------
        import_nodes = [
            node
            for node in tree.body
            if isinstance(node, (ast.Import, ast.ImportFrom))
        ]

        if import_nodes:
            start_line = import_nodes[0].lineno
            end_line = import_nodes[-1].end_lineno

            content = "\n".join(
                lines[start_line - 1 : end_line]
            )

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

        # -----------------------------
        # Top-level functions & classes
        # -----------------------------
        for node in tree.body:
            if not isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                    ast.ClassDef,
                ),
            ):
                continue

            content = ast.get_source_segment(
                text,
                node,
            )

            if not content:
                continue

            chunks.append(
                Chunk(
                    chunk_index=chunk_index,
                    content=content,
                    start_line=node.lineno,
                    end_line=node.end_lineno,
                    token_count=ChunkUtils.estimate_tokens(content),
                    content_hash=ChunkUtils.content_hash(content),
                )
            )

            chunk_index += 1

        # Safety fallback
        if not chunks:
            return self.generic_chunker.chunk(text)

        return chunks