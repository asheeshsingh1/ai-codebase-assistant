from __future__ import annotations

from google import genai
from google.genai import types

from app.services.llm.base import LLMProvider
from app.services.llm.exceptions import (
    ChatCompletionError,
    LLMProviderConfigurationError,
)
from app.services.llm.models import ChatMessage, ChatRole


class GeminiProvider(LLMProvider):
    """
    Google Gemini implementation of the LLM provider.
    """

    SUPPORTED_MODELS = {
        "gemini-3.5-flash",
        "gemini-2.5-pro",
    }

    def __init__(
        self,
        config,
    ) -> None:
        super().__init__(config)

        if self.model_name not in self.SUPPORTED_MODELS:
            raise LLMProviderConfigurationError(
                f"Unsupported Gemini model: {self.model_name}"
            )

        if not self.config.api_key:
            raise LLMProviderConfigurationError("Gemini API key is required.")

        self.client = genai.Client(api_key=self.config.api_key.get_secret_value())

    async def generate(
        self,
        messages: list[ChatMessage],
    ) -> str:

        system_instruction = None
        contents = []

        for message in messages:
            if message.role == ChatRole.SYSTEM:
                system_instruction = message.content
                continue

            contents.append(
                types.Content(
                    role=("user" if message.role == ChatRole.USER else "model"),
                    parts=[types.Part.from_text(text=message.content)],
                )
            )

        try:
            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=self.temperature,
                    max_output_tokens=self.max_tokens,
                ),
            )

            if not response.text:
                raise ChatCompletionError("Gemini returned an empty response.")

            return response.text

        except ChatCompletionError:
            raise

        except Exception as exc:
            raise ChatCompletionError(f"Gemini request failed: {exc}") from exc
