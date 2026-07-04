from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    bot_token: str

    postgres_user: str = "currency"
    postgres_password: str = "currency"
    postgres_db: str = "currency"
    postgres_host: str = "db"
    postgres_port: int = 5432

    redis_host: str = "redis"
    redis_port: int = 6379

    rates_cache_ttl: int = 300

    digest_hour: int = 9
    digest_minute: int = 0
    timezone: str = "Europe/Kyiv"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/0"


settings = Settings()
