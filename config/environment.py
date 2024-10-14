from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB_NAME: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    BOT_TOKEN: str = ""
    CHAT_ID: int = -1

    model_config = SettingsConfigDict(
        case_sensitive = True,
        env_file = "./.env",
        extra = "ignore",
    )
