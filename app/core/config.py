from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Codebase Assistant"
    app_env: str = "development"
    debug: bool = True

    database_url: str

    gemini_api_key: str

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )
    repository_storage_path: str = "storage/repos"


settings = Settings()