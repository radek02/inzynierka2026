from abc import ABC, abstractmethod
from typing import List
from app.models import GeneratedCandidate

class ICandidateGeneratorService(ABC):
    @abstractmethod
    def generate_candidates(self, user_id: int) -> List[GeneratedCandidate]:
        pass

class IRankerService(ABC):
    def rank_candidates(self, user_embeddings: List[float], candidates: List[GeneratedCandidate])  -> List[int]:
        pass

class IReRankerService(ABC):
    def rerank(self, book_ids: List[int]) -> List[int]:
        pass