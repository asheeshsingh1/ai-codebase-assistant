from __future__ import annotations


class RepositoryFileError(Exception):
    """
    Base exception for repository operations.
    """


class RepositoryFileNotFoundError(RepositoryFileError):
    """
    Raised when a repository cannot be found.
    """
