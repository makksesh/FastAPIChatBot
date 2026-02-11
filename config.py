from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    gemini_api_key: str

    database_url: str = "sqlite+aiosqlite:///chatbot.db" # Значение по умолчанию

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

config_obj = Settings()