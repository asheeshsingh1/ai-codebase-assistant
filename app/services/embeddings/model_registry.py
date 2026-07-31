from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EmbeddingModel:
    name: str
    dimensions: int


OPENAI_MODELS: dict[str, EmbeddingModel] = {
    "text-embedding-3-small": EmbeddingModel(
        name="text-embedding-3-small",
        dimensions=1536,
    ),
    "text-embedding-3-large": EmbeddingModel(
        name="text-embedding-3-large",
        dimensions=3072,
    ),
    "text-embedding-ada-002": EmbeddingModel(
        name="text-embedding-ada-002",
        dimensions=1536,
    ),
}

OPENROUTER_MODELS = {
    "nvidia/nemotron-3-embed-1b:free": EmbeddingModel(
        name="nvidia/nemotron-3-embed-1b:free",
        dimensions=2048,  # Verify this value from the provider docs or API.
    ),
}
