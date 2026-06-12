import logging

from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)

_INSECURE_SECRET_DEFAULTS = frozenset({"change-me-in-production", "secret", ""})


class Settings(BaseSettings):
    APP_NAME: str = "AI Job Application Agent"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/job_agent"

    # JWT — no safe default; must be overridden via env
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    # OpenAI
    OPENAI_API_KEY: str = ""

    # Email (Gmail API)
    GMAIL_CLIENT_ID: str = ""
    GMAIL_CLIENT_SECRET: str = ""
    GMAIL_REFRESH_TOKEN: str = ""
    SENDER_EMAIL: str = ""

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # File Storage
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE_MB: int = 10

    # Job Search
    MATCH_THRESHOLD: float = 0.80

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "production"

    @property
    def parsed_allowed_origins(self) -> list[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",") if o.strip()]


settings = Settings()

if settings.SECRET_KEY in _INSECURE_SECRET_DEFAULTS:
    if settings.is_production:
        raise RuntimeError(
            "SECRET_KEY must be set to a strong random value in production. "
            "Generate one with: python -c \"import secrets; print(secrets.token_urlsafe(64))\""
        )
    logger.warning(
        "SECRET_KEY is using an insecure default. "
        "Set a strong SECRET_KEY before deploying to production."
    )
