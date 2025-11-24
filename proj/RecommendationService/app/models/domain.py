from pydantic import BaseModel
from typing import List

class GeneratedCandidate(BaseModel):
    book_id: int
    book_embeddings: List[float]
    score: float