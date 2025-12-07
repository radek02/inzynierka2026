from models import Interaction
from typing import List
from db import IEmbeddingsStorage

class InteractionsService:
    def __init__(self, embeddings_repository: IEmbeddingsStorage):
        self.embeddings_repository = embeddings_repository

    def get_interactions_with_mf_id(self, user_id: int) -> List[Interaction]:
        pass