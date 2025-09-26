"""Configuration settings for ChatWait backend.

Loads configuration from environment variables with sensible defaults.
"""

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # === OPENAI AGENTS SDK CONFIGURATION ===
    gemini_api_key: str = Field(
        ..., description="Gemini API key for OpenAI-compatible endpoint"
    )
    gemini_model: str = Field(
        default="gemini-2.5-flash", description="Gemini model to use"
    )
    gemini_base_url: str = Field(
        default="https://generativelanguage.googleapis.com/v1beta/openai/",
        description="Gemini API base URL",
    )

    # === FASTAPI CONFIGURATION ===
    host: str = Field(default="localhost", description="Server host")
    port: int = Field(default=8000, description="Server port")
    debug: bool = Field(default=False, description="Enable debug mode")
    reload: bool = Field(
        default=False, description="Enable auto-reload for development"
    )

    # === CORS CONFIGURATION ===
    allowed_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:3000", "http://localhost:8000"],
        description="Allowed CORS origins",
    )

    # === LOGGING CONFIGURATION ===
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(default="json", description="Log format")

    # === PERFORMANCE CONFIGURATION ===
    max_tokens_per_response: int = Field(
        default=4096, description="Maximum tokens per response"
    )
    streaming_chunk_size: int = Field(default=1024, description="Streaming chunk size")
    response_timeout_seconds: int = Field(default=30, description="Response timeout")

    # === SECURITY CONFIGURATION ===
    rate_limit_requests_per_minute: int = Field(
        default=60, description="Rate limit requests per minute"
    )
    rate_limit_burst: int = Field(default=10, description="Rate limit burst capacity")

    # === MONITORING CONFIGURATION ===
    health_check_path: str = Field(default="/health", description="Health check path")
    health_check_interval_seconds: int = Field(
        default=30, description="Health check interval"
    )

    @computed_field
    def environment(self) -> str:
        """Determine environment from debug flag."""
        return "development" if self.debug else "production"


# Create settings instance
settings = Settings()
