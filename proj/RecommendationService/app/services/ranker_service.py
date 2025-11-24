from .interfaces import IRankerService
from typing import List 
from app.models import GeneratedCandidate

class RankerService(IRankerService):
    def __init__(self):
        pass

    def rank_candidates(self, user_embeddings: List[float], candidates: List[GeneratedCandidate])  -> List[int]:
        user_embeddings = user_embeddings
        res = []
        for candidate in candidates:
            res.append(candidate.book_id)
        return res