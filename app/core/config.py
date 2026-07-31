# app/core/config.py
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from app.services.embeddings.models import EmbeddingProviderType
from app.services.llm.models import LLMProviderType


class Settings(BaseSettings):
    enable_embeddings: bool = True
    app_name: str = "AI Codebase Assistant"
    app_env: str = "development"
    debug: bool = True

    database_url: str
    repository_storage_path: str = "storage/repos"

    # AI
    embedding_provider: EmbeddingProviderType = EmbeddingProviderType.OPENAI
    embedding_model: str = "text-embedding-3-small"

    openai_api_key: SecretStr | None = None
    gemini_api_key: SecretStr | None = None
    voyage_api_key: SecretStr | None = None
    openrouter_api_key: SecretStr | None = None

    llm_provider: LLMProviderType = LLMProviderType.OPENROUTER
    llm_model: str = "google/gemma-4-26b-a4b-it:free"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )


settings = Settings()
