from __future__ import annotations


class ChatError(Exception):
    """
    Base exception for all chat-related errors.
    """


class PromptConstructionError(ChatError):
    """
    Raised when the prompt cannot be constructed.
    """


class ContextRetrievalError(ChatError):
    """
    Raised when repository context cannot be retrieved.
    """


class RepositoryNotIndexedError(ChatError):
    """
    Raised when a repository has not yet been indexed and is
    therefore unavailable for chat.
    """


class EmptyContextError(ChatError):
    """
    Raised when no relevant context could be found for a query.
    """
