# app/services/llm/provider_factory.py
from __future__ import annotations

from app.services.llm.base import LLMProvider
from app.services.llm.config import LLMProviderConfig
from app.services.llm.exceptions import (
    LLMProviderConfigurationError,
)
from app.services.llm.models import LLMProviderType
from app.services.llm.openai_provider import OpenAIProvider
from app.services.llm.openrouter_provider import OpenRouterProvider


class LLMProviderFactory:
    """
    Factory responsible for creating LLM provider instances.
    """

    @staticmethod
    def create(
        config: LLMProviderConfig,
    ) -> LLMProvider:
        match config.provider:
            case LLMProviderType.OPENAI:
                return OpenAIProvider(config)

            case LLMProviderType.OPENROUTER:
                return OpenRouterProvider(config)

            case LLMProviderType.GEMINI:
                raise NotImplementedError("Gemini provider is not implemented.")

            case LLMProviderType.ANTHROPIC:
                raise NotImplementedError("Anthropic provider is not implemented.")

            case _:
                raise LLMProviderConfigurationError(
                    f"Unsupported LLM provider: {config.provider}"
                )
