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
    embedding_provider: EmbeddingProviderType = EmbeddingProviderType.GEMINI
    embedding_model: str = "gemini-embedding-2"

    openai_api_key: SecretStr | None = None
    gemini_api_key: SecretStr | None = None
    voyage_api_key: SecretStr | None = None
    openrouter_api_key: SecretStr | None = None

    llm_provider: LLMProviderType = LLMProviderType.GEMINI
    llm_model: str = "gemini-3.5-flash"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )


settings = Settings()
