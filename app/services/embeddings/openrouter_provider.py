from httpx import AsyncClient

from app.services.embeddings.base import EmbeddingProvider
from app.services.embeddings.config import EmbeddingProviderConfig
from app.services.embeddings.model_registry import OPENROUTER_MODELS


class OpenRouterEmbeddingProvider(EmbeddingProvider):

    BASE_URL = "https://openrouter.ai/api/v1/embeddings"

    def __init__(
        self,
        config: EmbeddingProviderConfig,
    ) -> None:
        super().__init__(config)

        if config.model not in OPENROUTER_MODELS:
            raise ValueError(f"Unsupported OpenRouter embedding model: {config.model}")

        self._model = OPENROUTER_MODELS[config.model]

    @property
    def model_name(self) -> str:
        return self._model.name

    @property
    def dimensions(self) -> int:
        return self._model.dimensions

    async def embed(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        if not texts:
            return []

        async with AsyncClient() as client:

            response = await client.post(
                self.BASE_URL,
                headers={
                    "Authorization": (
                        f"Bearer {self.config.api_key.get_secret_value()}"
                    ),
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model_name,
                    "input": texts,
                    "encoding_format": "float",
                },
                timeout=60,
            )

        response.raise_for_status()

        data = response.json()

        return [item["embedding"] for item in data["data"]]
