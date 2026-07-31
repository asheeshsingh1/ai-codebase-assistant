# app/services/llm/config.py
from __future__ import annotations

from dataclasses import dataclass

from pydantic import SecretStr

from app.services.llm.models import LLMProviderType


@dataclass(slots=True)
class LLMProviderConfig:
    """
    Configuration for an LLM provider.
    """

    provider: LLMProviderType
    api_key: SecretStr
    model: str

    temperature: float = 0.2
    max_tokens: int = 4096
