from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class AppConfig(BaseSettings):
    interactions_path: str
    model_saving_dir: str
    file_saving_dir: str
    collection_dim: int
    als_regularization: float
    als_epochs: int

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

settings = AppConfig()