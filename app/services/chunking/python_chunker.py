from __future__ import annotations

import ast

from .base_chunker import BaseChunker
from .generic_chunker import GenericChunker
from .models import Chunk
from .models import ChunkType
from .utils import ChunkUtils


class PythonChunker(BaseChunker):
    """
    AST-aware chunker for Python source code.
    """

    def __init__(
        self,
        max_methods_per_class: int = 3,
    ) -> None:
        self.max_methods_per_class = max_methods_per_class
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

        chunks: list[Chunk] = []
        chunk_index = 0

        import_chunk = self._build_import_chunk(
            tree,
            text,
            chunk_index,
        )

        if import_chunk:
            chunks.append(import_chunk)
            chunk_index += 1

        for node in tree.body:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                continue

            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                chunks.append(
                    self._build_function_chunk(
                        node,
                        text,
                        chunk_index,
                    )
                )
                chunk_index += 1

            elif isinstance(node, ast.ClassDef):
                class_chunks = self._build_class_chunks(
                    node,
                    text,
                    chunk_index,
                )

                chunks.extend(class_chunks)
                chunk_index += len(class_chunks)

        if not chunks:
            return self.generic_chunker.chunk(text)

        return chunks

    def _build_import_chunk(
        self,
        tree: ast.Module,
        text: str,
        chunk_index: int,
    ) -> Chunk | None:
        imports = [
            node for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom))
        ]

        if not imports:
            return None

        start = imports[0].lineno
        end = imports[-1].end_lineno

        content = "\n".join(text.splitlines()[start - 1 : end])

        return self._create_chunk(
            chunk_index=chunk_index,
            chunk_type=ChunkType.IMPORTS,
            symbol_name="__imports__",
            content=content,
            start_line=start,
            end_line=end,
        )

    def _build_function_chunk(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef,
        text: str,
        chunk_index: int,
    ) -> Chunk:
        content = ast.get_source_segment(text, node) or ""

        return self._create_chunk(
            chunk_index=chunk_index,
            chunk_type=ChunkType.FUNCTION,
            symbol_name=node.name,
            content=content,
            start_line=node.lineno,
            end_line=node.end_lineno,
        )

    def _build_class_chunks(
        self,
        node: ast.ClassDef,
        text: str,
        chunk_index: int,
    ) -> list[Chunk]:
        methods = [
            method
            for method in node.body
            if isinstance(
                method,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            )
        ]

        if len(methods) <= self.max_methods_per_class:
            content = ast.get_source_segment(text, node) or ""

            return [
                self._create_chunk(
                    chunk_index=chunk_index,
                    chunk_type=ChunkType.CLASS,
                    symbol_name=node.name,
                    content=content,
                    start_line=node.lineno,
                    end_line=node.end_lineno,
                )
            ]

        return self._build_method_chunks(
            node,
            methods,
            text,
            chunk_index,
        )

    def _build_method_chunks(
        self,
        class_node: ast.ClassDef,
        methods: list[ast.FunctionDef | ast.AsyncFunctionDef],
        text: str,
        chunk_index: int,
    ) -> list[Chunk]:
        chunks: list[Chunk] = []

        class_header = self._build_class_header(class_node)

        for index, method in enumerate(methods):
            method_source = ast.get_source_segment(
                text,
                method,
            )

            if not method_source:
                continue

            content = f"{class_header}\n" f"{self._indent(method_source)}"

            chunks.append(
                self._create_chunk(
                    chunk_index=chunk_index + index,
                    chunk_type=ChunkType.METHOD,
                    symbol_name=f"{class_node.name}.{method.name}",
                    content=content,
                    start_line=method.lineno,
                    end_line=method.end_lineno,
                )
            )

        return chunks

    def _build_class_header(
        self,
        node: ast.ClassDef,
    ) -> str:
        if not node.bases:
            return f"class {node.name}:"

        bases = []

        for base in node.bases:
            bases.append(ast.unparse(base))

        return f"class {node.name}" f"({', '.join(bases)}):"

    def _indent(
        self,
        text: str,
    ) -> str:
        return "\n".join(f"    {line}" if line else "" for line in text.splitlines())

    def _create_chunk(
        self,
        *,
        chunk_index: int,
        chunk_type: ChunkType,
        symbol_name: str,
        content: str,
        start_line: int,
        end_line: int,
    ) -> Chunk:
        return Chunk(
            chunk_index=chunk_index,
            chunk_type=chunk_type,
            symbol_name=symbol_name,
            content=content,
            start_line=start_line,
            end_line=end_line,
            token_count=ChunkUtils.estimate_tokens(content),
            content_hash=ChunkUtils.content_hash(content),
        )
