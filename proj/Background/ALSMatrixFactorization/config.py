from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class AppConfig(BaseSettings):
    interactions_path: str
    model_saving_path: str
    collection_dim: int

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

settings = AppConfig()