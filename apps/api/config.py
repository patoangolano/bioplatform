from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str = "redis://localhost:6379/0"
    API_SECRET_KEY: str
    ALLOWED_ORIGINS: str = "*"

    # ESM3 protein language model
    ESM_API_URL: str = "https://api.evolutionaryscale.ai"
    ESM_API_KEY: str = ""

    # Biosafety screening
    BIOSAFETY_STRICT_MODE: bool = False  # Se True, bloqueia MEDIUM também

    def get_allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
