from __future__ import annotations

import hashlib


class ChunkUtils:
    """
    Shared helper methods for all chunkers.
    """

    @staticmethod
    def estimate_tokens(text: str) -> int:
        """
        Rough token estimation.

        For now we use whitespace splitting.
        Later this can be replaced with tiktoken.
        """
        return len(text.split())

    @staticmethod
    def content_hash(text: str) -> str:
        """
        Generate a deterministic SHA-256 hash for a chunk.
        """
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    @staticmethod
    def line_count(text: str) -> int:
        """
        Number of lines in a text block.
        """
        if not text:
            return 0

        return text.count("\n") + 1