from fastapi import Depends
from .config import AppConfig,settings
from app.db import IEmbeddingsStorage, QdrantEmbeddingsStorage
from app.services import ICandidateGeneratorService, CandidateGeneratorService, IRankerService, RankerService, IReRankerService, ReRankerService

def get_settings() -> AppConfig:
    return settings

def get_embeddings_storage(config: AppConfig = Depends(get_settings)) -> IEmbeddingsStorage:
    return QdrantEmbeddingsStorage(config)

def get_candidate_generator(repo: IEmbeddingsStorage = Depends(get_embeddings_storage)) -> ICandidateGeneratorService:
    return CandidateGeneratorService(embeddings_repository=repo)

def get_ranker() -> IRankerService:
    return RankerService()

def get_reranker() -> IReRankerService:
    return ReRankerService()