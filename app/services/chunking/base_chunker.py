from __future__ import annotations

from abc import ABC, abstractmethod

from .models import Chunk


class BaseChunker(ABC):
    """
    Base interface for all chunking strategies.
    """

    @abstractmethod
    def chunk(
        self,
        text: str,
    ) -> list[Chunk]:
        """
        Chunk the provided text.

        Args:
            text: File contents.

        Returns:
            List of Chunk domain objects.
        """
        raise NotImplementedError