# app/services/llm/openrouter_provider.py

from __future__ import annotations

import httpx

from app.services.llm.base import LLMProvider
from app.services.llm.exceptions import (
    ChatCompletionError,
    LLMProviderConfigurationError,
)
from app.services.llm.models import ChatMessage


class OpenRouterProvider(LLMProvider):
    """
    OpenRouter implementation of the LLM provider.
    """

    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

    SUPPORTED_MODELS = {
        "openai/gpt-4.1-mini",
        "openai/gpt-4o-mini",
        "meta-llama/llama-3.3-70b-instruct",
        "anthropic/claude-3.5-sonnet",
        "google/gemini-2.5-flash",
        "deepseek/deepseek-chat-v3-0324:free",
        "google/gemma-4-26b-a4b-it:free",
    }

    def __init__(
        self,
        config,
    ) -> None:
        super().__init__(config)

        if self.model_name not in self.SUPPORTED_MODELS:
            raise LLMProviderConfigurationError(
                f"Unsupported OpenRouter model: {self.model_name}"
            )

    async def generate(
        self,
        messages: list[ChatMessage],
    ) -> str:

        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": message.role.value,
                    "content": message.content,
                }
                for message in messages
            ],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

        async with httpx.AsyncClient(timeout=120) as client:

            response = await client.post(
                self.BASE_URL,
                headers={
                    "Authorization": (
                        f"Bearer {self.config.api_key.get_secret_value()}"
                    ),
                    "Content-Type": "application/json",
                },
                json=payload,
            )

        if response.status_code >= 400:
            raise ChatCompletionError(response.text)

        data = response.json()

        try:
            return data["choices"][0]["message"]["content"]

        except (KeyError, IndexError) as exc:
            raise ChatCompletionError(
                "OpenRouter returned an invalid response."
            ) from exc
