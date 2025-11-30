from app.db import IEmbeddingsStorage, IInteractionsRepository
from app.ml_models import IMFModelService

class UserEmbeddingsRecomputer:
    def __init__(self, embeddings_storage: IEmbeddingsStorage, interactions_repository: IInteractionsRepository,
                 mf_model_service: IMFModelService):
        self.embeddings_storage = embeddings_storage
        self.interactions_repository = interactions_repository
        self.mf_model_service = mf_model_service 

    def recompute_user_embeddings(self, user_id: int):
        pass