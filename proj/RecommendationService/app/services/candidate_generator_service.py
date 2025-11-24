from .interfaces import ICandidateGeneratorService
from app.db import IEmbeddingsStorage
from typing import List
from app.models import GeneratedCandidate

class CandidateGeneratorService(ICandidateGeneratorService):
    def __init__(self, embeddings_repository: IEmbeddingsStorage):
        self.embeddings_repository = embeddings_repository

    def generate_candidates(self, user_id: int) -> List[GeneratedCandidate]:
        try:
            user_embeddings = self.embeddings_repository.get_user_embeddings(user_id)
            candidates = self.embeddings_repository.get_best_books(user_embeddings=user_embeddings, amount=10)
            return candidates
        except ValueError:
            print(f"User ID {user_id} not found.")
            raise
        
         
        