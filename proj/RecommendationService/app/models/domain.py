from pydantic import BaseModel
from typing import List

class GeneratedCandidate(BaseModel):
    book_id: int
    book_embeddings: List[float]
    score: float

class Interaction(BaseModel):
    user_id: int
    book_id: int
    rating: int
    mf_id: int