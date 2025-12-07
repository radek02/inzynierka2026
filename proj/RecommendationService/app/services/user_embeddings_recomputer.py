from app.db import IEmbeddingsStorage
from app.ml_models import IMFModelService
from .interactions_service import InteractionsService

class UserEmbeddingsRecomputer:
    def __init__(self, embeddings_storage: IEmbeddingsStorage, interaction_service: InteractionsService,
                 mf_model_service: IMFModelService):
        self.embeddings_storage = embeddings_storage
        self.interaction_service = interaction_service
        self.mf_model_service = mf_model_service 

    def recompute_user_embeddings(self, user_id: int):
        interactions = self.interaction_service.get_interactions_with_mf_id(user_id=user_id)
        if interactions is None or len(interactions) == 0:
            raise Exception("User does not have any interactions")
        new_user_embeddings = self.mf_model_service.recompute_user_embeddings(interactions=interactions)
        self.embeddings_storage.update_user_embeddings(user_id=user_id, new_embeddings=new_user_embeddings)