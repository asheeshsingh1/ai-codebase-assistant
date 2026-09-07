from google import genai
from google.genai import types

from app.services.embeddings.base import EmbeddingProvider
from app.services.embeddings.config import EmbeddingProviderConfig


class GeminiEmbeddingProvider(EmbeddingProvider):

    SUPPORTED_MODELS = {
        "gemini-embedding-2": 768,
    }

    def __init__(
        self,
        config: EmbeddingProviderConfig,
    ) -> None:
        super().__init__(config)

        if config.model not in self.SUPPORTED_MODELS:
            raise ValueError(f"Unsupported Gemini embedding model: {config.model}")

        if not config.api_key:
            raise ValueError("Gemini API key is required.")

        self._model = config.model

        self.client = genai.Client(api_key=config.api_key.get_secret_value())

    @property
    def model_name(self) -> str:
        return self._model

    @property
    def dimensions(self) -> int:
        return self.SUPPORTED_MODELS[self._model]

    async def embed(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        if not texts:
            return []

        embeddings: list[list[float]] = []

        for text in texts:
            response = await self.client.aio.models.embed_content(
                model=self.model_name,
                contents=text,
                config=types.EmbedContentConfig(
                    output_dimensionality=self.dimensions,
                ),
            )

            if not response.embeddings:
                raise ValueError("Gemini returned an empty embedding response.")

            embeddings.append(response.embeddings[0].values)

        return embeddings
