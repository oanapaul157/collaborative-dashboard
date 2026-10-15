from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """App configuration, read from environment variables (and the .env file).

    Each field maps to an env var with the same name, case-insensitive:
    `database_url` is filled from DATABASE_URL. Pydantic validates the types,
    so a missing or malformed value fails loudly at startup, not mid-request.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_url: str = "postgresql+psycopg://taskboard:taskboard@localhost:5432/taskboard"
    cors_origins: list[str] = ["http://localhost:5173"]


settings = Settings()
