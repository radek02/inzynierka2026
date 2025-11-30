from app.db import IEmbeddingsStorage, IInteractionsRepository
from app.ml_models import IMFModelService

class UserEmbeddingsRecomputer:
    def __init__(self, embeddings_storage: IEmbeddingsStorage, interactions_repository: IInteractionsRepository,
                 mf_model_service: IMFModelService):
        self.embeddings_storage = embeddings_storage
        self.interactions_repository = interactions_repository
        self.mf_model_service = mf_model_service 

    def recompute_user_embeddings(self, user_id: int):
        interactions = self.interactions_repository.get_user_interactions(user_id=user_id)
        if interactions in None or len(interactions) == 0:
            raise Exception("User does not have any interactions")
        new_user_embeddings = self.mf_model_service.recompute_user_embeddings(interactions=interactions)
        self.embeddings_storage.update_user_embeddings(user_id=user_id, new_embeddings=new_user_embeddings)