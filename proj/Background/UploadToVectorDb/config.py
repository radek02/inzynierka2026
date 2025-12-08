from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class AppConfig(BaseSettings):
    user_embeddings_path: str
    book_embeddings_path: str
    user_mapping_path: str
    book_mapping_path: str

    qdrant_url: str = "http://localhost:6333"
    collection_dim: int = 32
    batch_size: int = 10000

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

settings = AppConfig()