from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class AppConfig(BaseSettings):
    fastapi_host: str
    fastapi_port: str
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

settings = AppConfig()