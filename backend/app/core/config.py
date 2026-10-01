from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    gemini_api_key: str
    default_model: str = "gemini-3.6-flash"
    redis_url: str 
    monthly_budget: float = 5.00  # USD

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )
settings = Settings()