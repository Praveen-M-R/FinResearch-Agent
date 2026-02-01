"""
Application configuration using Pydantic Settings
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    APP_NAME: str = "FinResearch Agent"
    APP_VERSION: str = "0.1.0"
    APP_ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Google GenAI
    GOOGLE_GENAI_API_KEY: str

    # Ollama
    OLLAMA_HOST_URL: str = "http://localhost:11434/v1"
    OLLAMA_MODEL: str = "qwen3:0.6b"


# Global settings instance
settings = Settings()
