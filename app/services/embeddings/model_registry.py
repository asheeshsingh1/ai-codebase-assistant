# app/services/embeddings/model_registry.py
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EmbeddingModel:
    name: str
    dimensions: int


OPENAI_MODELS = {
    "text-embedding-3-small": EmbeddingModel(
        name="text-embedding-3-small",
        dimensions=1536,
    ),
    "text-embedding-3-large": EmbeddingModel(
        name="text-embedding-3-large",
        dimensions=3072,
    ),
}
