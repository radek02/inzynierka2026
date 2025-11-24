from fastapi import Depends
from config import AppConfig,settings
from app.db import IEmbeddingsStorage, QdrantEmbeddingsStorage

def get_settings() -> AppConfig:
    return settings

def get_embeddings_storage(config: AppConfig = Depends(get_settings)) -> IEmbeddingsStorage:
    return QdrantEmbeddingsStorage(config)