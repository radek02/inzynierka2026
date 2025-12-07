from abc import ABC, abstractmethod
from typing import List, Dict 
from app.models import GeneratedCandidate, Interaction

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
    
    @abstractmethod
    def get_mf_ids(self, collection_name: str, native_ids: List[int]) -> Dict[int, int]:
        pass

class IInteractionsRepository(ABC):
    @abstractmethod
    def get_user_interactions(self, user_id: int) -> List[Interaction]:
        pass