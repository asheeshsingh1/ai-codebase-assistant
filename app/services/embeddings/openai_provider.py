# app/services/embeddings/openai_provider.py
from openai import AsyncOpenAI

from app.services.embeddings.base import EmbeddingProvider
from app.services.embeddings.config import EmbeddingProviderConfig
from app.services.embeddings.model_registry import OPENAI_MODELS


class OpenAIEmbeddingProvider(EmbeddingProvider):

    def __init__(
        self,
        config: EmbeddingProviderConfig,
    ):
        super().__init__(config)

        if config.model not in OPENAI_MODELS:
            raise ValueError(f"Unsupported OpenAI embedding model: {config.model}")

        self._model = OPENAI_MODELS[config.model]

        self.client = AsyncOpenAI(
            api_key=config.api_key.get_secret_value(),
        )

    @property
    def provider_name(self):
        return self.config.provider

    @property
    def model_name(self):
        return self._model.name

    @property
    def dimensions(self):
        return self._model.dimensions

    async def embed(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        if not texts:
            return []

        response = await self.client.embeddings.create(
            model=self.model_name,
            input=texts,
        )

        return [item.embedding for item in response.data]
