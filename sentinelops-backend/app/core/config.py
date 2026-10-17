from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "SentinelOps API"
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./sentinelops.db"
    CORS_ORIGINS: str = "http://localhost:5500,http://127.0.0.1:5500"

    @property
    def cors_origin_list(self) -> list[str]:
        return [s.strip() for s in self.CORS_ORIGINS.split(",") if s.strip()]


settings = Settings()
