from __future__ import annotations

from app.services.chunking.base_chunker import BaseChunker
from app.services.chunking.generic_chunker import GenericChunker
from app.services.chunking.python_chunker import PythonChunker


class ChunkFactory:
    """
    Factory responsible for selecting the appropriate chunker
    based on a file's extension.
    """

    def __init__(self) -> None:
        self._generic_chunker = GenericChunker()
        self._python_chunker = PythonChunker()

    def get_chunker(
        self,
        extension: str | None,
    ) -> BaseChunker:
        """
        Return the appropriate chunker for the given file extension.
        """

        if extension is None:
            return self._generic_chunker

        extension = extension.lower()

        match extension:
            case ".py":
                # TODO: Replace with PythonChunker
                return self._python_chunker

            case ".md":
                # TODO: Replace with MarkdownChunker
                return self._generic_chunker

            case ".json":
                # TODO: Replace with JsonChunker
                return self._generic_chunker

            case ".yaml" | ".yml":
                # TODO: Replace with YamlChunker
                return self._generic_chunker

            case ".java":
                # TODO: Replace with JavaChunker
                return self._generic_chunker

            case ".js":
                # TODO: Replace with JavaScriptChunker
                return self._generic_chunker

            case ".ts":
                # TODO: Replace with TypeScriptChunker
                return self._generic_chunker

            case _:
                return self._generic_chunker
