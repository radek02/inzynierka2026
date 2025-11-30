from fastapi import Depends, Request
from .config import AppConfig,settings
from app.db import IEmbeddingsStorage, QdrantEmbeddingsStorage, IInteractionsRepository, InteractionsRepository
from app.services import ICandidateGeneratorService, CandidateGeneratorService, IRankerService, RankerService, IReRankerService, ReRankerService, UserRecommendationOrchestrator, UserEmbeddingsRecomputer
import psycopg2
from psycopg2.extensions import connection
from collections.abc import Generator
from app.ml_models import IMFModelService, IModelLoader, LocalModelLoader, ALSModelService


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

def get_user_recommendation_orchestrator(candidate_generator: ICandidateGeneratorService = Depends(get_candidate_generator),
                                         ranker: IRankerService = Depends(get_ranker),
                                         reranker: IReRankerService = Depends(get_reranker)):
    return UserRecommendationOrchestrator(candidate_generator=candidate_generator, ranker=ranker, reranker=reranker)

def get_db(config: AppConfig = Depends(get_settings)) -> Generator[connection, None, None]:
    """Dependency for database connection"""
    connection = psycopg2.connect(
        host=config.postgres_host,
        port=config.postgres_port,
        database=config.postgres_db,
        user=config.postgres_user,
        password=config.postgres_password,
    )
    try:
        yield connection
    finally:
        connection.close()

def get_interactions_repository(db: connection = Depends(get_db)) -> IInteractionsRepository:
    return InteractionsRepository(db=db)

def init_model_loader(config: AppConfig) -> IModelLoader:
    return LocalModelLoader(config=config)

def init_mf_model_service(model_loader: IModelLoader) -> IMFModelService:
    return ALSModelService(model_loader=model_loader)

def get_mf_model_service(request: Request) -> IMFModelService:
    return request.app.state.mf_model_service

def get_user_embeddings_recomputer(embeddings_storage: IEmbeddingsStorage = Depends(get_embeddings_storage),
                                   interactions_repository: IInteractionsRepository = Depends(get_interactions_repository),
                                   mf_model_service: IMFModelService = Depends(get_mf_model_service)) -> UserEmbeddingsRecomputer:
    return UserEmbeddingsRecomputer(embeddings_storage=embeddings_storage, interactions_repository=interactions_repository, mf_model_service=mf_model_service)
