from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    database_username: str
    database_password: str
    database_host: str
    database_name: str
    jwt_secret: str
    azure_api_key: str
    azure_storage_connection_string: str
    azure_blob_container_name: str

    keyword_api_key: str
    keyword_endpoint: str

    gpt_audio_key: str


@lru_cache
def get_settings():
    return Settings()