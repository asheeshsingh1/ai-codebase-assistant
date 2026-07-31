# app/services/llm/base.py
from __future__ import annotations

from abc import ABC, abstractmethod

from app.services.llm.config import LLMProviderConfig
from app.services.llm.models import LLMProviderType
from app.services.llm.models import ChatMessage


class LLMProvider(ABC):
    """
    Base class for all LLM providers.
    """

    def __init__(
        self,
        config: LLMProviderConfig,
    ) -> None:
        self.config = config

    @property
    def provider_name(self) -> LLMProviderType:
        return self.config.provider

    @property
    def model_name(self) -> str:
        return self.config.model

    @property
    def temperature(self) -> float:
        return self.config.temperature

    @property
    def max_tokens(self) -> int:
        return self.config.max_tokens

    @abstractmethod
    async def generate(
        self,
        messages: list[ChatMessage],
    ) -> str:
        """
        Generate a chat completion.
        """
        raise NotImplementedError
