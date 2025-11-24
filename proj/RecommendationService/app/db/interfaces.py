from abc import ABC, abstractmethod
from typing import List 
from app.models import GeneratedCandidate

class IEmbeddingsStorage(ABC):
    @abstractmethod
    def get_user_embeddings(self, user_id: int) -> List[float]:
        pass

    @abstractmethod
    def get_best_books(self, user_embeddings: List[float], amount: int) -> List[GeneratedCandidate]:
        pass

    @abstractmethod
    def update_user_embeddings(self, user_id: int, new_embeddings: List[float]):
        pass