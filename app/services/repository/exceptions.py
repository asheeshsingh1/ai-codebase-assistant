from __future__ import annotations


class RepositoryError(Exception):
    """
    Base exception for repository operations.
    """


class RepositoryNotFoundError(RepositoryError):
    """
    Raised when a repository cannot be found.
    """


class RepositoryAlreadyExistsError(RepositoryError):
    """
    Raised when a repository with the same Git URL already exists.
    """
