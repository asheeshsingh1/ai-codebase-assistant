# app/services/llm/openai_provider.py
from __future__ import annotations

from openai import APIError, AsyncOpenAI

from app.services.llm.base import LLMProvider
from app.services.llm.exceptions import (
    ChatCompletionError,
    LLMProviderConfigurationError,
)
from app.services.llm.models import ChatMessage


class OpenAIProvider(LLMProvider):
    """
    OpenAI implementation of the LLM provider.
    """

    SUPPORTED_MODELS = {
        "gpt-4.1",
        "gpt-4.1-mini",
        "gpt-4o",
        "gpt-4o-mini",
        "o3",
        "o3-mini",
    }

    def __init__(self, config):
        super().__init__(config)

        if self.model_name not in self.SUPPORTED_MODELS:
            raise LLMProviderConfigurationError(
                f"Unsupported OpenAI model: {self.model_name}"
            )

        self.client = AsyncOpenAI(
            api_key=config.api_key.get_secret_value(),
        )

    async def generate(
        self,
        messages: list[ChatMessage],
    ) -> str:
        """
        Generate a chat completion.
        """

        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": message.role.value,
                        "content": message.content,
                    }
                    for message in messages
                ],
                temperature=self.temperature,
                max_completion_tokens=self.max_tokens,
            )

            content = response.choices[0].message.content

            if not content:
                raise ChatCompletionError("OpenAI returned an empty response.")

            return content

        except APIError as exc:
            raise ChatCompletionError("Failed to generate chat completion.") from exc
