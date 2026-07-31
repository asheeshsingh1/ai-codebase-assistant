# app/services/llm/exceptions.py
from __future__ import annotations


class LLMProviderError(Exception):
    """
    Base exception for all LLM provider errors.
    """


class LLMProviderConfigurationError(LLMProviderError):
    """
    Raised when an LLM provider is misconfigured.
    """


class ChatCompletionError(LLMProviderError):
    """
    Raised when chat completion generation fails.
    """
