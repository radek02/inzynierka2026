from typing import List

from app.db import IEmbeddingsStorage, IInteractionsRepository
from app.models import Interaction

class InteractionsService:
    def __init__(self, embeddings_repository: IEmbeddingsStorage, interactions_repository: IInteractionsRepository):
        self.embeddings_repository = embeddings_repository
        self.interactions_repository = interactions_repository

    def get_interactions_with_mf_id(self, user_id: int) -> List[Interaction]:
        interactions = self.interactions_repository.get_user_interactions(user_id=user_id)
        mf_id_dictionary = self.embeddings_repository.get_mf_ids("books", [i.book_id for i in interactions])
        valid_interactions = []
        for i in interactions:
            mf_id = mf_id_dictionary.get(i.book_id)
            if mf_id is None:
                continue 
            i.mf_id = mf_id
            valid_interactions.append(i)
        return valid_interactions